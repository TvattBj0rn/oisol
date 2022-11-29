import os

import discord
from discord.ext import commands
from discord.ext import tasks

import utils.bases
import utils.config
from Base import Base

# Bot settings
token = "MTA0NDI3MDMwMjI3MzczNjcwNA.Gotgim.n8HEX34t1aTGY7Sd_Gn_tcRa-DxDZoJXHeFcSQ"
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    update_stockpiles.start()
    print(f'Logged in as {bot.user} (ID:{bot.user.id})')


@bot.command()
async def base_new(ctx, *, base_name: str = None):
    bases_list = utils.bases.load_bases(ctx.message.guild.id)
    if not base_name:
        await ctx.send("> Le nom de la base n'a pas été précisé.\nCommande: `!base_new [nom de la base]`")
        return
    elif base_name in bases_list.keys():
        await ctx.send(f"> La base {base_name} existe déjà.")
        return
    bases_list[base_name] = Base(base_name)
    await ctx.send(f"> La base {base_name} a été crée.")
    utils.bases.save_bases(bases_list, ctx.message.guild.id)


@bot.command()
async def base_del(ctx, *, base_name: str = None):
    bases_list = utils.bases.load_bases(ctx.message.guild.id)
    if not base_name:
        await ctx.send("> Le nom de la base n'a pas été précisé.\nCommande: `!base_new [nom de la base]`")
        return
    elif base_name not in bases_list.keys():
        await ctx.send(f"> La base {base_name} n'existe pas.")
        return
    bases_list.pop(base_name, None)
    await ctx.send(f"> La base {base_name} a été supprimé.")
    utils.bases.save_bases(bases_list, ctx.message.guild.id)


@bot.command()
async def base_list(ctx):
    bases_list = utils.bases.load_bases(ctx.message.guild.id)
    if len(bases_list.keys()) == 0:
        await ctx.send(f"> Aucune base n'est actuellement enregistrée.")
        return
    base_list_display = ""
    for key in bases_list.keys():
        base_list_display += f"**{key}**\n"
        base_list_display += utils.bases.get_base_maintenance_status(bases_list[key])
    await ctx.send(base_list_display)


@bot.command()
async def base_status(ctx, base_name: str = None):
    bases_list = utils.bases.load_bases(ctx.message.guild.id)
    if not base_name:
        await ctx.send("> Le nom de la base n'a pas été précisé.\nCommande: `!base_new [nom de la base]`")
        return
    elif base_name not in bases_list.keys():
        await ctx.send(f"> La base {base_name} n'existe pas.")
        return
    await ctx.send(f"**{base_name}**\n" + utils.bases.get_base_maintenance_status(bases_list[base_name]))


@bot.command()
async def base_set_consumption(ctx, resource_type: str = None, hourly_consumption: int = None, *, base_name: str = None):
    if not resource_type or not base_name or not hourly_consumption:
        await ctx.send("> Paramètres incorrects.\nCommande: `!base_consumption [bsup/gsup] [consommation horaire] [nom de la base]`")
        return
    bases_list = utils.bases.load_bases(ctx.message.guild.id)
    resource_type = resource_type.lower()
    if base_name not in bases_list.keys():
        await ctx.send(f"> La base {base_name} n'existe pas.")
        return
    if resource_type == "bsup":
        bases_list[base_name].set_maintenance_consumption(0, hourly_consumption)
    elif resource_type == "gsup":
        bases_list[base_name].set_maintenance_consumption(1, hourly_consumption)
    else:
        await ctx.send("> Le type de ressource précisé est invalide.\n`Ressources acceptées: bsup | gsup`.")
        return
    await ctx.send(
        f"> La base {base_name} a maintenant un taux de consomation horaire de {resource_type} de {hourly_consumption}.")
    utils.bases.save_bases(bases_list, ctx.message.guild.id)


@bot.command()
async def base_set_stockpile(ctx, resource_type: str = None, stock: int = None, *, base_name: str = None):
    if not resource_type or not base_name or not stock:
        await ctx.send("> Paramètres incorrects.\nCommande: `!base_set_stockpile [bsup/gsup] [stock] [nom de la base]`")
        return
    bases_list = utils.bases.load_bases(ctx.message.guild.id)
    resource_type = resource_type.lower()
    if base_name not in bases_list.keys():
        await ctx.send(f"> La base {base_name} n'existe pas.")
        return
    if resource_type == "bsup":
        bases_list[base_name].set_maintenance_stockpile(0, stock)
    elif resource_type == "gsup":
        bases_list[base_name].set_maintenance_stockpile(1, stock)
    else:
        await ctx.send("> Le type de ressource précisé est invalide.\n`Ressources acceptées: bsup | gsup`.")
        return
    await ctx.send(f"> La base {base_name} a maintenant un stock de {resource_type} de {stock} unités.")
    utils.bases.save_bases(bases_list, ctx.message.guild.id)


@bot.command()
async def base_add_stockpile(ctx, resource_type: str = None, stock: int = None, *, base_name: str = None):
    if not resource_type or not base_name or not stock:
        await ctx.send("> Paramètres incorrects.\nCommande: `!base_add_stockpile [bsup/gsup] [stock] [nom de la base]`")
        return
    bases_list = utils.bases.load_bases(ctx.message.guild.id)
    resource_type = resource_type.lower()
    if base_name not in bases_list.keys():
        await ctx.send(f"> La base {base_name} n'existe pas.")
        return
    current_stockpile = bases_list[base_name].get_maintenance_stockpile()
    if resource_type == "bsup":
        bases_list[base_name].set_maintenance_stockpile(0, stock + current_stockpile[0])
    elif resource_type == "gsup":
        bases_list[base_name].set_maintenance_stockpile(1, stock + current_stockpile[1])
    else:
        await ctx.send("> Le type de ressource précisé est invalide.\n`Ressources acceptées: bsup | gsup`.")
        return
    await ctx.send(f"> La base {base_name} a maintenant un stock de {resource_type} de {stock} unités.")
    utils.bases.save_bases(bases_list, ctx.message.guild.id)


@tasks.loop(seconds=10)
async def update_stockpiles():
    # todo: get check if config.json has a server channel
    alert_channel = bot.get_channel(1044270821029457964)  # replace with correct channel
    for directory in os.listdir("saves/"):
        if os.path.isdir(f"saves/{directory}"):  # This corresponds to the actions to do per server
            bases_list = utils.bases.load_bases(directory)

            if len(bases_list.keys()) == 0:
                continue
            for key in bases_list.keys():
                stockpile = bases_list[key].get_maintenance_stockpile()
                consumption_rate = bases_list[key].get_maintenance_consumption()
                stockpile[0] -= consumption_rate[0]
                stockpile[1] -= consumption_rate[1]
                if stockpile[0] < 0:
                    stockpile[0] = 0
                if stockpile[1] < 0:
                    stockpile[1] = 0
                utils.bases.save_bases(bases_list, directory)

                threshold = 5
                if consumption_rate[0] > 0 and int(stockpile[0] / consumption_rate[0]) < threshold:
                    await alert_channel.send(
                        f"> Le stock de bsup restant ({stockpile[0]}) dans {key} est critique. Temps restant: {int(stockpile[0] / consumption_rate[0])}h.")
                if consumption_rate[1] > 0 and int(stockpile[1] / consumption_rate[1]) < threshold:
                    await alert_channel.send(
                        f"> Le stock de gsup restant ({stockpile[1]}) dans {key} est critique. Temps restant: {int(stockpile[0] / consumption_rate[0])}h.")


if __name__ == "__main__":
    bot.run(token, reconnect=True)
