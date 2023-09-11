import discord
from discord import app_commands
from discord.ext import commands
from modules.stockpile_viewer import CreateStockpileInterface, CsvHandlerStockpiles, discord_data_transmission, stockpile_embed_generator
from modules.utils.EmbedFooterEnums import EmbedIds
from modules.utils.path import DataFilesPath, generate_path


class ModuleStockpiles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.csv_keys = ['region', 'subregion', 'code', 'name', 'type']

    @app_commands.command(name='stockpile_view')
    async def stockpile_view(self, interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            stockpiles_embed = stockpile_embed_generator.generate_view_stockpile_embed(interaction)
            await interaction.followup.send(embed=stockpiles_embed)
        except discord.ext.commands.HybridCommandError as e:
            await interaction.followup.send(e)

    @app_commands.command(name='stockpile_create')
    async def stockpile_create(self, interaction: discord.Interaction, code: str='0', *, name: str=''):
        if not name or not code:
            await interaction.response.send_message('> Il manque un paramètre à la commande: `/stockpile_create code name`', ephemeral=True)
            return
        if len(code) != 6:
            await interaction.response.send_message('> La taille du code est incorrecte', ephemeral=True)
            return

        view = CreateStockpileInterface.CreateStockpileInterface(code, name, self.csv_keys)
        await interaction.response.send_message(view=view, ephemeral=True)

    @app_commands.command(name='stockpile_delete')
    async def stockpile_delete(self, interaction: discord.Interaction, stockpile_code: str):
        if not stockpile_code:
            await interaction.response.send_message('> Il manque un paramètre à la commande: `/stockpile_delete stockpile_code`', ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        CsvHandlerStockpiles.CsvHandlerStockpiles(self.csv_keys).csv_delete_data(generate_path(interaction.guild.id, DataFilesPath.STOCKPILES.value), stockpile_code)
        await discord_data_transmission.send_data_to_discord(stockpile_embed_generator.generate_view_stockpile_embed(interaction), interaction, EmbedIds.STOCKPILES_VIEW.value, [])
        await interaction.followup.send(f'> Le stockpile (code: {stockpile_code}) a bien été supprimé', ephemeral=True)
