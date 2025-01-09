import collections
import logging
import operator
import random

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import (
    ALL_WIKI_ENTRIES,
    EMOJIS_FROM_DICT,
    NAMES_TO_ACRONYMS,
    STRUCTURES_WIKI_ENTRIES,
    VEHICLES_WIKI_ENTRIES,
)

from .scrapers.scrap_wiki_entry_health import scrap_health
from .scrapers.scrap_wiki_entry_infobox import scrap_wiki


class ModuleWiki(commands.Cog):
    def __init__(self, bot: commands.Bot):
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
    ) -> discord.Embed:
        # Embed description
        embed_desc = ''
        # Display each tier health's when dict
        if isinstance(wiki_data['HP'], dict):
            for k, v in wiki_data['HP'].items():
                embed_desc += f'{k}: {v} HP\n'
        else:
            embed_desc = f"{wiki_data['HP']} HP"

        if 'Class' in wiki_data:
            embed_desc += f"\n*Class: {wiki_data['Class']}*"

        fields = []
        for damage_type, weapons in wiki_data['Damage'].items():
            value_string = ''
            for weapon_name, weapon_value in weapons.items():
                value_string += f'{EMOJIS_FROM_DICT.get(weapon_name, weapon_name)}: '
                if isinstance(weapon_value, dict) and 'Disabled' in weapon_value:
                    value_string += f'{weapon_value['Disabled']} **|** {weapon_value['Kill']}'
                elif isinstance(weapon_value, dict) and len(weapon_value.keys()) == 3:
                    value_string += f'{weapon_value['S']} **|** {weapon_value['M']} **|** {weapon_value['L']}'
                elif isinstance(weapon_value, str):
                    value_string += weapon_value
                if len(value_string) + 15 >= 300:
                    value_string += '\n'
                # Add separator chars for better readability
                value_string += '   '
            fields.append({'name': f'{damage_type.upper()} ({EMOJIS_FROM_DICT[damage_type]})', 'value': value_string})

        return discord.Embed().from_dict(
            {
                'title': wiki_data['Name'],
                'url': url_health,
                'description': embed_desc,
                'color': wiki_data['Color'],
                'thumbnail': {'url': wiki_data['img_url']},
                'fields': fields,
            },
        )

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
                    'inline': True,
                },
            )
        return discord.Embed().from_dict(
            {
                'title': wiki_data['title'],
                'description': f"*{wiki_data['description']}*" if wiki_data['description'] else None,
                'url': wiki_data['url'],
                'color': wiki_data['color'],
                'image': {'url': wiki_data['img_url']},
                'fields': embed_fields,
            },
        )

    @app_commands.command(name='wiki', description='Get a wiki infobox')
    async def wiki(self, interaction: discord.Interaction, search_request: str, visible: bool = False) -> None:
        logging.info(f'[COMMAND] wiki command by {interaction.user.name} on {interaction.guild.name}')
        if not search_request.startswith('https://foxhole.wiki.gg/wiki/'):
            await interaction.response.send_message('> The request you made was incorrect', ephemeral=True)
            # In case the user provided an url that is not from the official wiki
            if search_request.startswith(('https://', 'http://')) and not search_request.startswith('https://foxhole.wiki.gg'):
                logging.warning(f'{interaction.user.name} provided a suspicious URL in {interaction.guild.name} ({search_request})')
            return

        entry_name = next((entry['name'] for entry in ALL_WIKI_ENTRIES if entry['url'] == search_request), '')
        entry_data = scrap_wiki(search_request, entry_name)
        entry_data['url'] = search_request

        if 'title' not in entry_data:
            await interaction.response.send_message('> Unexpected error, most likely due to a url change not yet implemented on the bot side. Please report this error to @vaskbjorn !', ephemeral=True)
            logging.warning(f'Entry URL failing: {search_request, entry_name}')
            return

        entry_embed = self.generate_wiki_embed(entry_data)

        await interaction.response.send_message(embed=entry_embed, ephemeral=not visible)

    @app_commands.command(name='health', description='Structures / Vehicles health')
    async def entities_health(self, interaction: discord.Interaction, search_request: str, visible: bool = False) -> None:
        logging.info(f'[COMMAND] health command by {interaction.user.name} on {interaction.guild.name}')

        entry_searches = (
            next((('https://foxhole.wiki.gg/wiki/Structure_Health', entry['name']) for entry in STRUCTURES_WIKI_ENTRIES if entry['url'] == search_request), None),
            next((('https://foxhole.wiki.gg/wiki/Vehicle_Health', entry['name']) for entry in VEHICLES_WIKI_ENTRIES if entry['url'] == search_request), None),
        )
        if not any(entry_searches):
            await interaction.response.send_message('> The request you made was incorrect', ephemeral=True)
            # In case the user provided an url that is not from the official wiki
            if search_request.startswith(('https://', 'http://')) and not search_request.startswith('https://foxhole.wiki.gg'):
                logging.warning(f'{interaction.user.name} provided a suspicious URL in {interaction.guild.name} ({search_request})')
            return

        entry_url, entry_name = entry_searches[0] if entry_searches[0] is not None else entry_searches[1]
        if (
                entry_name.startswith(('Bunker Base', 'Safe House', 'Town Base', 'Medical Room'))
                and entry_name.endswith('(Tier 1)')
        ):
            entry_name = entry_name.removesuffix(' (Tier 1)')

        scraped_health_data = scrap_health(entry_url, entry_name)
        if 'Name' not in scraped_health_data:
            await interaction.response.send_message('> Unexpected error, most likely due to a url change not yet implemented on the bot side. Please report this error to @vaskbjorn !', ephemeral=True)
            logging.warning(f'Entry URL failing: {entry_url, entry_name}')
            return

        await interaction.response.send_message(embed=self.generate_hmtk_embed(scraped_health_data, entry_url), ephemeral=not visible)

    @app_commands.command(name='production', description='Get production costs, location & time from the wiki')
    async def get_item_production_parameters(self, interaction: discord.Interaction, search_request: str, visible: bool = False) -> None:
        logging.info(f'[COMMAND] production command by {interaction.user.name} on {interaction.guild.name}')
        if not search_request.startswith('https://foxhole.wiki.gg/wiki/'):
            await interaction.response.send_message('> The request you made was incorrect', ephemeral=True)
            # In case the user provided an url that is not from the official wiki
            if search_request.startswith(('https://', 'http://')) and not search_request.startswith('https://foxhole.wiki.gg'):
                logging.warning(f'{interaction.user.name} provided a suspicious URL in {interaction.guild.name} ({search_request})')
            return
        entry_name = next((entry['name'] for entry in ALL_WIKI_ENTRIES if entry['url'] == search_request), '')




    ## Search bar autocompletes
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

        # Get number of matched keywords for each entry
        search_results = []
        for wiki_entry in entries:
            search_value = 0
            for kw in current:
                if kw in wiki_entry['keywords']:
                    search_value += 1
            # We only want entries related to the search, 0 means nothing matched for a specific entry
            if search_value:
                search_results.append((wiki_entry['name'], wiki_entry['url'], search_value))

        # Sort by descending order to get searches with more value first
        search_results = sorted(search_results, key=operator.itemgetter(2), reverse=True)[:25]

        return [(entry_result[0], entry_result[1]) for entry_result in search_results]

    # used in wiki & production commands
    @wiki.autocomplete('search_request')
    @get_item_production_parameters.autocomplete('search_request')
    async def all_autocomplete(self, _interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        choice_list = self.generic_autocomplete(ALL_WIKI_ENTRIES, current)
        return [app_commands.Choice(name=entry[0], value=entry[1]) for entry in choice_list]

    # used in health command
    @entities_health.autocomplete('search_request')
    async def structures_vehicles_autocomplete(self, _interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        choice_list = self.generic_autocomplete(STRUCTURES_WIKI_ENTRIES + VEHICLES_WIKI_ENTRIES, current)
        return [app_commands.Choice(name=entry[0], value=entry[1]) for entry in choice_list]
