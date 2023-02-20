import discord
from modules.vehicles_stats import fstats_utils
from discord.ext import commands


@commands.hybrid_command()
async def fstats(ctx, *, vehicle_name: str=''):
    if not vehicle_name:
        await ctx.send('> Command is missing a parameter: `$stats vehicle_name` or `/stats vehicle_name`', ephemeral=True)
    else:
        general_stats_list = ['Faction', 'Vehicle Type', 'Disabled Under', 'Repair Cost', 'Crew', 'Inventory Slots']
        armament_stats_list = ['Ammo', 'Maximum Range', 'Reload Time']
        faction_color = {'Warden': 0x245682, 'Colonial': 0x516C4B, 'Both': 0xffffff}

        vehicle_name = vehicle_name.lower()
        vehicle_search_keys = fstats_utils.check_name_validity(vehicle_name)
        if not vehicle_search_keys:
            await ctx.send('> Tank name is incorrect', ephemeral=True)
        else:
            embeds_list = []
            vehicle_general_stats = fstats_utils.scrap_wiki_page(vehicle_search_keys)
            vehicle_health_stats = fstats_utils.scrap_health_page(vehicle_search_keys)

            embed = discord.Embed(title=vehicle_search_keys[0], description=vehicle_general_stats['description'], color=faction_color[vehicle_general_stats['general']['Faction']])
            embed.set_thumbnail(url=vehicle_general_stats['icon'])

            general_stats_list = [field for field in general_stats_list if field in vehicle_general_stats['general']]

            embed.add_field(name='**HP**', value=vehicle_health_stats['HP'] if 'HP' in vehicle_health_stats else 'N/A', inline=False)
            for stat in general_stats_list:
                embed.add_field(name=stat, value=vehicle_general_stats['general'][stat], inline=True)

            if vehicle_general_stats['general']['Vehicle Type'] in fstats_utils.MILITARY_VEHICLE:
                embed.add_field(name=u'\u200B', value='', inline=False)
                embed.add_field(name='**Armament**', value='', inline=False)
                for key, value in vehicle_general_stats['armament'].items():
                    embed.add_field(name=key, value='', inline=False)
                    armament_stats_list = [field for field in armament_stats_list if field in value] # allow to only embed tag present in the dict
                    for stat in armament_stats_list:
                        embed.add_field(name=stat, value=value[stat], inline=True)
            embed.add_field(name='', value=f'[Wiki Page]({vehicle_search_keys[1]})', inline=False)
            embeds_list.append(embed)

            vehicle_health_stats.pop('HP')
            embed = discord.Embed(title='**Shell Resistance**', color=faction_color[vehicle_general_stats['general']['Faction']])
            for key, value in vehicle_health_stats.items():
                embed.add_field(name=key, value='', inline=False)
                for subkey, sub_value in value.items():
                    embed.add_field(name=subkey, value=sub_value, inline=True)
                embed.add_field(name=u'\u200B', value='', inline=False)
            embed.add_field(name='', value=f"[Wiki Page]({'https://foxhole.fandom.com/wiki/Vehicle_Health'})", inline=False)
            embeds_list.append(embed)

            await ctx.send(embeds=embeds_list, ephemeral=True)


async def setup(bot):
    bot.add_command(fstats)
