import discord
from discord.ext import commands
from modules.stockpile_viewer import StockpileViewerMenu, StockpileCreatorMenu, google_sheet_commands
from modules.utils import foxhole_types
from main import bot as oisol

@oisol.tree.command(name='view_stockpiles')
async def view_stockpiles(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    try:
        stockpile_list = google_sheet_commands.get_all_stockpiles()
        sorted_stockpile_list = dict()

        for stockpile_name, stockpile_values in stockpile_list.items():
            if stockpile_values['localisation'] not in sorted_stockpile_list.keys():
                sorted_stockpile_list[stockpile_values['localisation']] = list()
            sorted_stockpile_list[stockpile_values['localisation']].append({stockpile_name: stockpile_values})
        embed = discord.Embed(
            title='Stockpiles',
            description='Current accessible stockpiles',
            color=foxhole_types.FACTION_COLORS['Warden']
        )

        for localisation, stockpile_list in sorted_stockpile_list.items():
            stockpiles_here = str()
            for stockpile in stockpile_list:
                stockpiles_here += f"{stockpile[list(stockpile.keys())[0]]['name']} | {stockpile[list(stockpile.keys())[0]]['code']}\n"
            embed.add_field(
                name=localisation,
                value=stockpiles_here,
                inline=False
            )

        await interaction.followup.send(embed=embed)
    except discord.ext.commands.HybridCommandError as e:
        await interaction.followup.send(e)


@oisol.tree.command(name='view_stockpile')
async def view_stockpile(interaction: discord.Interaction, stockpile_name: str):
    if not stockpile_name:
        await interaction.response.send_message('> Command is missing a parameter: `/view_stockpile stockpile_name`', ephemeral=True)
        return
    menu = StockpileViewerMenu.StockpileViewerMenu(stockpile_name)
    embed = menu.set_home_page()
    await interaction.response.send_message(embed=embed, view=menu, ephemeral=True)


@oisol.tree.command(name='create_stockpile')
async def create_stockpile(interaction: discord.Interaction, code: str='0', *, name:str=''):
    if not name or not code:
        await interaction.response.send_message('> Command is missing a parameter: `/create_stockpile code name`', ephemeral=True)
        return

    view = StockpileCreatorMenu.StockpileCreatorMenu(code, name)
    await interaction.response.send_message(view=view, ephemeral=True)


async def setup(bot):
    bot.tree.add_command(view_stockpiles)
    bot.tree.add_command(view_stockpile)
    bot.tree.add_command(create_stockpile)
