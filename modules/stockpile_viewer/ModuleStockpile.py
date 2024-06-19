import configparser
import discord
import os
import pathlib
import random
from discord import app_commands
from discord.ext import commands
from modules.stockpile_viewer import discord_data_transmission, stockpile_embed_generator
from modules.stockpile_viewer.CsvHandlerStockpiles import CsvHandlerStockpiles
from modules.utils import EmbedIds, DataFilesPath, REGIONS, REGIONS_STOCKPILES


class ModuleStockpiles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.csv_keys = ['region', 'subregion', 'code', 'name', 'type']

    async def region_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        regions_cities = []
        for k, v in REGIONS_STOCKPILES.items():
            for vv in v:
                regions_cities.append(f'{k} | {vv[0]}')

        if not current:
            return [app_commands.Choice(name=city, value=city) for city in random.choices(regions_cities, k=10)]

        search_results = dict()

        for city in regions_cities:
            search_results[city] = 0
            for cut_current in current.lower().split():
                if cut_current in city.lower():
                    search_results[city] += 1
            if search_results[city] == 0:
                search_results.pop(city)

        search_results = sorted(search_results, reverse=True)[:25]

        return [app_commands.Choice(name=city, value=city) for city in search_results]

    @app_commands.command(name='stockpile_view')
    async def stockpile_view(self, interaction: discord.Interaction):
        print(f'> stockpile_view command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.defer()
        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild.id))
        config = configparser.ConfigParser()
        config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        config['stockpile'] = {}
        config['stockpile']['channel'] = str(interaction.channel_id)
        with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
            config.write(configfile)
        stockpiles_embed = stockpile_embed_generator.generate_view_stockpile_embed(interaction, self.csv_keys)
        await interaction.followup.send(embed=stockpiles_embed)

    @app_commands.command(name='stockpile_create')
    @app_commands.autocomplete(region=region_autocomplete)
    async def stockpile_create(self, interaction: discord.Interaction, code: str, region: str, *, name: str):
        print(f'> stockpile_create command by {interaction.user.name} on {interaction.guild.name}')
        if len(code) != 6:
            await interaction.response.send_message(
                '> Le code doit comporter 6 chiffres',
                ephemeral=True
            )
            return

        r, s = region.split(' | ')  # Only one '|' -> 2 splits
        stockpile = {
            'region': r,
            'subregion': s,
            'code': code,
            'name': name,
        }

        for subregion in REGIONS_STOCKPILES[r]:
            if subregion[0] == s:
                stockpile['type'] = 'Seaport' if subregion[1][2:9] == 'seaport' else 'Storage Depot'

        file_path = os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.STOCKPILES.value)
        csv_handler = CsvHandlerStockpiles(self.csv_keys)
        csv_handler.csv_try_create_file(file_path)
        csv_handler.csv_append_data(file_path, stockpile)

        stockpiles_embed = stockpile_embed_generator.generate_view_stockpile_embed(interaction, self.csv_keys)

        await discord_data_transmission.send_data_to_discord(
            stockpiles_embed,
            interaction,
            EmbedIds.STOCKPILES_VIEW.value
        )

        await interaction.response.send_message('> Le stockpile a bien été généré', ephemeral=True)

    @app_commands.command(name='stockpile_delete')
    async def stockpile_delete(self, interaction: discord.Interaction, stockpile_code: str):
        print(f'> stockpile_delete command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.defer(ephemeral=True)
        CsvHandlerStockpiles(self.csv_keys).csv_delete_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.STOCKPILES.value),
            stockpile_code
        )

        await discord_data_transmission.send_data_to_discord(
            stockpile_embed_generator.generate_view_stockpile_embed(interaction, self.csv_keys),
            interaction,
            EmbedIds.STOCKPILES_VIEW.value,
        )
        await interaction.followup.send(f'> Le stockpile (code: {stockpile_code}) a bien été supprimé', ephemeral=True)

    @app_commands.command(name='stockpile_clear')
    async def stockpile_clear(self, interaction: discord.Interaction):
        print(f'> stockpile_clear command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.defer(ephemeral=True)
        CsvHandlerStockpiles(self.csv_keys).csv_clear_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.STOCKPILES.value)
        )

        await discord_data_transmission.send_data_to_discord(
            stockpile_embed_generator.generate_view_stockpile_embed(interaction, self.csv_keys),
            interaction,
            EmbedIds.STOCKPILES_VIEW.value,
        )
        await interaction.followup.send(f'> La liste des stockpiles a bien été supprimée', ephemeral=True)
