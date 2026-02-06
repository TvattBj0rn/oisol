from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

if TYPE_CHECKING:
    from main import Oisol


class ModuleOwner(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot

    @app_commands.command(name='refresh_possible_shards')
    @app_commands.dm_only()
    async def refresh_available_shards(self, interaction: discord.Interaction) -> None:
        if interaction.user.id != self.bot.owner_id:
            await interaction.response.send_message("> This command can only be run by the bot's owner", ephemeral=True, delete_after=5)
            return

        await interaction.response.defer(ephemeral=True)
        await self.bot.fetch_available_shards()
        await interaction.followup.send('> The available shards were updated', ephemeral=True)
