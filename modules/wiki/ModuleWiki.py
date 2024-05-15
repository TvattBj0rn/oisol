import discord
import random
import re
from discord import app_commands
from discord.ext import commands
from typing import List
from modules.utils import ALL_WIKI_ENTRIES, EMOJIS_FROM_DICT
from modules.wiki.scraper.scrap_wiki import scrap_wiki


class ModuleWiki(commands.Cog):
    def __init__(self, bot):
        self.oisol = bot

    @staticmethod
    def generate_wiki_embed(wiki_data: dict) -> discord.Embed:
        print(wiki_data)
        embed = discord.Embed(
            title=wiki_data['title'],
            description=f"*{wiki_data['description']}*" if wiki_data['description'] else None,
            url=wiki_data['url']
        )
        embed.set_image(url=wiki_data['img_url'])
        for attribute_key, attribute_value in wiki_data.items():
            if attribute_key in ['description', 'url', 'title', 'img_url', 'Fuel Capacity']:
                continue
            if isinstance(attribute_value, str):
                embed.add_field(name=attribute_key, value=attribute_value)
            else:
                attribute_string = ''
                for k, v in attribute_value.items():
                    attribute_string += f'\n{EMOJIS_FROM_DICT[k]} {v}' if k in EMOJIS_FROM_DICT.keys() else f'{v} **:** '
                attribute_string = attribute_string.removesuffix(' **:** ')
                embed.add_field(name=attribute_key, value=attribute_string)
        if 'Fuel Capacity' in wiki_data.keys():
            embed.add_field(
                name='Fuel Capacity',
                value=f"{wiki_data['Fuel Capacity']['']} {' **|** '.join(EMOJIS_FROM_DICT[k] for k in wiki_data['Fuel Capacity'] if k in EMOJIS_FROM_DICT.keys())}"
            )
        return embed

    async def wiki_autocomplete(
            self,
            interaction: discord.Interaction,
            current: str,
    ):
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
    async def wiki(self, interaction: discord.Interaction, wiki_request: str, visible: bool = False):
        if not wiki_request.startswith('https://foxhole.wiki.gg/wiki/'):
            await interaction.response.send_message(f'The request you made was incorrect', ephemeral=True)
            return
        wiki_entry_complete_name = ''
        for entry in ALL_WIKI_ENTRIES:
            if entry['url'] == wiki_request:
                wiki_entry_complete_name = entry['name']
                break

        entry_data = scrap_wiki(wiki_request, wiki_entry_complete_name)
        entry_data['url'] = wiki_request
        entry_embed = self.generate_wiki_embed(entry_data)

        await interaction.response.send_message(embed=entry_embed, ephemeral=not visible)
