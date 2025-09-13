from __future__ import annotations

import configparser
from itertools import compress
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

from ...utils.foxhole_wiki_api_handler import FoxholeWikiAPIWrapper
from .health_embed_template import HealthEntryEngine
from .wiki_embeds_templates import WikiTemplateFactory

if TYPE_CHECKING:
    from main import Oisol


class ModuleWiki(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot
        self._autocomplete_cache = {}

    @app_commands.command(name='wiki', description='Get a wiki infobox')
    async def wiki(self, interaction: discord.Interaction, search_request: str, visible: bool = False) -> None:
        self.bot.logger.command(f'wiki command by {interaction.user.name} on {interaction.guild.name}')

        self._autocomplete_cache.pop(interaction.user.id, None)

        async with FoxholeWikiAPIWrapper() as wrapper:
            # search request, but redirect are resolved
            resolved_search_request = next(iter(await wrapper.wiki_search_request(search_request)), search_request)

            table_name = await wrapper.find_table_from_value_name(resolved_search_request, [WikiTables.MAPS.value, WikiTables.VEHICLES.value, WikiTables.STRUCTURES.value, WikiTables.ITEM_DATA.value])
            target_fields = await wrapper.fetch_cargo_table_fields(table_name)
            data_dict = await wrapper.retrieve_row_data_from_table(target_fields, table_name, resolved_search_request)

        embeded_data = WikiTemplateFactory(data_dict).get(WikiTables(table_name)).generate_embed_data()

        await interaction.response.send_message(embed=discord.Embed().from_dict(embeded_data), ephemeral=not visible)

    @app_commands.command(name='health', description='Structures / Vehicles health')
    async def entities_health(self, interaction: discord.Interaction, search_request: str, visible: bool = False) -> None:
        self.bot.logger.command(f'health command by {interaction.user.name} on {interaction.guild.name}')

        self._autocomplete_cache.pop(interaction.user.id, None)

        # Fields required for health process for the two available tables
        table_fields = {
            WikiTables.STRUCTURES.value: ['image', 'type', 'structure_hp', 'structure_hp_entrenched', 'armour_type', 'faction'],
            WikiTables.VEHICLES.value: ['image', 'type', 'vehicle_hp', 'armour_type', 'disable', 'faction'],
        }

        async with FoxholeWikiAPIWrapper() as wrapper:
            # search request, but redirect are resolved
            resolved_search_request = next(iter(await wrapper.wiki_search_request(search_request)), search_request)

            # Get the table to request, depending on the user request
            health_table = await wrapper.find_table_from_value_name(resolved_search_request, [WikiTables.MAPS.value, WikiTables.STRUCTURES.value, WikiTables.VEHICLES.value])
            health_table_redirect = await wrapper.find_table_from_value_name(search_request, [WikiTables.MAPS.value, WikiTables.STRUCTURES.value, WikiTables.VEHICLES.value])

            # In case the user requested something that cannot be processed as a "health" entity
            if health_table is None or (health_table_redirect is not None and health_table is not None and health_table == WikiTables.MAPS.value):
                await interaction.response.send_message('> This entry is not a vehicle or a structure', ephemeral=True, delete_after=5)
                return

            if health_table == WikiTables.MAPS.value:
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

            # Search request can include tiered entries while resolved serve as a backup
            final_search_request = resolved_search_request if health_table_redirect is None else search_request

            data_dict = await wrapper.retrieve_row_data_from_table(table_fields[health_table], health_table, final_search_request)

        data_dict['name'] = final_search_request
        health_embed = HealthEntryEngine(data_dict).get_generated_embed()

        await interaction.response.send_message(embed=discord.Embed.from_dict(health_embed), ephemeral=not visible)

    @wiki.autocomplete('search_request')
    @entities_health.autocomplete('search_request')
    async def structures_vehicles_autocomplete(self, _interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        if not current:
            current = 'foxhole' # when user input is empty, search for a default value foxhole

        async with FoxholeWikiAPIWrapper() as wrapper:
            # Get non redirected search results
            search_results = await wrapper.wiki_search_request(current, do_resolve_redirect=False)

            # Create a mask of valid entries from raw results (not a page but a redirect are ignored for example)
            mask = await wrapper.is_page_wiki_page(wrapper.get_active_session(), list(search_results))

        # Get valid entries from the mask
        search_results_redirect = compress(list(search_results), mask)

        # Manual corrections to add all types of a specific entry,
        # Replace k by k: k + vv for vv in v
        tier_iterable = ['(Tier 1)', '(Tier 2)', '(Tier 3)']
        manual_corrections = {
            'Safe House': tier_iterable,
            'Town Center': tier_iterable,
            'Post Office': tier_iterable,
            'School': tier_iterable,
            'Bunker Base': tier_iterable,
            'Wall': tier_iterable,
            'Gate': tier_iterable,
            'Bunker': tier_iterable,
            'Bunker Ramp': tier_iterable,
            'Bunker Corner': tier_iterable,
            'Observation Bunker': tier_iterable,
            'Garrisoned House': [
                '- Small (Tier 1)', '- Medium (Tier 1)', '- Large (Tier 1)',
                '- Small (Tier 2)', '- Medium (Tier 2)', '- Large (Tier 2)',
                '- Small (Tier 3)', '- Medium (Tier 3)', '- Large (Tier 3)',
            ],
        }

        final_search_list = []

        for entry in search_results_redirect:
            if entry in manual_corrections:
                final_search_list.extend(f'{entry} {correction}' for correction in manual_corrections[entry])
            else:
                final_search_list.append(entry)

        return [app_commands.Choice(name=result, value=result) for result in final_search_list]
