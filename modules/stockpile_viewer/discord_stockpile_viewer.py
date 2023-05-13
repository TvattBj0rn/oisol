import discord
from discord.ext import commands
from modules.stockpile_viewer import ViewSpecificStockpileInterface, CreateStockpileInterface, ViewAllStockpilesInterface
from main import bot as oisol
import modules.stockpile_viewer.google_sheet_commands as gs

@oisol.tree.command(name='view_stockpiles')
async def view_stockpiles(interaction: discord.Interaction):
    await interaction.response.defer()
    try:
        view_all_stockpiles = ViewAllStockpilesInterface.ViewAllStockpilesInterface()
        await interaction.followup.send(embed=view_all_stockpiles.embed, view=view_all_stockpiles)
    except discord.ext.commands.HybridCommandError as e:
        await interaction.followup.send(e)


@oisol.tree.command(name='view_stockpile')
async def view_stockpile(interaction: discord.Interaction, stockpile_code: str):
    if not stockpile_code:
        await interaction.response.send_message('> Command is missing a parameter: `/view_stockpile stockpile_code`', ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    try:
        menu = ViewSpecificStockpileInterface.ViewSpecificStockpileInterface(stockpile_code)
        embed = menu.set_home_page()
        await interaction.followup.send(embed=embed, view=menu, ephemeral=True)
    except Exception:
        await interaction.followup.send('Code is incorrect')

@oisol.tree.command(name='create_stockpile')
async def create_stockpile(interaction: discord.Interaction, code: str='0', *, name:str=''):
    if not name or not code:
        await interaction.response.send_message('> Command is missing a parameter: `/create_stockpile code name`', ephemeral=True)
        return

    view = CreateStockpileInterface.CreateStockpileInterface(code, name)
    await interaction.response.send_message(view=view, ephemeral=True)


@oisol.tree.command(name='delete_stockpile')
async def delete_stockpile(interaction: discord.Interaction, stockpile_code: str):
    if not stockpile_code:
        await interaction.response.send_message('> Command is missing a parameter: `/delete_stockpile stockpile_code`', ephemeral=True)
        return
    await interaction.response.defer(ephemeral=True)
    try:
        gs.delete_stockpile(stockpile_code)
        await interaction.followup.send(f'Stockpile with code {stockpile_code} was deleted', ephemeral=True)
    except Exception:
        await interaction.followup.send('Code is incorrect')

async def setup(bot):
    bot.tree.add_command(delete_stockpile)
    bot.tree.add_command(view_stockpiles)
    bot.tree.add_command(view_stockpile)
    bot.tree.add_command(create_stockpile)
