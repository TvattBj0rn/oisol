from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from libretranslatepy import LibreTranslateAPI


if TYPE_CHECKING:
    from main import Oisol

ALPHABET_CONVERTOR = {
    '🇦': 'a', '🇧': 'b', '🇨': 'c', '🇩': 'd', '🇪': 'e', '🇫': 'f', '🇬': 'g', '🇭': 'h', '🇮': 'i', '🇯': 'j', '🇰': 'k',
    '🇱': 'l', '🇲': 'm', '🇳': 'n','🇴': 'o', '🇵': 'p', '🇶': 'q', '🇷': 'r', '🇸': 's', '🇹': 't', '🇺': 'u', '🇻': 'v',
    '🇼': 'w', '🇽': 'x','🇾': 'y', '🇿': 'z',
}


class ModuleTranslation(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot
        self.lt_api = LibreTranslateAPI('http://127.0.0.1:5000')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        target_language_code = ''.join(ALPHABET_CONVERTOR.get(c, '') for c in reaction.emoji)
        all_available_languages = (language['code'] for language in self.lt_api.languages())

        if target_language_code in all_available_languages:
            self.bot.logger.command(f'translation reaction by {user.name} on {reaction.message.guild.name}')
            source_language = self.lt_api.detect(reaction.message.content)[0]['language']
            translated_source = self.lt_api.translate(reaction.message.content, source_language, target_language_code)
            await reaction.message.channel.send(translated_source, silent=True, reference=reaction.message)
