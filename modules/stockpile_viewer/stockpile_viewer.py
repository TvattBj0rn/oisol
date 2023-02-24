import asyncio

import discord
from discord.ext import commands
from modules.stockpile_viewer import StockpileViewerMenu, StockpileCreatorMenu, google_sheet_commands


@commands.hybrid_command()
async def view_stockpiles(ctx):
    await ctx.defer()
    try:
        stockpile_list = google_sheet_commands.get_all_stockpiles()

        embed = discord.Embed(title='Stockpiles', description='Current accessible stockpiles')
        for stockpile in stockpile_list:
            embed.add_field(name=f"{stockpile_list[stockpile]['localisation']} | {('<:storagedepot:1077298889490694204>' if stockpile_list[stockpile]['type'] == 'Storage Depot' else '<:seaport:1077298856196313158>')} | {stockpile}", value=stockpile_list[stockpile]['code'], inline=False)

        await ctx.send(embed=embed)
    except discord.ext.commands.HybridCommandError as e:
        await ctx.send(e)


@commands.hybrid_command()
async def view_stockpile(ctx, stockpile_name: str):
    menu = StockpileViewerMenu.StockpileViewerMenu(stockpile_name)
    embed = menu.set_home_page()
    await ctx.send(embed=embed, view=menu, ephemeral=True)


@commands.hybrid_command()
async def create_stockpile(ctx, code: int=0, *, name:str=''):
    if not name or not code:
        await ctx.send('> Command is missing a parameter: `$create_stockpile code name` or `/create_stockpile code name`', ephemeral=True)
        return

    view = StockpileCreatorMenu.StockpileCreatorMenu(code, name)
    await ctx.send(view=view, ephemeral=True)


async def setup(bot):
    bot.add_command(view_stockpiles)
    bot.add_command(view_stockpile)
    bot.add_command(create_stockpile)
