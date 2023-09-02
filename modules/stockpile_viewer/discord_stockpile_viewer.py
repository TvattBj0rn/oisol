import os
import discord
from discord.ext import commands
from modules.stockpile_viewer import CreateStockpileInterface, csv_handler, stockpile_embed_generator, discord_data_transmission
from main import bot as oisol
from modules.utils.path import generate_path


@oisol.tree.command(name='stockpile_init')
async def stockpile_init(interaction: discord.Interaction):
    os.makedirs(generate_path(interaction.guild.id, ''), exist_ok=True)
    try:
        csv_handler.csv_try_create_file(generate_path(interaction.guild.id, 'stockpiles.csv'))
    except FileExistsError:
        pass
    await interaction.response.send_message(f'> Tout a bien pu être initialisé !', ephemeral=True)


@oisol.tree.command(name='stockpile_view')
async def stockpile_view(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        stockpiles_embed = stockpile_embed_generator.generate_view_stockpile_embed(interaction)
        await interaction.followup.send(embed=stockpiles_embed)
    except discord.ext.commands.HybridCommandError as e:
        await interaction.followup.send(e)


@oisol.tree.command(name='stockpile_create')
async def stockpile_create(interaction: discord.Interaction, code: str='0', *, name: str=''):
    if not name or not code:
        await interaction.response.send_message('> Il manque un paramètre à la commande: `/create_stockpile code name`', ephemeral=True)
        return
    if len(code) != 6:
        await interaction.response.send_message('> La taille du code est incorrecte', ephemeral=True)
        return

    view = CreateStockpileInterface.CreateStockpileInterface(code, name)
    await interaction.response.send_message(view=view, ephemeral=True)


@oisol.tree.command(name='stockpile_delete')
async def stockpile_delete(interaction: discord.Interaction, stockpile_code: str):
    if not stockpile_code:
        await interaction.response.send_message('> Il manque un paramètre à la commande: `/delete_stockpile stockpile_code`', ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    csv_handler.csv_delete_data(generate_path(interaction.guild.id, 'stockpiles.csv'), stockpile_code)
    stockpiles_embed = stockpile_embed_generator.generate_view_stockpile_embed(interaction)
    await discord_data_transmission.send_data_to_discord(stockpiles_embed, interaction, 'Stockpiles Viewer', [])
    await interaction.followup.send(f'> Le stockpile (code: {stockpile_code}) a bien été supprimé', ephemeral=True)

async def setup(bot):
    bot.tree.add_command(stockpile_init)
    bot.tree.add_command(stockpile_create)
    bot.tree.add_command(stockpile_delete)
    bot.tree.add_command(stockpile_view)

