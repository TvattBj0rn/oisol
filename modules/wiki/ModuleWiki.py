import collections
from typing import Optional
import discord
import random
import re
from discord import app_commands
from discord.ext import commands
from modules.utils import (
    ALL_WIKI_ENTRIES,
    STRUCTURES_WIKI_ENTRIES,
    VEHICLES_WIKI_ENTRIES,
    EMOJIS_FROM_DICT,
    NAMES_TO_ACRONYMS
)
from modules.wiki.scrapers.scrap_wiki import scrap_wiki
from modules.wiki.scrapers.scrap_health import scrap_health, scrap_main_picture


class ModuleWiki(commands.Cog):
    def __init__(self, bot):
        self.oisol = bot

    @staticmethod
    def retrieve_facility_mats(resource_type: str, amount: str) -> str:
        if resource_type not in EMOJIS_FROM_DICT.keys():
            return f'{amount} **:** '

        if resource_type in NAMES_TO_ACRONYMS.keys():
            return f'\n{EMOJIS_FROM_DICT[resource_type]} **|** {NAMES_TO_ACRONYMS[resource_type]} **-** {amount}'
        return f'\n{EMOJIS_FROM_DICT[resource_type]} {amount}'

    @staticmethod
    def generate_hmtk_embed(wiki_data: dict, url_health: str, picture_url: Optional[str], color: Optional[int]) -> discord.Embed:
        embed_desc = ''
        if isinstance(wiki_data['HP'], dict):
            for k, v in wiki_data['HP'].items():
                embed_desc += f'{k}: {v} HP\n'
        else:
            embed_desc = f"{wiki_data['HP']} HP"
        embed = discord.Embed(
            title=wiki_data['Name'],
            url=url_health,
            description=embed_desc,
            color=color
        )
        if picture_url:
            embed.set_thumbnail(url=picture_url)
        if 'Class' in wiki_data.keys():
            embed.description += f"\n*Class: {wiki_data['Class']}*"

        for i, (k, v) in enumerate(wiki_data.items()):
            if k in ['Class', 'Name', '', 'Icon', 'HP']:
                continue
            value_string = f"{EMOJIS_FROM_DICT[k] if k in EMOJIS_FROM_DICT.keys() else k}: "
            if isinstance(wiki_data[k], dict) and 'disabled' in wiki_data[k].keys():
                value_string += wiki_data[k]['disabled'] + ' **|** ' + wiki_data[k]['kill']
            elif isinstance(wiki_data[k], dict) and len(wiki_data[k].keys()) == 3:
                value_string += wiki_data[k]['S'] + ' **|** ' + wiki_data[k]['M'] + ' **|** ' + wiki_data[k]['L']
            elif isinstance(wiki_data[k], str):
                value_string += wiki_data[k]
            embed.add_field(
                name='',
                value=value_string
            )
        return embed

    @staticmethod
    def generic_autocomplete(entries: list, current: str) -> list:
        # Default search values, before any input in the search bar
        if len(current) == 0:
            return [
                app_commands.Choice(name=wiki_entry['name'], value=wiki_entry['url'])
                for wiki_entry in random.choices(entries, k=5)
            ]
        pattern = re.compile('[\\W_]+')
        current = pattern.sub(' ', current).lower().split()
        search_results = []
        for wiki_entry in entries:
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

    def generate_wiki_embed(self, wiki_data: dict) -> discord.Embed:
        print(wiki_data)
        embed = discord.Embed(
            title=wiki_data['title'],
            description=f"*{wiki_data['description']}*" if wiki_data['description'] else None,
            url=wiki_data['url'],
            color=wiki_data['color']
        )
        embed.set_image(url=wiki_data['img_url'])
        for attribute_key, attribute_value in wiki_data.items():
            if attribute_key in ['description', 'url', 'title', 'img_url', 'Fuel Capacity', 'color']:
                continue
            if isinstance(attribute_value, str):
                embed.add_field(name=attribute_key, value=attribute_value)
            else:
                attribute_string = ''
                ordered_attribute_value = collections.OrderedDict(sorted(attribute_value.items()))
                for k, v in ordered_attribute_value.items():
                    attribute_string += self.retrieve_facility_mats(k, v)
                attribute_string = attribute_string.removesuffix(' **:** ')
                embed.add_field(name=attribute_key, value=attribute_string)
        if 'Fuel Capacity' in wiki_data.keys():
            embed.add_field(
                name='Fuel Capacity',
                value=f"{wiki_data['Fuel Capacity']['']} {' **|** '.join(EMOJIS_FROM_DICT[k] for k in wiki_data['Fuel Capacity'] if k in EMOJIS_FROM_DICT.keys())}"
            )
        return embed

    async def wiki_autocomplete(self, interaction: discord.Interaction, current: str) -> list:
        return self.generic_autocomplete(ALL_WIKI_ENTRIES, current)

    async def health_autocomplete(self, interaction: discord.Interaction, current: str) -> list:
        return self.generic_autocomplete(STRUCTURES_WIKI_ENTRIES + VEHICLES_WIKI_ENTRIES, current)

    @app_commands.command(name='wiki', description='Info wiki')
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

    @app_commands.command(name='health', description='Structures / Vehicles health')
    @app_commands.autocomplete(wiki_request=health_autocomplete)
    async def entities_health(self, interaction: discord.Interaction, wiki_request: str, visible: bool = False):
        if not wiki_request.startswith('https://foxhole.wiki.gg/wiki/'):
            await interaction.response.send_message(f'The request you made was incorrect', ephemeral=True)
            return
        entry_url = 'https://foxhole.wiki.gg/wiki/Vehicle_Health'
        for entry in STRUCTURES_WIKI_ENTRIES:
            if entry['url'] == wiki_request:
                entry_url = 'https://foxhole.wiki.gg/wiki/Structure_Health'
                break
        wiki_entry_complete_name = ''
        for entry in ALL_WIKI_ENTRIES:
            if entry['url'] == wiki_request:
                wiki_entry_complete_name = entry['name']
                break
        if wiki_entry_complete_name.startswith(('Bunker Base', 'Safe House', 'Town Base')) and wiki_entry_complete_name.endswith('(Tier 1)'):
            wiki_entry_complete_name = wiki_entry_complete_name.removesuffix(' (Tier 1)')
        infobox_tuple = scrap_main_picture(wiki_request, wiki_entry_complete_name)
        entry_picture_url, color = None, None
        if infobox_tuple:
            entry_picture_url, color = infobox_tuple
        entry_embed = self.generate_hmtk_embed(scrap_health(entry_url, wiki_entry_complete_name), entry_url, entry_picture_url, color)
        await interaction.response.send_message(embed=entry_embed, ephemeral=not visible)
