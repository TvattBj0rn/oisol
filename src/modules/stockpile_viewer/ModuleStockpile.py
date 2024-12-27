import configparser
import logging
import os
import pathlib
import random

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import (
    MODULES_CSV_KEYS,
    REGIONS_STOCKPILES,
    CsvHandler,
    DataFilesPath,
    EmbedIds,
    Modules,
    update_discord_interface,
)

from .stockpile_embed_generator import generate_view_stockpile_embed


class ModuleStockpiles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.csv_keys = MODULES_CSV_KEYS['stockpiles']
        self.CsvHandler = CsvHandler(self.csv_keys)

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
    @app_commands.autocomplete(localisation=region_autocomplete)
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

        r, s = localisation.split(' | ')  # Only one '|' -> 2 splits
        stockpile = {
            'region': r,
            'subregion': s,
            'code': code,
            'name': name,
        }

        for subregion in REGIONS_STOCKPILES[r]:
            if subregion[0] == s:
                stockpile['type'] = 'Seaport' if subregion[1][2:9] == 'seaport' else 'Storage Depot'
                break

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
