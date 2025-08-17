from __future__ import annotations

import configparser
import datetime
import sqlite3
import time
from typing import TYPE_CHECKING

import discord
from discord.ext import commands, tasks

from src.modules.stockpile_viewer.module_stockpile import (
    update_all_associated_stockpiles,
)
from src.utils import (
    OISOL_HOME_PATH,
    DataFilesPath,
    FoxholeAPIWrapper,
    InterfacesTypes,
    InterfaceType,
    Shard,
)

if TYPE_CHECKING:
    from main import Oisol


class DatabaseCleaner(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot
        # Clear available interfaces that were deleted
        self.remove_non_existing_interfaces.start()

        # Clear existing stockpiles at war's end
        self.clear_stockpiles_able.start()
        self.clear_stockpiles_baker.start()
        self.clear_stockpiles_charlie.start()

    @staticmethod
    def _clear_entries(
            conn_cursor: tuple[sqlite3.Connection, sqlite3.Cursor],
            channel_id: int,
            message_id: int,
            interface_type: str,
            interface_reference: str,
    ) -> None:
        for table, column in InterfaceType[interface_type].value:
            conn_cursor[1].execute(
                f'DELETE FROM {table} WHERE ? == ?',
                (column, interface_reference),
            )

        conn_cursor[1].execute(
            'DELETE FROM AllInterfacesReferences WHERE ChannelId == ? AND MessageId == ?',
            (channel_id, message_id),
        )

        conn_cursor[0].commit()

    @tasks.loop(hours=24)
    async def remove_non_existing_interfaces(self) -> None:
        start_time = time.time()
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            all_existing_interfaces = cursor.execute(
                'SELECT ChannelId, MessageId, InterfaceType, InterfaceReference FROM AllInterfacesReferences',
            ).fetchall()
            for channel_id, message_id, interface_type, interface_reference in all_existing_interfaces:
                # Check if the interface exists
                channel = self.bot.get_channel(int(channel_id))
                try:
                    await channel.fetch_message(int(message_id))
                except (discord.NotFound, AttributeError):
                    # Associated message does not exist on the path given in the db
                    self._clear_entries((conn, cursor), int(channel_id), int(message_id), interface_type, interface_reference)
                except (discord.Forbidden, discord.HTTPException):
                    # Rights of the bot have been removed or fail on network part
                    continue
        self.bot.logger.task(f'remove_non_existing_interface task complete in {time.time() - start_time}s')


    async def _clear_stockpiles_new_war(self, shard_api: FoxholeAPIWrapper) -> None:
        current_state = shard_api.get_current_war_state()
        if (
                current_state.get('conquestEndTime') is None # The war is still active
                or (res_start_time := current_state.get('resistanceStartTime')) is None # Ensure we can work with the resistanceStartTime otherwise
        ):
            return
        # Check if current time is in the interval of res_start_time and res_start_time + 2 hours
        # to ensure we run this task only once
        if datetime.datetime.now().timestamp() > res_start_time / 1000 + 7200:
            return
        shard_guilds = []

        for guild in self.bot.guilds:
            # Overwrite config each time to ensure no leftover from previous config file
            config = configparser.ConfigParser()
            config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{guild.id}.ini')

            if config.has_option('default', 'shard') and config.get('default', 'shard') == shard_api.shard_name:
                shard_guilds.append(guild.id)

        # No guild exist for specified shard
        if not shard_guilds:
            return

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            all_stockpiles_interfaces = cursor.execute(
                f'''
                SELECT AssociationId FROM AllInterfacesReferences
                WHERE InterfaceType IN (?, ?) AND GroupId IN ({', '.join('?' * len(shard_guilds))})
                ''',
                (InterfacesTypes.STOCKPILE.value, InterfacesTypes.MULTISERVER_STOCKPILE.value, *shard_guilds),
            ).fetchall()

            cursor.executemany(
                'DELETE FROM GroupsStockpilesList WHERE AssociationId == ?',
                all_stockpiles_interfaces,
            )
        for association_id, *_ in all_stockpiles_interfaces:
            await update_all_associated_stockpiles(self.bot, association_id)

        self.bot.logger.task(f'Stockpile interfaces were cleared for shard {shard_api.shard_name}')

    @tasks.loop(hours=1)
    async def clear_stockpiles_able(self) -> None:
        await self._clear_stockpiles_new_war(FoxholeAPIWrapper())

    @tasks.loop(hours=1)
    async def clear_stockpiles_baker(self) -> None:
        await self._clear_stockpiles_new_war(FoxholeAPIWrapper(shard=Shard.BAKER))

    @tasks.loop(hours=1)
    async def clear_stockpiles_charlie(self) -> None:
        await self._clear_stockpiles_new_war(FoxholeAPIWrapper(shard=Shard.CHARLIE))
