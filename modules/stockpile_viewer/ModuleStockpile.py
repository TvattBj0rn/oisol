import configparser
import discord
import os
import pathlib
from discord import app_commands
from discord.ext import commands
from modules.stockpile_viewer import CreateStockpileInterface, discord_data_transmission, stockpile_embed_generator
from modules.stockpile_viewer.CsvHandlerStockpiles import CsvHandlerStockpiles
from modules.utils import EmbedIds
from modules.utils import DataFilesPath


class ModuleStockpiles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.csv_keys = ['region', 'subregion', 'code', 'name', 'type']

    @app_commands.command(name='stockpile_view')
    async def stockpile_view(self, interaction: discord.Interaction):
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
    async def stockpile_create(self, interaction: discord.Interaction, code: str, *, name: str):
        if len(code) != 6:
            await interaction.response.send_message(
                '> Le code doit comporter 6 digits',
                ephemeral=True
            )
            return

        view = CreateStockpileInterface.CreateStockpileInterface(code, name, self.csv_keys)
        await interaction.response.send_message(view=view, ephemeral=True)

    @app_commands.command(name='stockpile_delete')
    async def stockpile_delete(self, interaction: discord.Interaction, stockpile_code: str):
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
        await interaction.followup.send(
            f'> Le stockpile (code: {stockpile_code}) a bien été supprimé',
            ephemeral=True
        )

    @app_commands.command(name='stockpile_clear')
    async def stockpile_clear(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        CsvHandlerStockpiles(self.csv_keys).csv_clear_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.STOCKPILES.value)
        )

        await discord_data_transmission.send_data_to_discord(
            stockpile_embed_generator.generate_view_stockpile_embed(interaction, self.csv_keys),
            interaction,
            EmbedIds.STOCKPILES_VIEW.value,
        )

        await interaction.followup.send(
            f'> La liste des stockpiles a bien été supprimée',
            ephemeral=True
        )
