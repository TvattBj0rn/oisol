from __future__ import annotations

import configparser
import operator
import random
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import (
    ALL_WIKI_ENTRIES, REGIONS_TYPES, OISOL_HOME_PATH, DataFilesPath, CacheKeys, WikiTables
)
from .health_embed_template import HealthEntryEngine

from .wiki_embeds_templates import WikiTemplateFactory
from .wiki_api_requester import get_entry_attributes
from ...utils.foxhole_wiki_api_handler import FoxholeWikiAPIWrapper

if TYPE_CHECKING:
    from main import Oisol


class ModuleWiki(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot

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

    async def _return_unexpected_error(self, interaction: discord.Interaction, entry_error: str):
        await interaction.response.send_message(
            '> Unexpected error, most likely due to a url change not yet implemented on the bot side. Please report this error to @vaskbjorn !',
            ephemeral=True)
        self.bot.logger.warning(f'Entry URL failing: {entry_error}')

    @app_commands.command(name='health', description='Structures / Vehicles health')
    async def entities_health(self, interaction: discord.Interaction, search_request: str, visible: bool = False) -> None:
        self.bot.logger.command(f'health command by {interaction.user.name} on {interaction.guild.name}')

        # Fields required for health process for the two available tables
        table_fields = {
            WikiTables.STRUCTURES.value: ['image', 'type', 'structure_hp', 'structure_hp_entrenched', 'armour_type', 'faction'],
            WikiTables.VEHICLES.value: ['image', 'type', 'vehicle_hp', 'armour_type', 'disable', 'faction']
        }

        async with FoxholeWikiAPIWrapper() as wrapper:
            # search request, but redirect are resolved
            resolved_search_request = next(iter(await wrapper.wiki_search_request(search_request)))

            # Get the table to request, depending on the user request
            health_table = await wrapper.find_table_from_value_name(resolved_search_request, [WikiTables.MAPS.value, WikiTables.STRUCTURES.value, WikiTables.VEHICLES.value])
            health_table_redirect = await wrapper.find_table_from_value_name(search_request, [WikiTables.MAPS.value, WikiTables.STRUCTURES.value, WikiTables.VEHICLES.value])

            # In case the user requested something that cannot be processed as a "health" entity
            if health_table is None or (health_table_redirect is not None and health_table is not None and health_table == WikiTables.MAPS.value):
                print(health_table, health_table_redirect)
                await interaction.response.send_message('> This entry is not a vehicle or a structure', ephemeral=True, delete_after=5)
                return
            elif health_table == WikiTables.MAPS.value:
                # Get the discord's server current shard
                config = configparser.ConfigParser()
                config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')
                guild_shard = config.get('default', 'shard', fallback='ABLE')

                town_tier_mapping = {
                    'TOWN_BASE_1': ' (Tier 1)',
                    'TOWN_BASE_2': ' (Tier 2)',
                    'TOWN_BASE_3': ' (Tier 3)',
                }
                # Get base tier level of selected town base / relic
                tier_level = self.bot.cache[CacheKeys.WORLD_SPAWNS_STATUS][guild_shard][search_request]

                # Get base type of selected town base / relic
                base_type = REGIONS_TYPES[search_request].value

                # Convert subregion to associated type & tier (Cuttail Station -> Town Center (Tier 3)
                resolved_search_request = f'{base_type}{town_tier_mapping.get(tier_level, '')}'

                # Maps targets are converted to their associated structures
                health_table = WikiTables.STRUCTURES.value

            data_dict = await wrapper.retrieve_row_data_from_table(table_fields[health_table], health_table, resolved_search_request)

        data_dict['name'] = resolved_search_request
        health_embed = HealthEntryEngine(data_dict).get_generated_embed()

        await interaction.response.send_message(embed=discord.Embed.from_dict(health_embed), ephemeral=not visible)

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
        if not current:
            current = 'foxhole' # when user input is empty, search for a default value foxhole

        async with FoxholeWikiAPIWrapper() as wrapper:
            search_results_redirect = await wrapper.wiki_search_request(current, do_resolve_redirect=False)

        return [app_commands.Choice(name=result, value=result) for result in list(search_results_redirect)]
