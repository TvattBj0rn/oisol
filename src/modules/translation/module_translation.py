from __future__ import annotations

import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands, InteractionCallbackResponse
from discord.ext import commands
from libretranslatepy import LibreTranslateAPI

from src.utils.languages_per_country import TERRITORY_LANGUAGES

if TYPE_CHECKING:
    from main import Oisol


DISCORD_MESSAGE_MAX_LENGTH = 2000


class ModuleTranslation(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot
        self.lt_api = LibreTranslateAPI(os.getenv('LIBRETRANSLATE_API_IP'))
        self.bot.tree.add_command(
            app_commands.ContextMenu(
                name=app_commands.locale_str('Translate'),
                callback=self.translate_to_user_language,
            ),
        )

    @staticmethod
    def __split_into_discord_message_length(source: str) -> list[str]:
        """
        Discord bot messages can only be 2000 chars long, while nitro users can post up to 4000 chars messages.
        This method split any message longer than 2000 into chunks of closest space char below 2000 char.
        :param source: translated message with more than 2000 chars
        :return: list of subtexts of source with less than 2000 chars each
        """
        source_results = []
        result = ''
        for word in source.split(' '):
            if len(result) + len(f'{word} ') >= DISCORD_MESSAGE_MAX_LENGTH:
                source_results.append(result)
                result = f'{word} '
            else:
                result += f'{word} '

        # Ensure the final text is properly registered
        source_results.append(result)

        return source_results

    async def translate_to_user_language(self, interaction: discord.Interaction, message: discord.Message) -> None:
        self.bot.logger.command(f'translate command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.defer(ephemeral=True)

        if not message.content:
            await interaction.followup.send('> The bot can only translate text messages')
            return

        source_language = self.lt_api.detect(message.content)[0]['language']
        target_language = TERRITORY_LANGUAGES.get(str(interaction.locale).split('-')[0].lower())[0]

        try:
            translated_source = self.lt_api.translate(message.content, source_language, target_language)
        except Exception:
            await interaction.followup.send('> This translation is not supported', ephemeral=True)
            self.bot.logger.error(f'Invalid translation for locale ({str(interaction.locale), str(interaction.locale).split('-')[0].lower()}) and source ({source_language})')
            return

        channel = await interaction.user.create_dm() if not interaction.app_permissions.send_messages else None

        if len(translated_source) < DISCORD_MESSAGE_MAX_LENGTH:
            if channel is not None:
                await channel.send(translated_source)
            else:
                await interaction.followup.send(translated_source, ephemeral=True)
            return

        for msg in self.__split_into_discord_message_length(translated_source):
            if channel is not None:
                await channel.send(translated_source)
            else:
                await interaction.followup.send(msg, ephemeral=True)
