import collections
import logging
import operator
import random

import discord
from discord import app_commands
from discord.ext import commands

from src.modules.wiki.scrapers.scrap_health import scrap_health, scrap_main_picture
from src.modules.wiki.scrapers.scrap_wiki import scrap_wiki
from src.utils.resources import (
    ALL_WIKI_ENTRIES,
    EMOJIS_FROM_DICT,
    NAMES_TO_ACRONYMS,
    STRUCTURES_WIKI_ENTRIES,
    VEHICLES_WIKI_ENTRIES,
)


class ModuleWiki(commands.Cog):
    def __init__(self, bot):
        self.oisol = bot

    @staticmethod
    def retrieve_facility_mats(resource_type: str, amount: str) -> str:
        if resource_type not in EMOJIS_FROM_DICT:
            return f'{amount} **:** '

        if resource_type in NAMES_TO_ACRONYMS:
            return f'\n{EMOJIS_FROM_DICT[resource_type]} **|** {NAMES_TO_ACRONYMS[resource_type]} **-** {amount}'
        return f'\n{EMOJIS_FROM_DICT[resource_type]} {amount}'

    @staticmethod
    def generate_hmtk_embed(
            wiki_data: dict,
            url_health: str,
            picture_url: str,
            color: int
    ) -> discord.Embed:
        embed_desc = ''
        if isinstance(wiki_data['HP'], dict):
            for k, v in wiki_data['HP'].items():
                embed_desc += f'{k}: {v} HP\n'
        else:
            embed_desc = f"{wiki_data['HP']} HP"
        if 'Class' in wiki_data:
            embed_desc += f"\n*Class: {wiki_data['Class']}*"
        embed = discord.Embed().from_dict(
            {
                'title': wiki_data['Name'],
                'url': url_health,
                'description': embed_desc,
                'color': color,
                'thumbnail': {'url': picture_url}
            }
        )

        # For relic vehicles, there are more available entries on the wiki, causing embed fields to be > 25.
        # This set the relic vehicles entries to the same level as normal vehicles.
        if 'Class' in wiki_data and wiki_data['Class'] == 'Relic Vehicles':
            for entry in ['Alligator Charge', "Hydra's Whisper", 'Havoc Charge', 'Sea Mine', 'Torpedo','Sea Mine']:
                wiki_data.pop(entry, None)

        for k, v in wiki_data.items():
            if k in {'Class', 'Name', '', 'Icon', 'HP'}:
                continue
            value_string = f"{EMOJIS_FROM_DICT.get(k, k)}: "
            if isinstance(v, dict) and 'Disabled' in v:
                value_string += f'{v['Disabled']} **|** {v['Kill']}'
            elif isinstance(v, dict) and len(v.keys()) == 3:
                value_string += f'{v['S']} **|** {v['M']} **|** {v['L']}'
            elif isinstance(v, str):
                value_string += v
            embed.add_field(
                name='',
                value=value_string
            )
        return embed

    @staticmethod
    def generic_autocomplete(entries: list, current: str) -> list:
        """
        Method to generate search suggestions to the user
        :param entries: List of wiki entries to use (differing between health and wiki)
        :param current: Current input given by the user
        :return: List of the best suggestions for the user
        """
        # Default search values, before any input in the search bar
        if not current:
            return [(wiki_entry['name'], wiki_entry['url']) for wiki_entry in random.choices(entries, k=5)]

        # Tokenize user input
        current = current.strip().lower().split()

        # If at least one keyword matches, the entry information are saved
        search_results = [(wiki_entry['name'], wiki_entry['url'], search_value) for wiki_entry in entries if (search_value := sum(wiki_entry['keywords'].count(kw) for kw in current))]

        # Sort by search values & get higher values at the bottom of the list in reverse order
        search_results = sorted(search_results, key=operator.itemgetter(2))[:-25:-1]

        return [(entry_result[0], entry_result[1]) for entry_result in search_results]

    def generate_wiki_embed(self, wiki_data: dict) -> discord.Embed:
        embed_fields = []
        for attribute_key, attribute_value in wiki_data.items():
            if attribute_key in {'description', 'url', 'title', 'img_url', 'Fuel Capacity', 'color'}:
                continue
            if isinstance(attribute_value, str):
                embed_fields.append({'name': attribute_key, 'value': attribute_value, 'inline': True})
            else:
                attribute_string = ''
                ordered_attribute_value = collections.OrderedDict(sorted(attribute_value.items()))
                for k, v in ordered_attribute_value.items():
                    attribute_string += self.retrieve_facility_mats(k, v)
                attribute_string = attribute_string.removesuffix(' **:** ')
                embed_fields.append({'name': attribute_key, 'value': attribute_string, 'inline': True})
        if 'Fuel Capacity' in wiki_data:
            embed_fields.append(
                {
                    'name': 'Fuel Capacity',
                    'value': f"{wiki_data['Fuel Capacity']['']} {(' **|** '.join(EMOJIS_FROM_DICT[k] for k in wiki_data['Fuel Capacity'] if k in EMOJIS_FROM_DICT))}",
                    'inline': True
                }
            )
        return discord.Embed().from_dict(
            {
                'title': wiki_data['title'],
                'description': f"*{wiki_data['description']}*" if wiki_data['description'] else None,
                'url': wiki_data['url'],
                'color': wiki_data['color'],
                'image': {'url': wiki_data['img_url']},
                'fields': embed_fields
            }
        )

    @app_commands.command(name='wiki', description='Get a wiki infobox')
    async def wiki(self, interaction: discord.Interaction, wiki_search_request: str, visible: bool = False):
        logging.info(f'> wiki command by {interaction.user.name} on {interaction.guild.name} ({wiki_search_request})')
        if not wiki_search_request.startswith('https://foxhole.wiki.gg/wiki/'):
            await interaction.response.send_message('> The request you made was incorrect', ephemeral=True)
            # In case the user provided an url that is not from the official wiki
            if wiki_search_request.startswith(('https://', 'http://')) and not wiki_search_request.startswith('https://foxhole.wiki.gg'):
                logging.warning(f'{interaction.user.name} provided a suspicious URL to the /health command in {interaction.guild.name} ({wiki_search_request})')
            return

        entry_name = next((entry['name'] for entry in ALL_WIKI_ENTRIES if entry['url'] == wiki_search_request), '')
        entry_data = scrap_wiki(wiki_search_request, entry_name)
        entry_data['url'] = wiki_search_request

        if 'title' not in entry_data:
            await interaction.response.send_message('> Unexpected error, most likely due to a url change not yet implemented on the bot side. Please report this error to @vaskbjorn !', ephemeral=True)
            logging.warning(f'Entry URL failing: {wiki_search_request, entry_name}')
            return

        entry_embed = self.generate_wiki_embed(entry_data)

        await interaction.response.send_message(embed=entry_embed, ephemeral=not visible)

    @wiki.autocomplete('wiki_search_request')
    async def wiki_autocomplete(self, _interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        choice_list = self.generic_autocomplete(ALL_WIKI_ENTRIES, current)
        return [app_commands.Choice(name=entry[0], value=entry[1]) for entry in choice_list]

    @app_commands.command(name='health', description='Structures / Vehicles health')
    async def entities_health(self, interaction: discord.Interaction, health_search_request: str, visible: bool = False):
        logging.info(f'[COMMAND] health command by {interaction.user.name} on {interaction.guild.name}')

        entry_searches = (
            next((('https://foxhole.wiki.gg/wiki/Structure_Health', entry['name']) for entry in STRUCTURES_WIKI_ENTRIES if entry['url'] == health_search_request), None),
            next((('https://foxhole.wiki.gg/wiki/Vehicle_Health', entry['name']) for entry in VEHICLES_WIKI_ENTRIES if entry['url'] == health_search_request), None)
        )
        if not any(entry_searches):
            await interaction.response.send_message('> The request you made was incorrect', ephemeral=True)
            # In case the user provided an url that is not from the official wiki
            if health_search_request.startswith(('https://', 'http://')) and not health_search_request.startswith('https://foxhole.wiki.gg'):
                logging.warning(f'{interaction.user.name} provided a suspicious URL to the /health command in {interaction.guild.name} ({health_search_request})')
            return

        entry_url, entry_name = entry_searches[0] if entry_searches[0] is not None else entry_searches[1]
        if (
                entry_name.startswith(('Bunker Base', 'Safe House', 'Town Base'))
                and entry_name.endswith('(Tier 1)')
        ):
            entry_name = entry_name.removesuffix(' (Tier 1)')
        infobox_tuple = scrap_main_picture(health_search_request, entry_name)

        if not all(infobox_tuple):
            await interaction.response.send_message(embed=discord.Embed(), ephemeral=not visible)
            return

        scraped_health_data = scrap_health(entry_url, entry_name)
        if 'Name' not in scraped_health_data:
            await interaction.response.send_message('> Unexpected error, most likely due to a url change not yet implemented on the bot side. Please report this error to @vaskbjorn !', ephemeral=True)
            logging.warning(f'Entry URL failing: {entry_url, entry_name}')
            return

        entry_embed = self.generate_hmtk_embed(
            scraped_health_data,
            entry_url,
            infobox_tuple[0],
            infobox_tuple[1]
        )
        await interaction.response.send_message(embed=entry_embed, ephemeral=not visible)

    @entities_health.autocomplete('health_search_request')
    async def health_autocomplete(self, _interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        choice_list = self.generic_autocomplete(STRUCTURES_WIKI_ENTRIES + VEHICLES_WIKI_ENTRIES, current)
        return [app_commands.Choice(name=entry[0], value=entry[1]) for entry in choice_list]
