from __future__ import annotations

import configparser
import logging
import os
import pathlib
import random
import re
from multiprocessing import Pool, cpu_count
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands, tasks

from src.utils import (
    MODULES_CSV_KEYS,
    REGIONS_STOCKPILES,
    CsvHandler,
    DataFilesPath,
    EmbedIds,
    MapIcon,
    Modules,
    Shard,
    update_discord_interface,
)

from ...utils.foxhole_api_handler import FoxholeAPIWrapper
from .stockpile_embed_generator import generate_view_stockpile_embed

if TYPE_CHECKING:
    from main import Oisol


class ModuleStockpiles(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot
        self.csv_keys = MODULES_CSV_KEYS['stockpiles']
        self.CsvHandler = CsvHandler(self.csv_keys)

    @app_commands.command(name='stockpile-view')
    async def stockpile_view(self, interaction: discord.Interaction) -> None:
        logging.info(f'[COMMAND] stockpile-view command by {interaction.user.name} on {interaction.guild.name}')
        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild.id))
        config = configparser.ConfigParser()
        config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))

        if not config.has_section('stockpile'):
            config.add_section('stockpile')
        config.set('stockpile', 'channel', str(interaction.channel_id))

        with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
            config.write(configfile)
        stockpiles_embed = generate_view_stockpile_embed(interaction, self.csv_keys)
        await interaction.response.send_message(embed=stockpiles_embed)

    @app_commands.command(name='stockpile-create')
    async def stockpile_create(self, interaction: discord.Interaction, code: str, localisation: str, *, name: str) -> None:
        logging.info(f'[COMMAND] stockpile-create command by {interaction.user.name} on {interaction.guild.name}')
        # Case where a user entered an invalid sized code
        if len(code) != 6:
            await interaction.response.send_message('> The code must be a 6-digits code', ephemeral=True, delete_after=5)
            return
        # Case where a user entered a code without digits only
        if not code.isdigit():
            await interaction.response.send_message('> The code contains non digit characters', ephemeral=True, delete_after=5)
            return
        # Case where a user did not select a provided localisation
        if ' | ' not in localisation or localisation.startswith(' | '):
            await interaction.response.send_message('> The localisation you entered is incorrect, displayed localisations are clickable', ephemeral=True, delete_after=5)
            return

        region, subregion = localisation.split(' | ')  # Only one '|' -> 2 splits

        stockpile = {
            'region': region,
            'subregion': subregion,
            'code': code,
            'name': name,
        }

        for s in REGIONS_STOCKPILES[region]:
            if s[0] == subregion:
                stockpile['type'] = 'Seaport' if subregion[1][2:9] == 'seaport' else 'Storage Depot'
                break

        self.bot.cursor.execute(
            'INSERT INTO GroupsStockpiles (GroupId, Region, Subregion, Code, Name, Type) VALUES (?, ?, ?, ?, ?, ?)',
            (interaction.guild_id, region, subregion, code, name, stockpile['type']),
        )
        self.bot.connection.commit()

        file_path = os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.STOCKPILES.value)
        self.CsvHandler.csv_try_create_file(file_path)
        self.CsvHandler.csv_append_data(file_path, stockpile, Modules.STOCKPILE)

        stockpiles_embed = generate_view_stockpile_embed(interaction, self.csv_keys)

        await update_discord_interface(
            interaction,
            EmbedIds.STOCKPILES_VIEW.value,
            embed=stockpiles_embed,
        )

        await interaction.response.send_message('> Stockpile was properly generated', ephemeral=True, delete_after=5)

    @app_commands.command(name='stockpile-delete')
    async def stockpile_delete(self, interaction: discord.Interaction, stockpile_code: str) -> None:
        logging.info(f'[COMMAND] stockpile-delete command by {interaction.user.name} on {interaction.guild.name}')
        self.CsvHandler.csv_delete_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild_id), DataFilesPath.STOCKPILES.value),
            stockpile_code,
        )

        await update_discord_interface(
            interaction,
            EmbedIds.STOCKPILES_VIEW.value,
            embed=generate_view_stockpile_embed(interaction, self.csv_keys),
        )
        await interaction.response.send_message(f'> The stockpile (code: {stockpile_code}) was properly removed', ephemeral=True, delete_after=5)

    @app_commands.command(name='stockpile-clear')
    async def stockpile_clear(self, interaction: discord.Interaction) -> None:
        logging.info(f'[COMMAND] stockpile-clear command by {interaction.user.name} on {interaction.guild.name}')
        self.CsvHandler.csv_clear_data(os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.STOCKPILES.value))

        await update_discord_interface(
            interaction,
            EmbedIds.STOCKPILES_VIEW.value,
            embed=generate_view_stockpile_embed(interaction, self.csv_keys),
        )
        await interaction.response.send_message('> The stockpile interface was properly cleared', ephemeral=True, delete_after=5)

    @stockpile_create.autocomplete('localisation')
    async def region_autocomplete(self, _interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        regions_cities = []
        for region_name, subregion_tuples in REGIONS_STOCKPILES.items():
            for subregion_name, *_ in subregion_tuples:
                regions_cities.append(f'{region_name} | {subregion_name}')

        if not current:
            return [app_commands.Choice(name=city, value=city) for city in random.choices(regions_cities, k=10)]

        search_results = {}

        for city in regions_cities:
            search_results[city] = 0
            for cut_current in current.lower().split():
                if cut_current in city.lower():
                    search_results[city] += 1
            if search_results[city] == 0:
                search_results.pop(city)

        search_results = sorted(search_results, reverse=True)[:25]

        return [app_commands.Choice(name=city, value=city) for city in search_results]


class StockpileTasks(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot
        self.all_regions_stockpiles = []
        # Start tasks
        self.refresh_able_shard_stockpiles_subregions.start()
        self.refresh_baker_shard_stockpiles_subregions.start()
        self.refresh_charlie_shard_stockpiles_subregions.start()

    @staticmethod
    def _prepare_region_data(api_wrapper: FoxholeAPIWrapper, war_data: dict, region: str) -> list[tuple]:
        single_region_stockpiles = []
        map_items = api_wrapper.get_region_specific_icons(region, [MapIcon.SEAPORT.value, MapIcon.STORAGE_DEPOT.value])
        map_label = api_wrapper.get_region_specific_labels(region)
        ordered_items = api_wrapper.get_subregion_from_map_items(map_items, map_label)
        if region == 'MooringCountyHex':
            region = 'TheMoors'
        elif region == 'DeadLandsHex':
            region = 'Deadlands'
        if ordered_items is not None:
            for item in ordered_items:
                single_region_stockpiles.append((
                    api_wrapper.shard_name,
                    war_data['warNumber'],
                    war_data['conquestStartTime'],
                    re.sub(r'(\w)([A-Z])', r'\1 \2', region.replace('Hex', '')),
                    *item,
                ))
        return single_region_stockpiles

    def _save_region_stockpiles(self, region_stockpiles: list[tuple]) -> None:
        self.all_regions_stockpiles += region_stockpiles

    def _get_latest_stockpiles_zones(self, api_wrapper: FoxholeAPIWrapper, war_data: dict) -> list:
        region_list = api_wrapper.get_regions_list()
        pool = Pool(processes=(cpu_count() - 1))
        for region in region_list:
            pool.apply_async(self._prepare_region_data, args=(api_wrapper, war_data, region), callback=self._save_region_stockpiles)
        pool.close()
        pool.join()
        return self.all_regions_stockpiles

    def _update_stockpile_subregions(self, shard_api: FoxholeAPIWrapper) -> None:
        self.all_regions_stockpiles = []
        if current_war_data := shard_api.get_current_war_state():
            last_war_start_time = self.bot.cursor.execute(
                f"SELECT MAX(ConquestStartTime) FROM StockpilesZones WHERE Shard == '{shard_api.shard_name}'",
            ).fetchone()[0]
            # If war has not started yet
            if not current_war_data['conquestStartTime']:
                return
            if last_war_start_time is None or current_war_data['conquestStartTime'] > last_war_start_time:
                if not (latest_stockpiles := self._get_latest_stockpiles_zones(shard_api, current_war_data)):
                    return
                self.bot.cursor.executemany(
                    'INSERT INTO StockpilesZones (Shard, WarNumber, ConquestStartTime, Region, Subregion, Type) VALUES (?, ?, ?, ?, ?, ?)',
                    latest_stockpiles,
                )
                self.bot.connection.commit()
                logging.info(f'[TASK] Available stockpiles were updated for {shard_api.shard_name}')

    @tasks.loop(minutes=2)
    async def refresh_able_shard_stockpiles_subregions(self) -> None:
        self._update_stockpile_subregions(FoxholeAPIWrapper())

    @tasks.loop(minutes=2)
    async def refresh_baker_shard_stockpiles_subregions(self) -> None:
        self._update_stockpile_subregions(FoxholeAPIWrapper(shard=Shard.BAKER))

    @tasks.loop(minutes=2)
    async def refresh_charlie_shard_stockpiles_subregions(self) -> None:
        self._update_stockpile_subregions(FoxholeAPIWrapper(shard=Shard.CHARLIE))
