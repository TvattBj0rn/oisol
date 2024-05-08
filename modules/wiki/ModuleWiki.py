import random
import discord
from typing import List
from discord import app_commands
from discord.ext import commands
from modules.utils import ALL_WIKI_ENTRIES


class ModuleWiki(commands.Cog):
    def __init__(self, bot):
        self.oisol = bot

    async def wiki_autocomplete(
            self,
            interaction: discord.Interaction,
            current: str,
    ) -> List[app_commands.Choice[str]]:

        # Default search values, before any input in the search bar
        if len(current) == 0:
            return [
                app_commands.Choice(name=wiki_entry['name'], value=wiki_entry['url'])
                for wiki_entry in random.choices(ALL_WIKI_ENTRIES, k=5)
            ]
        return [
            app_commands.Choice(name=wiki_entry['name'], value=wiki_entry['url'])
            for wiki_entry in ALL_WIKI_ENTRIES if current.lower() in wiki_entry['name'].lower()
        ]

    @app_commands.command(name='wiki', description='Official wiki request')
    @app_commands.autocomplete(wiki_request=wiki_autocomplete)
    async def wiki(self, interaction: discord.Interaction, wiki_request: str):
        await interaction.response.send_message(f'You chose: {wiki_request}')
