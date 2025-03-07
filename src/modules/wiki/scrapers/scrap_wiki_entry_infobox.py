import requests
from bs4 import BeautifulSoup, Tag

from src.utils import Faction, get_highest_res_img_link


def handle_specific_attribute(infobox_attribute_soup: Tag, attr_title: str) -> tuple:
    attr_dict = {}
    match attr_title:
        case 'Resistance(damage reduction)' | 'Resistance(damagereduction)':
            if damage_type_link := infobox_attribute_soup.select_one('div > a').get_text(strip=True):
                attr_dict['type'] = f'\n*{damage_type_link}*'
            else:  # This forces a value to 'type' and worst case nothing is displayed
                attr_dict['type'] = f'\n*{infobox_attribute_soup.find(string=True, recursive=False)}*'
            for damage_reduction in infobox_attribute_soup.select('div > div'):
                if resistance_type := damage_reduction.select_one('a').get('title', ''):
                    attr_dict[resistance_type] = reduction_percentage if (reduction_percentage := damage_reduction.get_text(strip=True)) else 'Immune'
            return 'Resistance (damage reduction)', attr_dict
        case 'Subsystemsdisable chance':
            disable_chances = [f'{x}%' for x in infobox_attribute_soup.get_text(strip=True).split('%') if x]
            subsystem_icon_soup = infobox_attribute_soup.select('a > img')
            for subsystem_index in range(len(subsystem_icon_soup)):
                attr_dict[subsystem_icon_soup[subsystem_index]['alt'].strip()] = disable_chances[subsystem_index]
            return 'Subsystems disable chance', attr_dict
        case 'Cost':
            if vehicle_cost := infobox_attribute_soup.select('p > span'):
                for cost in vehicle_cost:
                    attr_dict[cost.find('a')['title']] = cost.get_text(strip=True)
                if infobox_attribute_soup.select('p > a'):
                    attr_dict['chassis'] = f"""\nChassis: {infobox_attribute_soup.select_one('p > a').get_text()}"""
                return attr_title, attr_dict
            for cost in infobox_attribute_soup.select('span > span'):
                attr_dict[cost.select_one('a')['title']] = cost.parent.get_text(strip=True)
            return attr_title, attr_dict
        case 'IntelIcon' | 'MapIcon (allied)' | 'IntelIcon (enemy)':
            return 'Intel Icon', {infobox_attribute_soup.select_one('a > img')['alt'].removesuffix('.png'): 'Intel Icon'}
        case 'Construction Tool':
            if infobox_attribute_soup.select_one('span').get_text(strip=True) == 'pressE':
                return attr_title, {'': 'press E'}
            return attr_title, {infobox_attribute_soup.select_one('span > a')['title']: ''}
        case 'RepairCost':
            return 'Repair Cost', {'Basic Materials': infobox_attribute_soup.get_text(strip=True)}
        case 'Fuel Capacity':
            attr_dict['capacity'] = infobox_attribute_soup.select_one('a').get_text(strip=True)
            attr_dict['type'] = [fuel.find('a')['title'] for fuel in infobox_attribute_soup.select('span > span')]
            return attr_title, attr_dict
        case 'Ammo' | 'Ammunition':
            for ammo_type in infobox_attribute_soup.find_all('a'):
                if ammo_type_text := ammo_type.get_text(strip=True):  # There can be cases with empty text
                    attr_dict[ammo_type_text] = ammo_type_text
            return attr_title, attr_dict
        case 'Ammunition':
            return attr_title, {infobox_attribute_soup.select_one('a').get_text(strip=True): infobox_attribute_soup.select_one('a').get_text(strip=True)}
        case 'Decay':
            decay = infobox_attribute_soup.get_text().split('Duration: ')
            return attr_title, f'{decay[0]}\nDuration: {decay[1]}'
        case 'Encumbrance':
            if 'In backpack: ' in infobox_attribute_soup.get_text():
                encumbrance = infobox_attribute_soup.get_text().split('In backpack: ')
                return attr_title, f'{encumbrance[0]}\nIn backpack: {encumbrance[1]}'
            return attr_title, infobox_attribute_soup.get_text(strip=True).replace(',', '\n')
        case _:
            return attr_title, infobox_attribute_soup.get_text(strip=True).replace(',', '\n')


def generate_infobox_data(infobox_soup: Tag) -> dict:
    data_dict = {
        'title': infobox_soup.find('h2', {'class': 'pi-item pi-item-spacing pi-title'}).get_text(),
        'img_url': get_highest_res_img_link(infobox_soup.select_one('a > img')['src']),
        'attributes': {},
    }

    merged_class = infobox_soup['class']
    if 'pi-theme-Col' in merged_class:
        data_dict['color'] = Faction.COLONIAL.value
    elif 'pi-theme-War' in merged_class:
        data_dict['color'] = Faction.WARDEN.value
    else:
        data_dict['color'] = Faction.NEUTRAL.value

    for infobox_attribute in infobox_soup.select('section > div'):
        attribute_title, attribute_value = handle_specific_attribute(infobox_attribute.select_one('div[class^="pi-data-value pi-font"]'), infobox_attribute.select_one('h3').get_text(strip=True))
        data_dict['attributes'][attribute_title] = attribute_value

    return data_dict


def scrap_wiki(url: str, name: str) -> dict:
    # Request to the given url, check if response is valid
    response = requests.get(url, timeout=5)
    if not response:
        return {}

    # Whole page soup data
    soup = BeautifulSoup(response.content, features='lxml')

    # Description soup and retrieving (we make sure the description exists)
    desc_soup = soup.select_one('table > tbody > tr > td > i')
    entry_desc = desc_soup.get_text() if desc_soup else ''

    # Infobox handling within a function to allow for loop later on
    for infobox in soup.select('aside'):
        if not infobox.has_attr('class'):  # Asides without classes are ads
            continue
        wiki_response_dict = generate_infobox_data(infobox)
        if name != wiki_response_dict['title']:
            continue
        wiki_response_dict['description'] = entry_desc
        return wiki_response_dict
    return {}
