from __future__ import annotations

import configparser
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import REGIONS_TYPES, OISOL_HOME_PATH, DataFilesPath, CacheKeys, WikiTables
from .health_embed_template import HealthEntryEngine

from .wiki_embeds_templates import WikiTemplateFactory
from ...utils.foxhole_wiki_api_handler import FoxholeWikiAPIWrapper

if TYPE_CHECKING:
    from main import Oisol


class ModuleWiki(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot

    @app_commands.command(name='wiki', description='Get a wiki infobox')
    async def wiki(self, interaction: discord.Interaction, search_request: str, visible: bool = False) -> None:
        self.bot.logger.command(f'wiki command by {interaction.user.name} on {interaction.guild.name}')

        wiki_name, _ = search_request.split('__')
        async with FoxholeWikiAPIWrapper() as wrapper:
            # search request, but redirect are resolved
            resolved_search_request = next(iter(await wrapper.wiki_search_request(wiki_name)))

            table_name = await wrapper.find_table_from_value_name(resolved_search_request, [WikiTables.MAPS.value, WikiTables.VEHICLES.value, WikiTables.STRUCTURES.value, WikiTables.ITEM_DATA.value])
            target_fields = await wrapper.fetch_cargo_table_fields(table_name)
            data_dict = await wrapper.retrieve_row_data_from_table(target_fields, table_name, resolved_search_request)

        embeded_data = WikiTemplateFactory(data_dict).get(WikiTables(table_name)).generate_embed_data()

        await interaction.response.send_message(embed=discord.Embed().from_dict(embeded_data), ephemeral=not visible)

    @app_commands.command(name='health', description='Structures / Vehicles health')
    async def entities_health(self, interaction: discord.Interaction, search_request: str, visible: bool = False) -> None:
        self.bot.logger.command(f'health command by {interaction.user.name} on {interaction.guild.name}')

        # Fields required for health process for the two available tables
        table_fields = {
            WikiTables.STRUCTURES.value: ['image', 'type', 'structure_hp', 'structure_hp_entrenched', 'armour_type', 'faction'],
            WikiTables.VEHICLES.value: ['image', 'type', 'vehicle_hp', 'armour_type', 'disable', 'faction']
        }

        # Retrieve the wiki name from the wiki_name__user_input
        search_request, _ =  search_request.split('__')

        async with FoxholeWikiAPIWrapper() as wrapper:
            # search request, but redirect are resolved
            resolved_search_request = next(iter(await wrapper.wiki_search_request(search_request)))

            # Get the table to request, depending on the user request
            health_table = await wrapper.find_table_from_value_name(resolved_search_request, [WikiTables.MAPS.value, WikiTables.STRUCTURES.value, WikiTables.VEHICLES.value])
            health_table_redirect = await wrapper.find_table_from_value_name(search_request, [WikiTables.MAPS.value, WikiTables.STRUCTURES.value, WikiTables.VEHICLES.value])

            # In case the user requested something that cannot be processed as a "health" entity
            if health_table is None or (health_table_redirect is not None and health_table is not None and health_table == WikiTables.MAPS.value):
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

    # used in health command
    @wiki.autocomplete('search_request')
    @entities_health.autocomplete('search_request')
    async def structures_vehicles_autocomplete(self, _interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        if not current:
            current = 'foxhole' # when user input is empty, search for a default value foxhole

        async with FoxholeWikiAPIWrapper() as wrapper:
            search_results_redirect = await wrapper.wiki_search_request(current, do_resolve_redirect=False)

        return [app_commands.Choice(name=result, value=f'{result}__{current}') for result in list(search_results_redirect)]
