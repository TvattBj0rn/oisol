import json
import re

import discord
import requests
from discord.ext import commands
from bs4 import BeautifulSoup, Tag


def check_name_validity(tank_name: str) -> tuple or None:
    with open('modules/tank_stats/tanks_names.json') as tank_names_file:
        tank_names = json.load(tank_names_file)

    for tank_key in tank_names:
        if tank_name in tank_names[tank_key]:
            return tank_key, tank_names[tank_key][-1]

    return None


def scrap_wiki_page_armament_section(html_tags: Tag) -> dict:
    armament_pertinent_stats = ['Ammo', 'Maximum Range', 'Reload Time']
    armament_stats = dict()

    for stat in html_tags.find_all('h3'):
        if stat.text in armament_pertinent_stats:
            armament_stats[stat.text] = stat.findNext('div', attrs={'class': 'pi-data-value pi-font'}).text

    return armament_stats


def scrap_wiki_page(tank_tup: tuple) -> dict:
    general_stats = ['Faction', 'Vehicle Type', 'Disabled Under', 'Repair Cost', 'Crew', 'Inventory Slots']
    tank_stats = {'general': dict(), 'armament': dict()}
    page = requests.get(tank_tup[1])
    soup = BeautifulSoup(page.content, 'html.parser')
    tank_paper = soup.find('aside')

    tank_stats['icon'] = tank_paper.find('img')['src']
    for tag in soup.find_all('i'):
        if tag.text != 'could':
            tank_stats['description'] = tag.text
            break

    for stat in tank_paper.find_all('h3'):
        if stat.text in general_stats:
            tank_stats['general'][stat.text] = stat.findNext('div', attrs={'class': 'pi-data-value pi-font'}).text
    armament_section = tank_paper.find('section', attrs={'class': 'pi-item pi-panel pi-border-color wds-tabber'})

    for div in armament_section.find_all('div', attrs={'class': 'wds-tabs__tab-label'}):
        tank_stats['armament'][div.text.strip()] = dict()
    armament_subsections = armament_section.findAll('div', attrs={'class': re.compile('^wds-tab__content')})
    for index in range(len(list(tank_stats['armament'].keys()))):
        tank_stats['armament'][list(tank_stats['armament'].keys())[index]] = scrap_wiki_page_armament_section(armament_subsections[index])

    return tank_stats


@commands.command()
async def stats(ctx, tank_name: str=''):
    if not tank_name:
        await ctx.send('> Command is missing a parameter: `!stats tank_name`')
    else:
        tank_search_keys = check_name_validity(tank_name)
        if not tank_search_keys:
            await ctx.send('> Tank name is incorrect')
        else:
            tank_general_stats = scrap_wiki_page(tank_search_keys)
            # tank_health_stats = scrap_health_page(tank_search_keys)

            embed = discord.Embed(title=tank_search_keys[0], description=tank_general_stats['description'], color=(0x245682 if tank_general_stats['general']['Faction'] == 'Warden' else 0x516C4B))
            embed.set_thumbnail(url=tank_general_stats['icon'])
            embed.add_field(name='Faction', value=tank_general_stats['general']['Faction'], inline=True)
            embed.add_field(name='Vehicle Type', value=tank_general_stats['general']['Vehicle Type'], inline=True)
            embed.add_field(name='Disable Under', value=tank_general_stats['general']['Disabled Under'], inline=True)
            embed.add_field(name='Repair Cost', value=tank_general_stats['general']['Repair Cost'], inline=True)
            embed.add_field(name='Crew', value=tank_general_stats['general']['Crew'], inline=True)
            embed.add_field(name='Inventory Slots', value=tank_general_stats['general']['Inventory Slots'], inline=True)
            await ctx.send(embed=embed)

            print(tank_general_stats)
            for key, value in tank_general_stats['armament'].items():

                embed = discord.Embed(title=key, color=(0x245682 if tank_general_stats['general']['Faction'] == 'Warden' else 0x516C4B))
                embed.add_field(name='Ammo', value=value['Ammo'], inline=True)
                try:
                    embed.add_field(name='Max. Range', value=value['Maximum Range'], inline=True)
                    embed.add_field(name='Reload Time', value=value['Reload Time'], inline=True)
                except KeyError:
                    pass
                await ctx.send(embed=embed)



async def setup(bot):
    bot.add_command(stats)
