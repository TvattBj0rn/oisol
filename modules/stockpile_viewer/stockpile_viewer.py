import discord
from discord.ext import commands
from modules.stockpile_viewer import StockpileViewerMenu, StockpileCreatorMenu, google_sheet_commands


@commands.hybrid_command()
async def view_stockpiles(ctx):
    await ctx.defer()
    try:
        stockpile_list = google_sheet_commands.get_all_stockpiles()

        sorted_stockpile_list = dict()
        for stockpile_name, stockpile_values in stockpile_list.items():
            if stockpile_values['localisation'] not in sorted_stockpile_list.keys():
                sorted_stockpile_list[stockpile_values['localisation']] = list()
            sorted_stockpile_list[stockpile_values['localisation']].append({stockpile_name: stockpile_values})
        embed = discord.Embed(title='Stockpiles', description='Current accessible stockpiles', color=0x245682)

        for localisation, stockpile_list in sorted_stockpile_list.items():
            stockpiles_here = str()
            for stockpile in stockpile_list:
                stockpiles_here += f"{stockpile[list(stockpile.keys())[0]]['name']} | {stockpile[list(stockpile.keys())[0]]['code']}\n"
            embed.add_field(
                name=localisation,
                value=stockpiles_here,
                inline=False
            )

        await ctx.send(embed=embed)
    except discord.ext.commands.HybridCommandError as e:
        await ctx.send(e)


@commands.hybrid_command()
async def view_stockpile(ctx, stockpile_name: str):
    menu = StockpileViewerMenu.StockpileViewerMenu(stockpile_name)
    embed = menu.set_home_page()
    await ctx.send(embed=embed, view=menu, ephemeral=True)


@commands.hybrid_command()
async def create_stockpile(ctx, code: str='0', *, name:str=''):
    if not name or not code:
        await ctx.send('> Command is missing a parameter: `$create_stockpile code name` or `/create_stockpile code name`', ephemeral=True)
        return

    view = StockpileCreatorMenu.StockpileCreatorMenu(code, name)
    await ctx.send(view=view, ephemeral=True)


async def setup(bot):
    bot.add_command(view_stockpiles)
    bot.add_command(view_stockpile)
    bot.add_command(create_stockpile)
