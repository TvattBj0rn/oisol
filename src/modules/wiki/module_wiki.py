from __future__ import annotations

import math
import operator
import random
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import (
    ALL_WIKI_ENTRIES,
    EMOJIS_FROM_DICT,
    PRODUCTION_ENTRIES,
    RESOURCE_TO_CRATE,
    STRUCTURES_WIKI_ENTRIES,
    VEHICLES_WIKI_ENTRIES,
)

from .mpf_generation import generate_mpf_data
from .scrapers.scrap_wiki_entry_health import scrap_health
from .scrapers.scrap_wiki_entry_production import scrap_production
from .templated_dicts import WikiTemplateFactory
from .wiki_api_requester import get_entry_attributes

if TYPE_CHECKING:
    from main import Oisol


class ModuleWiki(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot

    @staticmethod
    def generate_hmtk_embed(
            wiki_data: dict,
            url_health: str,
    ) -> discord.Embed:
        # Display each tier health's when dict
        embed_desc = ''.join(f'{k}: {v} Health\n' for k, v in wiki_data['Health'].items()) if isinstance(wiki_data['Health'], dict) else f"{wiki_data['Health']} Health"

        if 'Class' in wiki_data:
            embed_desc += f"\n*Class: {wiki_data['Class']}*"

        fields = []
        for damage_type, weapons in wiki_data['Damage'].items():
            value_string = ''
            for i, (weapon_name, weapon_value) in enumerate(weapons.items()):
                value_string += f'{EMOJIS_FROM_DICT.get(weapon_name, weapon_name)}: '
                if isinstance(weapon_value, dict) and 'Disabled' in weapon_value:
                    value_string += f'{weapon_value['Disabled']} **|** {weapon_value['Kill']}'
                elif isinstance(weapon_value, dict) and len(weapon_value.keys()) == 3:
                    value_string += f'{weapon_value['S']} **|** {weapon_value['M']} **|** {weapon_value['L']}'
                elif isinstance(weapon_value, str):
                    value_string += weapon_value
                value_string += '\n' if i and not i % 3 else '   '
            fields.append({'name': f'{damage_type.upper()} ({EMOJIS_FROM_DICT[damage_type]})', 'value': f'{value_string[:-1]}\n‎'})
        fields[-1]['value'] = fields[-1]['value'][:-1]

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

    @staticmethod
    def generate_production_embed(wiki_data: dict) -> list[discord.Embed]:
        row_number = len(wiki_data['Structure'])  # All table related column have equal length
        embed_fields = []
        for i in range(row_number):
            for k in ['Structure', 'Input(s)', 'Output']:
                if isinstance(wiki_data[k][i], tuple):  # Structure
                    value = ' '.join(wiki_data[k][i])
                else:  # Input(s) / Output
                    value = '\n- '.join(' '.join(j) for j in wiki_data[k][i])
                embed_fields.append({'name': k, 'value': f'- {value}', 'inline': True})

        generated_embeds = [discord.Embed().from_dict({
            'title': wiki_data['name'],
            'url': wiki_data['url'],
            'thumbnail': wiki_data['thumbnail'],
            'color': wiki_data['color'],
            'fields': embed_fields,
        })]

        if 'mpf_data' in wiki_data:
            # Iterate over MPF slots (5 or 9)
            mpf_fields = [{
                    'name': f'{i + 1} {EMOJIS_FROM_DICT.get('Crate', 'Crate')}',
                    'value': '\n'.join(f'- x{f'{math.ceil(v[i] / RESOURCE_TO_CRATE.get(k, 1))} crates of '} {k} {EMOJIS_FROM_DICT.get(k, '')} *({v[i]})*' for k, v in wiki_data['mpf_data'].items()),
                    'inline': True,
                } for i in range(len(wiki_data['mpf_data'][next(iter(wiki_data['mpf_data']))]))
            ]

            generated_embeds.append(discord.Embed().from_dict({
                'title': 'MPF Stats',
                'url': 'https://foxhole.wiki.gg/wiki/Mass_Production_Factory',
                'thumbnail': {'url': 'https://foxhole.wiki.gg/images/e/eb/MapIconMassProductionFactory.png'},
                'color': wiki_data['color'],
                'fields': mpf_fields,
            }))
        return generated_embeds

    @app_commands.command(name='wiki', description='Get a wiki infobox')
    async def wiki(self, interaction: discord.Interaction, search_request: str, visible: bool = False) -> None:
        self.bot.logger.command(f'wiki command by {interaction.user.name} on {interaction.guild.name}')
        if not search_request.startswith('https://foxhole.wiki.gg/wiki/'):
            await interaction.response.send_message('> The request you made was incorrect', ephemeral=True)
            # In case the user provided a url that is not from the official wiki
            if search_request.startswith(('https://', 'http://')) and not search_request.startswith('https://foxhole.wiki.gg'):
                self.bot.logger.warning(f'{interaction.user.name} provided a suspicious URL in {interaction.guild.name} ({search_request})')
            return

        entry: dict = next((entry for entry in ALL_WIKI_ENTRIES if entry['url'] == search_request), '')

        data_dict = await get_entry_attributes(entry['name'], entry['wiki_table'].value)

        embeded_data = WikiTemplateFactory(data_dict).get(entry['wiki_table']).generate_embed_data()

        await interaction.response.send_message(embed=discord.Embed().from_dict(embeded_data), ephemeral=not visible)

    @app_commands.command(name='health', description='Structures / Vehicles health')
    async def entities_health(self, interaction: discord.Interaction, search_request: str, visible: bool = False) -> None:
        self.bot.logger.command(f'health command by {interaction.user.name} on {interaction.guild.name}')

        entry_searches = (
            next((('https://foxhole.wiki.gg/wiki/Structure_Health', entry['name']) for entry in STRUCTURES_WIKI_ENTRIES if entry['url'] == search_request), None),
            next((('https://foxhole.wiki.gg/wiki/Vehicle_Health', entry['name']) for entry in VEHICLES_WIKI_ENTRIES if entry['url'] == search_request), None),
        )
        if not any(entry_searches):
            await interaction.response.send_message('> The request you made was incorrect', ephemeral=True)
            # In case the user provided a url that is not from the official wiki
            if search_request.startswith(('https://', 'http://')) and not search_request.startswith('https://foxhole.wiki.gg'):
                self.bot.logger.warning(f'{interaction.user.name} provided a suspicious URL in {interaction.guild.name} ({search_request})')
            return

        entry_url, entry_name = entry_searches[0] if entry_searches[0] is not None else entry_searches[1]
        scraped_health_data = scrap_health(entry_url, entry_name)
        if 'Name' not in scraped_health_data:
            await interaction.response.send_message('> Unexpected error, most likely due to a url change not yet implemented on the bot side. Please report this error to @vaskbjorn !', ephemeral=True)
            self.bot.logger.warning(f'Entry URL failing: {entry_url, entry_name}')
            return

        await interaction.response.send_message(embed=self.generate_hmtk_embed(scraped_health_data, entry_url), ephemeral=not visible)

    @app_commands.command(name='production', description='Get production costs, location & time from the wiki')
    async def get_item_production_parameters(self, interaction: discord.Interaction, search_request: str, visible: bool = False) -> None:
        self.bot.logger.command(f'production command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.send_message('> This command is currently being reworked and will not be available for some time', ephemeral=True)
        return
        if not search_request.startswith('https://foxhole.wiki.gg/wiki/'):
            await interaction.response.send_message('> The request you made was incorrect', ephemeral=True)
            # In case the user provided an url that is not from the official wiki
            if search_request.startswith(('https://', 'http://')) and not search_request.startswith('https://foxhole.wiki.gg'):
                self.bot.logger.warning(f'{interaction.user.name} provided a suspicious URL in {interaction.guild.name} ({search_request})')
            return

        # Get costs info from the wiki
        scraped_production_data = scrap_production(search_request)

        # Get correct entry name & url
        scraped_production_data['name'] = next((entry['name'] for entry in ALL_WIKI_ENTRIES if entry['url'] == search_request), '')
        scraped_production_data['url'] = search_request

        # If any entry refers to the MPF in the wiki, a new key is added with the calculated MPF data
        if any(tup for tup in scraped_production_data['Structure'] if tup[0] == 'Mass Production Factory'):
            # For vehicles and structures, the maximum slots of mpf is 5 instead of 9
            is_short_mpf = any(tup for tup in scraped_production_data['Structure'] if tup[0] in {'Garage', 'Shipyard', 'Construction Yard', 'Home Base'})

            # The input is a flattened tuple without the emojis
            scraped_production_data['mpf_data'] = generate_mpf_data(list(sum(scraped_production_data['Input(s)'][next(i for i, (v, *_) in enumerate(scraped_production_data['Structure']) if v == 'Mass Production Factory')], ()))[::2], is_short_mpf)

        await interaction.response.send_message(embeds=self.generate_production_embed(scraped_production_data), ephemeral=not visible)

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

    # used in wiki commands
    @wiki.autocomplete('search_request')
    async def all_autocomplete(self, _interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        choice_list = self.generic_autocomplete(ALL_WIKI_ENTRIES, current)
        return [app_commands.Choice(name=entry[0], value=entry[1]) for entry in choice_list]

    # used in health command
    @entities_health.autocomplete('search_request')
    async def structures_vehicles_autocomplete(self, _interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        choice_list = self.generic_autocomplete(STRUCTURES_WIKI_ENTRIES + VEHICLES_WIKI_ENTRIES, current)
        return [app_commands.Choice(name=entry[0], value=entry[1]) for entry in choice_list]

    # used in production command
    @get_item_production_parameters.autocomplete('search_request')
    async def items_vehicles_autocomplete(self, _interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        choice_list = self.generic_autocomplete(PRODUCTION_ENTRIES, current)
        return [app_commands.Choice(name=entry[0], value=entry[1]) for entry in choice_list]
