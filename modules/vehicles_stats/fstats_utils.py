import re
import requests
import json
from bs4 import BeautifulSoup, Tag


MILITARY_VEHICLE = ['Armoured Car', 'Assault Tank', 'Battle Tank', 'Combat Car', 'Cruiser Tank', 'Destroyer Tank', 'Field Artillery', 'Field AT Gun', 'Field Cannon', 'Field Gun', 'Field Launcher', 'Field Machine Gun', 'Field Mortar', 'Gunboat', 'Half-Track', 'Heavy Field Cannon', 'Heavy Field Gun', 'Infantry Car', 'Light Infantry Tank', 'Light Tank', 'Long-Range Artillery Car', 'Scout Tank', 'Siege Tank', 'Super Tank', 'Tankette']


## This function is used to check if the vehicle name
def check_name_validity(vehicle_name: str) -> tuple or None:
    with open('modules/vehicles_stats/vehicles_names_data/vehicles_names.json') as tank_names_file:
        tank_names = json.load(tank_names_file)

    for tank_key in tank_names:
        if vehicle_name in tank_names[tank_key]:
            return tank_key, tank_names[tank_key][-1]

    return None


## This function is used to retrieve the health of a vehicle on the wiki health page
def scrap_health_page(vehicle_name: str) -> dict:
    vehicle_health_stats = dict()
    page = requests.get('https://foxhole.wiki.gg/wiki/Vehicle_Health')
    soup = BeautifulSoup(page.content, 'html.parser')
    tbody_list = soup.find_all('tbody')

    for tbody in tbody_list:
        for tr in tbody.find_all('tr'):
            td_list = list(tr.find_all('td'))
            if len(td_list) == 0: # This prevents errors from the first row of the 'tr' which is categories names
                continue
            if td_list[1].text.strip() == vehicle_name[0]:
                vehicle_health_stats['HP'] = td_list[3].text.strip()
                vehicle_health_stats['Kinetic'] = dict()
                vehicle_health_stats['Explosive'] = dict()
                vehicle_health_stats['Armour Piercing'] = dict()
                vehicle_health_stats['AT Explosive'] = dict()

                vehicle_health_stats['Kinetic']['<:9mm:1088823410412503141>'] = f"{td_list[4].get_text(' **|** ')}"
                vehicle_health_stats['Kinetic']['<:792mm:1088823653027815424>'] = f"{td_list[5].get_text(' **|** ')}"
                vehicle_health_stats['Kinetic']['<:762mm:1088823887510388959>'] = f"{td_list[6].get_text(' **|** ')}"
                vehicle_health_stats['Kinetic']['<:127mm:1088826018883719281>'] = f"{td_list[8].get_text(' **|** ')}"
                vehicle_health_stats['Kinetic']['<:20mm:1088826350850281492>'] = f"{td_list[13].get_text(' **|** ')}"

                vehicle_health_stats['Explosive']['<:mamon:1088827447128109146>'] = f"{td_list[14].get_text(' **|** ')}"
                vehicle_health_stats['Explosive']['<:tremola:1088827774787125349>'] = f"{td_list[15].get_text(' **|** ')}"
                vehicle_health_stats['Explosive']['<:30mm:1077033326407335956>'] = f"{td_list[16].get_text(' **|** ')}"
                vehicle_health_stats['Explosive']['<:rpg:1088828056073945179>'] = f"{td_list[17].get_text(' **|** ')}"
                vehicle_health_stats['Explosive']['<:40mm:1077032968310239292>'] = f"{td_list[18].get_text(' **|** ')}"
                vehicle_health_stats['Explosive']['<:75mm:1077033155749482546>'] = f"{td_list[19].get_text(' **|** ')}"
                vehicle_health_stats['Explosive']['<:flask:1088831037766893669>'] = f"{td_list[31].get_text(' **|** ')}"
                vehicle_health_stats['Explosive']['<:sticky:1088831015964909749>'] = f"{td_list[32].get_text(' **|** ')}"
                vehicle_health_stats['Explosive']['<:landmine:1088831369762848850>'] = f"{td_list[33].get_text(' **|** ')}"

                vehicle_health_stats['Armour Piercing']['<:ignifist:1088829111859949619>'] = f"{td_list[26].get_text(' **|** ')}"
                vehicle_health_stats['Armour Piercing']['<:aprpg:1088829901341212693>'] = f"{td_list[27].get_text(' **|** ')}"
                vehicle_health_stats['Armour Piercing']['<:68mm:1077033006881063003>'] = f"{td_list[28].get_text(' **|** ')}"
                vehicle_health_stats['Armour Piercing']['<:arcrpg:1088830211799392316>'] = f"{td_list[29].get_text(' **|** ')}"
                vehicle_health_stats['Armour Piercing']['<:94mm:1077033020856483880>'] = f"{td_list[30].get_text(' **|** ')}"

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
    vehicle_box = soup.find('aside', attrs={'class': re.compile('portable-infobox noexcerpt pi-background pi-theme-(War|Col|Both) pi-layout-default pi-type-vehicle')}) # War and Warden because of the outdated thornfall wiki page

    # Get the icon for the thumbnail
    vehicle_stats['icon'] = f"https://foxhole.wiki.gg{vehicle_box.find('img')['src']}"

    # Get the vehicle's description
    description_box = soup.find('table', attrs={'style': 'background:transparent'})
    for tag in description_box.find_all('i'):
        if tag.parent.name == 'td':
            vehicle_stats['description'] = tag.text
            break

    # Get stats from the vehicle's wiki page
    for stat in vehicle_box.find_all('h3'):
        if stat.text in general_stats:
            vehicle_stats['general'][stat.text] = stat.findNext('div', attrs={'class': 'pi-data-value pi-font'}).text
    all_sections = vehicle_box.find_all('section', attrs={'class': 'pi-item pi-panel pi-border-color'})
    armament_section = all_sections[0]

    if vehicle_stats['general']['Vehicle Type'] in MILITARY_VEHICLE:
        # Get armament stats from the wiki page
        for div in armament_section.find_all('div', attrs={'class': 'pi-section-content'}): # this retrieve the armament divs
            all_armament_category = div.find_all('h3', attrs={'class': 'pi-data-label pi-secondary-font'})
            all_armament_type = div.find_all('div', attrs={'class': 'pi-data-value pi-font'})
            if all_armament_type[0].text == 'Commander':
                break
            vehicle_stats['armament'][all_armament_type[0].text] = dict()
            for i in range(len(all_armament_type)):
                if all_armament_category[i].text != 'Name':
                    vehicle_stats['armament'][all_armament_type[0].text][all_armament_category[i].text] = all_armament_type[i].get_text(separator=' | ')

    return vehicle_stats
