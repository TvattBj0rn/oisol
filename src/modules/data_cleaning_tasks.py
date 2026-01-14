from __future__ import annotations

import configparser
import datetime
import sqlite3
from typing import TYPE_CHECKING

import aiohttp
from discord.ext import commands, tasks

from src.utils import (
    OISOL_HOME_PATH,
    DataFilesPath,
    FoxholeAsyncAPIWrapper,
    InterfacesTypes,
    Shard,
)

if TYPE_CHECKING:
    from main import Oisol


class DatabaseCleaner(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot

        # Clear existing stockpiles at war's end
        if Shard.ABLE.name in self.bot.connected_shards:
            self.clear_stockpiles_able.start()
        if Shard.BAKER.name in self.bot.connected_shards:
            self.clear_stockpiles_baker.start()
        if Shard.CHARLIE.name in self.bot.connected_shards:
            self.clear_stockpiles_charlie.start()


    async def _clear_stockpiles_new_war(self, shard_api: FoxholeAsyncAPIWrapper) -> None:
        async with aiohttp.ClientSession() as session:
            current_state = await shard_api.get_current_war_state(session)
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

        self.bot.logger.task(f'Stockpile interfaces were cleared for shard {shard_api.shard_name}')

    @tasks.loop(hours=1)
    async def clear_stockpiles_able(self) -> None:
        await self._clear_stockpiles_new_war(FoxholeAsyncAPIWrapper())

    @tasks.loop(hours=1)
    async def clear_stockpiles_baker(self) -> None:
        await self._clear_stockpiles_new_war(FoxholeAsyncAPIWrapper(shard=Shard.BAKER))

    @tasks.loop(hours=1)
    async def clear_stockpiles_charlie(self) -> None:
        await self._clear_stockpiles_new_war(FoxholeAsyncAPIWrapper(shard=Shard.CHARLIE))
