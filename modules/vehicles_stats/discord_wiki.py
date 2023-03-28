import discord
from modules.vehicles_stats import wiki_utils
from modules.utils import foxhole_types
from main import bot as oisol

@oisol.tree.command(name='wiki')
async def wiki(interaction: discord.Interaction, *, vehicle_name: str=''):
    if not vehicle_name:
        await interaction.response.send_message('> Command is missing a parameter: `/wiki vehicle_name`', ephemeral=True)
    else:
        general_stats_list = ['Faction', 'Vehicle Type', 'Disabled Under', 'Repair Cost', 'Crew', 'Inventory Slots', 'Cost']
        armament_stats_list = ['Ammo', 'Maximum Range', 'Reload Time', 'Range']


        vehicle_name = vehicle_name.lower()
        vehicle_search_keys = wiki_utils.check_name_validity(vehicle_name)
        if not vehicle_search_keys:
            await interaction.response.send_message('> Vehicle name is incorrect', ephemeral=True)
            return
        embeds_list = []
        vehicle_general_stats = wiki_utils.scrap_wiki_page(vehicle_search_keys)
        vehicle_health_stats = wiki_utils.scrap_health_page(vehicle_search_keys)

        embed = discord.Embed(
            title=vehicle_search_keys[0],
            description=vehicle_general_stats['description'],
            color=factions_settings.FACTION_COLORS[vehicle_general_stats['general']['Faction']],

        )
        embed.set_thumbnail(url=vehicle_general_stats['icon'])

        general_stats_list = [field for field in general_stats_list if field in vehicle_general_stats['general']]

        embed.add_field(
            name='**HP**',
            value=vehicle_health_stats['HP'] if 'HP' in vehicle_health_stats else 'N/A',
            inline=False
        )
        for stat in general_stats_list:
            embed.add_field(
                name=stat,
                value=vehicle_general_stats['general'][stat],
                inline=True
            )

        if vehicle_general_stats['general']['Vehicle Type'] in wiki_utils.MILITARY_VEHICLE:
            embed.add_field(
                name=u'\u200B',
                value='',
                inline=False
            )
            embed.add_field(
                name='**Armament**',
                value='',
                inline=False
            )
            for key, value in vehicle_general_stats['armament'].items():
                embed.add_field(
                    name=key,
                    value='',
                    inline=False
                )
                armament_stats_list = [field for field in armament_stats_list if field in value] # allow to only embed tag present in the dict
                for stat in armament_stats_list:
                    embed.add_field(
                        name=stat,
                        value=value[stat],
                        inline=True
                    )
        embed.add_field(
            name='',
            value=f'[Wiki Page]({vehicle_search_keys[1]})',
            inline=False
        )
        embeds_list.append(embed)

        vehicle_health_stats.pop('HP')
        embed = discord.Embed(
            title='**Damage Type Resistance**',
            color=factions_settings.FACTION_COLORS[vehicle_general_stats['general']['Faction']]
        )
        for key, value in vehicle_health_stats.items():
            embed.add_field(
                name=key,
                value='',
                inline=False
            )
            for subkey, sub_value in value.items():
                embed.add_field(
                    name=subkey,
                    value=sub_value,
                    inline=True
                )
            embed.add_field(
                name=u'\u200B',
                value='',
                inline=False
            )
        embed.add_field(
            name='',
            value=f"[Wiki Page]({'https://foxhole.wiki.gg/wiki/Vehicle_Health'})",
            inline=False
        )
        embeds_list.append(embed)

        await interaction.response.send_message(embeds=embeds_list, ephemeral=True)

async def setup(bot):
    bot.tree.add_command(wiki)