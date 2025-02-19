from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING

import discord
from discord.ext import commands, tasks

from src.utils import InterfaceType

if TYPE_CHECKING:
    from main import Oisol


class DatabaseCleaner(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot
        self.remove_non_existing_interfaces.start()

    def _clear_entries(self, channel_id: int, message_id: int, interface_type: str, interface_reference: str) -> None:
        for table, column in InterfaceType[interface_type].value:
            self.bot.cursor.execute(f"DELETE FROM {table} WHERE {column} == '{interface_reference}'")
        self.bot.cursor.execute(
            f'DELETE FROM AllInterfacesReferences WHERE ChannelId == {channel_id} AND MessageId == {message_id}',
        )
        self.bot.connection.commit()

    @tasks.loop(hours=168)
    async def remove_non_existing_interfaces(self) -> None:
        start_time = time.time()
        all_existing_interfaces = self.bot.cursor.execute(
            'SELECT ChannelId, MessageId, InterfaceType, InterfaceReference FROM AllInterfacesReferences',
        ).fetchall()
        for channel_id, message_id, interface_type, interface_reference in all_existing_interfaces:
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                self._clear_entries(channel_id, message_id, interface_type, interface_reference)
                continue
            try:
                await channel.fetch_message(message_id)
            except discord.NotFound:
                # Associated message was deleted
                self._clear_entries(channel_id, message_id, interface_type, interface_reference)
            except (discord.Forbidden, discord.HTTPException):
                # Rights of the bot have been removed or fail on network part
                continue
        logging.info(f'[TASK] remove_non_existing_interface task complete in {time.time() - start_time}s')
