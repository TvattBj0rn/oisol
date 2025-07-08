from __future__ import annotations

import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands
from libretranslatepy import LibreTranslateAPI

from src.utils.languages_per_country import TERRITORY_LANGUAGES

if TYPE_CHECKING:
    from main import Oisol


class ModuleTranslation(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot
        self.lt_api = LibreTranslateAPI(os.getenv('LIBRETRANSLATE_API_IP'))
        self.bot.tree.add_command(
            app_commands.ContextMenu(
                name='Translate',
                callback=self.translate_to_user_language,
            ),
        )

    async def translate_to_user_language(self, interaction: discord.Interaction, message: discord.Message) -> None:
        self.bot.logger.command(f'translate command by {interaction.user.name} on {interaction.guild.name}')

        source_language = self.lt_api.detect(message.content)[0]['language']
        target_language = TERRITORY_LANGUAGES.get(str(interaction.locale).split('-')[0].lower())[0]
        try:
            translated_source = self.lt_api.translate(message.content, source_language, target_language)
            await interaction.response.send_message(translated_source, ephemeral=True)
        except Exception:
            await interaction.response.send_message('> This translation is not supported', ephemeral=True)
            self.bot.logger.error(f'Invalid translation for locale ({str(interaction.locale), str(interaction.locale).split('-')[0].lower()}) and source ({source_language})')
