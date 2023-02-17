import re
import requests
import json
from bs4 import BeautifulSoup, Tag


## This function is used to check if the vehicle name
def check_name_validity(vehicle_name: str) -> tuple or None:
    with open('modules/vehicles_stats/vehicles_names_data/tanks_names.json') as tank_names_file:
        tank_names = json.load(tank_names_file)

    for tank_key in tank_names:
        if vehicle_name in tank_names[tank_key]:
            return tank_key, tank_names[tank_key][-1]

    return None


## This function is used to retrieve the health of a vehicle on the wiki health page
def scrap_health_page(vehicle_name: str) -> dict:
    vehicle_health_stats = dict()
    page = requests.get('https://foxhole.fandom.com/wiki/Vehicle_Health')
    soup = BeautifulSoup(page.content, 'html.parser')
    tbody_list = soup.find_all('tbody')

    for tbody in tbody_list:
        for tr in tbody.find_all('tr'):
            td_list = list(tr.find_all('td'))
            if len(td_list) == 0: # This prevents errors from the first row of the 'tr' which is categories names
                continue
            if td_list[1].text.strip() == vehicle_name[0]:
                vehicle_health_stats['HP'] = td_list[3].text.strip()
    return vehicle_health_stats


## This function is a sub-function for scrap_wiki_page and is used to get vehicle armament if the vehicle is armed
def scrap_wiki_page_armament_section(html_tags: Tag) -> dict:
    armament_pertinent_stats = ['Ammo', 'Maximum Range', 'Reload Time']
    armament_stats = dict()

    for stat in html_tags.find_all('h3'):
        if stat.text in armament_pertinent_stats:
            armament_stats[stat.text] = stat.findNext('div', attrs={'class': 'pi-data-value pi-font'}).text

    return armament_stats


## This function is used to retrieve the information on the vehicle wiki page
def scrap_wiki_page(vehicle_tup: tuple) -> dict:
    general_stats = ['Faction', 'Vehicle Type', 'Disabled Under', 'Repair Cost', 'Crew', 'Inventory Slots']
    vehicle_stats = {'general': dict(), 'armament': dict()}

    page = requests.get(vehicle_tup[1])
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get the wiki box where all the pertinent information is stored
    vehicle_box = soup.find('aside', attrs={'class': re.compile('portable-infobox pi-background pi-border-color pi-theme-(Col|War|Both) pi-layout-default type-vehicle')})

    # Get the icon for the thumbnail
    vehicle_stats['icon'] = vehicle_box.find('img')['src']

    # Get the vehicle's description
    for tag in soup.find_all('i'):
        if tag.parent.name == 'td':
            vehicle_stats['description'] = tag.text
            break

    # Get stats from the vehicle's wiki page
    for stat in vehicle_box.find_all('h3'):
        if stat.text in general_stats:
            vehicle_stats['general'][stat.text] = stat.findNext('div', attrs={'class': 'pi-data-value pi-font'}).text
    armament_section = vehicle_box.find('section', attrs={'class': 'pi-item pi-panel pi-border-color wds-tabber'})

    try:
        # Get armament stats from the wiki page
        for div in armament_section.find_all('div', attrs={'class': 'wds-tabs__tab-label'}):
            vehicle_stats['armament'][div.text.strip()] = dict()
        armament_subsections = armament_section.findAll('div', attrs={'class': re.compile('^wds-tab__content')})
        for index in range(len(list(vehicle_stats['armament'].keys()))):
            vehicle_stats['armament'][list(vehicle_stats['armament'].keys())[index]] = scrap_wiki_page_armament_section(armament_subsections[index])
            if list(vehicle_stats['armament'].keys())[index] == 'Commander':
                del vehicle_stats['armament']['Commander']
    except AttributeError: # Vehicle is a civil vehicle
        pass

    return vehicle_stats
