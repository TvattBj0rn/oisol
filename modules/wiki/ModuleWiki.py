import discord
import random
import re
from discord import app_commands
from discord.ext import commands
from typing import List
from modules.utils import ALL_WIKI_ENTRIES


class ModuleWiki(commands.Cog):
    def __init__(self, bot):
        self.oisol = bot

    async def wiki_autocomplete(
            self,
            interaction: discord.Interaction,
            current: str,
    ) -> List[app_commands.Choice[str]]:
        # TODO: STRIP ANY NON ALPHANUM
        # Default search values, before any input in the search bar
        if len(current) == 0:
            return [
                app_commands.Choice(name=wiki_entry['name'], value=wiki_entry['url'])
                for wiki_entry in random.choices(ALL_WIKI_ENTRIES, k=5)
            ]
        pattern = re.compile('[\\W_]+')
        current = pattern.sub(' ', current).lower().split()
        search_results = []
        for wiki_entry in ALL_WIKI_ENTRIES:
            search_value = 0
            for kw in current:
                if kw in wiki_entry['keywords']:
                    search_value += 1
            # We only want entries related to the search, 0 means nothing matched for a specific entry
            if search_value > 0:
                search_results.append((wiki_entry['name'], wiki_entry['url'], search_value))
        search_results = sorted(
            search_results,
            key=lambda x: x[2],
            reverse=True
        )[:25]
        return [
            app_commands.Choice(name=entry_result[0], value=entry_result[1])
            for entry_result in search_results
        ]

    @app_commands.command(name='wiki', description='Official wiki request')
    @app_commands.autocomplete(wiki_request=wiki_autocomplete)
    async def wiki(self, interaction: discord.Interaction, wiki_request: str):
        if not wiki_request.startswith('https://foxhole.wiki.gg/wiki/'):
            await interaction.response.send_message(f'The request you made was incorrect', ephemeral=True)
            return
        await interaction.response.send_message(f'You chose: {wiki_request}')
