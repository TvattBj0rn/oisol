from __future__ import annotations

import sqlite3
import time
from typing import TYPE_CHECKING

import discord
from discord.ext import commands, tasks

from src.utils import OISOL_HOME_PATH, InterfaceType

if TYPE_CHECKING:
    from main import Oisol


class DatabaseCleaner(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot
        self.remove_non_existing_interfaces.start()

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
                channel = self.bot.get_channel(int(channel_id))
                if channel is None:
                    self._clear_entries((conn, cursor), int(channel_id), int(message_id), interface_type, interface_reference)
                    continue
                try:
                    await channel.fetch_message(int(message_id))
                except discord.NotFound:
                    # Associated message was deleted
                    self._clear_entries((conn, cursor), int(channel_id), int(message_id), interface_type, interface_reference)
                except (discord.Forbidden, discord.HTTPException):
                    # Rights of the bot have been removed or fail on network part
                    continue
        self.bot.logger.task(f'[TASK] remove_non_existing_interface task complete in {time.time() - start_time}s')
