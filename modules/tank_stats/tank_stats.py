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

    # Get the icon for the thumbnail
    tank_stats['icon'] = tank_paper.find('img')['src']

    # Get the vehicle's description
    for tag in soup.find_all('i'):
        if tag.parent.name == 'td':
            tank_stats['description'] = tag.text
            break

    # Get stats from the tank wiki page
    for stat in tank_paper.find_all('h3'):
        if stat.text in general_stats:
            tank_stats['general'][stat.text] = stat.findNext('div', attrs={'class': 'pi-data-value pi-font'}).text
    armament_section = tank_paper.find('section', attrs={'class': 'pi-item pi-panel pi-border-color wds-tabber'})

    # Get stats from the health page
    for div in armament_section.find_all('div', attrs={'class': 'wds-tabs__tab-label'}):
        tank_stats['armament'][div.text.strip()] = dict()
    armament_subsections = armament_section.findAll('div', attrs={'class': re.compile('^wds-tab__content')})
    for index in range(len(list(tank_stats['armament'].keys()))):
        tank_stats['armament'][list(tank_stats['armament'].keys())[index]] = scrap_wiki_page_armament_section(armament_subsections[index])
        if list(tank_stats['armament'].keys())[index] == 'Commander':
            del tank_stats['armament']['Commander']

    return tank_stats


def scrap_health_page(tank_name: str) -> dict:
    tank_health_stats = dict()
    url = 'https://foxhole.fandom.com/wiki/Vehicle_Health'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tank_soup = soup.find('tbody') # First one of the page is tanks

    for tr in tank_soup.find_all('tr'):
        td_list = tr.find_all('td')
        if len(td_list) == 0:
            continue
        if td_list[1].findNext('a', attrs={'title': tank_name}):
            tank_health_stats['HP'] = td_list[3].text.strip()

    return tank_health_stats


@commands.hybrid_command()
async def fstats(ctx, *, tank_name: str=''):
    if not tank_name:
        await ctx.send('> Command is missing a parameter: `!stats tank_name`')
    else:
        general_stats_list = ['Faction', 'Vehicle Type', 'Disabled Under', 'Repair Cost', 'Crew', 'Inventory Slots']
        armament_stats_list = ['Ammo', 'Maximum Range', 'Reload Time']

        tank_name = tank_name.lower()
        tank_search_keys = check_name_validity(tank_name)
        if not tank_search_keys:
            await ctx.send('> Tank name is incorrect')
        else:
            embeds_list = []
            tank_general_stats = scrap_wiki_page(tank_search_keys)
            tank_health_stats = scrap_health_page(tank_search_keys)

            embed_general_stats = discord.Embed(title=tank_search_keys[0], description=tank_general_stats['description'], color=(0x245682 if tank_general_stats['general']['Faction'] == 'Warden' else 0x516C4B))
            embed_general_stats.set_thumbnail(url=tank_general_stats['icon'])
            general_stats_list = [field for field in general_stats_list if field in tank_general_stats['general']]
            for stat in general_stats_list:
                embed_general_stats.add_field(name=stat, value=tank_general_stats['general'][stat], inline=True)
            embed_general_stats.add_field(name='', value=f'[Wiki Page]({tank_search_keys[1]})', inline=False)
            embeds_list.append(embed_general_stats)

            embed_health = discord.Embed(title='HP', color=(0x245682 if tank_general_stats['general']['Faction'] == 'Warden' else 0x516C4B))
            embed_health.add_field(name=tank_health_stats['HP'] if tank_health_stats['HP'] else 'N/A', value='', inline=True)
            embeds_list.append(embed_health)

            for key, value in tank_general_stats['armament'].items():
                embed = discord.Embed(title=key, color=(0x245682 if tank_general_stats['general']['Faction'] == 'Warden' else 0x516C4B))
                armament_stats_list = [field for field in armament_stats_list if field in value] # allow to only embed tag present in the dict
                for stat in armament_stats_list:
                    embed.add_field(name=stat, value=value[stat])
                embeds_list.append(embed)

            await ctx.send(embeds=embeds_list)



async def setup(bot):
    bot.add_command(fstats)
