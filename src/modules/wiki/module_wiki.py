from __future__ import annotations

import configparser
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import (
    OISOL_HOME_PATH,
    REGIONS_TYPES,
    CacheKeys,
    DataFilesPath,
    WikiTables,
)

from ...utils.autocompletion import (
    ITEMDATA_DATA,
    MAPS_DATA,
    STRUCTURES_DATA,
    VEHICLES_DATA,
)
from ...utils.foxhole_wiki_api_handler import FoxholeWikiAPIWrapper
from .health_embed_template import HealthEntryEngine
from .wiki_embeds_templates import WikiTemplateFactory

if TYPE_CHECKING:
    from main import Oisol


HEALTH_DATA = STRUCTURES_DATA + VEHICLES_DATA + [
                {'name': subregion, 'keywords': subregion.lower(), 'table': 'custom_map'} for subregion in REGIONS_TYPES
            ]
HEALTH_DATA_KEYS = [entry['name'] for entry in HEALTH_DATA]

WIKI_DATA = ITEMDATA_DATA + MAPS_DATA + STRUCTURES_DATA + VEHICLES_DATA
WIKI_DATA_KEYS = [entry['name'] for entry in WIKI_DATA]


class ModuleWiki(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot

    @app_commands.command(name='wiki', description='Get a wiki infobox')
    async def wiki(self, interaction: discord.Interaction, search_request: str, visible: bool = False) -> None:
        self.bot.logger.command(f'wiki command by {interaction.user.name} on {interaction.guild.name}')

        # Retrieve search_request & table from autocomplete value: search_request@table
        split_search_request = search_request.split('@')
        if len(split_search_request) != 2:
            await interaction.response.send_message('> The entry you provided is invalid', ephemeral=True, delete_after=5)
            return

        search_request, table_name = split_search_request
        if search_request not in WIKI_DATA_KEYS:
            await interaction.response.send_message('> The entry you provided does not exist', ephemeral=True, delete_after=5)
            return

        async with FoxholeWikiAPIWrapper() as wrapper:
            target_fields = await wrapper.fetch_cargo_table_fields(table_name)
            data_dict = await wrapper.retrieve_row_data_from_table(target_fields, table_name, search_request)

        embeded_data = WikiTemplateFactory(data_dict).get(WikiTables(table_name)).generate_embed_data()

        await interaction.response.send_message(embed=discord.Embed().from_dict(embeded_data), ephemeral=not visible)

    @app_commands.command(name='health', description='Structures / Vehicles health')
    async def entities_health(self, interaction: discord.Interaction, search_request: str, visible: bool = False) -> None:
        self.bot.logger.command(f'health command by {interaction.user.name} on {interaction.guild.name}')

        # Fields required for health process for the two available tables
        table_fields = {
            WikiTables.STRUCTURES.value: ['image', 'type', 'structure_hp', 'structure_hp_entrenched', 'armour_type', 'faction'],
            WikiTables.VEHICLES.value: ['image', 'type', 'vehicle_hp', 'armour_type', 'disable', 'faction'],
        }

        # Retrieve search_request & table from autocomplete value: search_request@table
        split_search_request = search_request.split('@')
        if len(split_search_request) != 2:
            await interaction.response.send_message('> The entry you provided is invalid', ephemeral=True, delete_after=5)
            return

        search_request, health_table = split_search_request
        if search_request not in HEALTH_DATA_KEYS:
            await interaction.response.send_message('> The entry you provided does not exist', ephemeral=True, delete_after=5)
            return

        # Special subregion buffer for display purpose
        subregion_name = ''

        # Associate given subregion to its current type of base + tier status
        if health_table == 'custom_map':
            # Get the discord's server current shard
            config = configparser.ConfigParser()
            config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')
            guild_shard = config.get('default', 'shard', fallback='ABLE')
            subregion_name = search_request

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
            search_request = f'{base_type}{town_tier_mapping.get(tier_level, '')}'

            # Maps targets are converted to their associated structures
            health_table = WikiTables.STRUCTURES.value

        async with FoxholeWikiAPIWrapper() as wrapper:
            data_dict = await wrapper.retrieve_row_data_from_table(table_fields[health_table], health_table, search_request)

        data_dict['name'] = subregion_name if subregion_name else search_request

        # Compute health of search_request & generate embed
        health_embed = HealthEntryEngine(data_dict).get_generated_embed()

        await interaction.response.send_message(embed=discord.Embed.from_dict(health_embed), ephemeral=not visible)

    @staticmethod
    def _generic_autocomplete(search_data: list[dict], current: str) -> list[app_commands.Choice]:
        # Normalize current
        current = current.lower().strip().split(' ')

        # Score each entry using keywords and current
        scoring_result = {}
        for i, entry in enumerate(search_data):
            if entry_sum_result := sum(1 for kw in current if kw in entry['keywords']):
                scoring_result[i] = entry_sum_result

        # Sort to get the highest entry score
        scoring_result = dict(sorted(scoring_result.items(), key=lambda item: item[1], reverse=True))

        top_entries_indexes = list(scoring_result)[:10]
        top_entries = [search_data[i] for i in top_entries_indexes]

        return [app_commands.Choice(name=entry['name'], value=f'{entry['name']}@{entry['table']}') for entry in top_entries]

    @entities_health.autocomplete('search_request')
    async def health_autocomplete(self, _interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return self._generic_autocomplete(HEALTH_DATA, current)

    @wiki.autocomplete('search_request')
    async def wiki_autocomplete(self, _interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        return self._generic_autocomplete(WIKI_DATA, current)
