import requests
from bs4 import BeautifulSoup, Tag

from src.utils import Faction, get_highest_res_img_link


def handle_specific_attribute(infobox_attribute_soup: Tag, attr_title: str) -> dict | str:
    attr_dict = {}
    match attr_title:
        case 'Resistance(damage reduction)':
            attr_dict['type'] = f"\n{infobox_attribute_soup.get_text(strip=True).split('-')[0]}"
            for damage_reduction in infobox_attribute_soup.select('code'):
                attr_dict[damage_reduction.find('a')['title']] = f' | {damage_reduction.get_text(strip=True)}'
            return attr_dict
        case 'Subsystems disable chance':
            disable_chances = [f'{x}%' for x in infobox_attribute_soup.get_text(strip=True).split('%') if x]
            subsystem_icon_soup = infobox_attribute_soup.select('a > img')
            for subsystem_index in range(len(subsystem_icon_soup)):
                attr_dict[subsystem_icon_soup[subsystem_index]['alt'].strip()] = disable_chances[subsystem_index]
            return attr_dict
        case 'Cost':
            if infobox_attribute_soup.select('p > span'):
                for cost in infobox_attribute_soup.select('p > span'):
                    attr_dict[cost.find('a')['title']] = cost.get_text(strip=True)
                if infobox_attribute_soup.select('p > a'):
                    attr_dict['chassis'] = f"""\nChassis: {infobox_attribute_soup.select_one('p > a').get_text()}"""
                return attr_dict
            for cost in infobox_attribute_soup.select('span'):
                attr_dict[cost.find('a')['title']] = cost.get_text(strip=True)
            return attr_dict
        case 'Intel Icon' | 'Intel Icon (enemy)' | 'Map Icon' | 'Map Icon (allied)':
            return {infobox_attribute_soup.select_one('a > img')['alt'].removesuffix('.png'): ''}
        case 'Construction Tool':
            if infobox_attribute_soup.select_one('span').get_text(strip=True) == 'pressE':
                return {'': 'press E'}
            return {infobox_attribute_soup.select_one('span > a')['title']: ''}
        case 'Repair Cost':
            return {'Basic Materials': infobox_attribute_soup.get_text(strip=True)}
        case 'Fuel Capacity':
            attr_dict[''] = infobox_attribute_soup.select_one('a').get_text(strip=True)
            for fuel in infobox_attribute_soup.select('span'):
                attr_dict[fuel.find('a')['title']] = ''
            return attr_dict
        case 'Ammo' | 'Ammunition':
            for ammo_type in infobox_attribute_soup.findChildren('a'):
                ammo_type_text = ammo_type.get_text()
                attr_dict[ammo_type_text] = ammo_type_text
            return attr_dict
        case 'Ammunition':
            return {infobox_attribute_soup.select_one('a').get_text(strip=True): infobox_attribute_soup.select_one('a').get_text(strip=True)}
        case 'Decay':
            decay = infobox_attribute_soup.get_text().split('Duration: ')
            return f'{decay[0]}\nDuration: {decay[1]}'
        case 'Encumbrance':
            if 'In backpack: ' in infobox_attribute_soup.get_text():
                encumbrance = infobox_attribute_soup.get_text().split('In backpack: ')
                return f'{encumbrance[0]}\nIn backpack: {encumbrance[1]}'
            return infobox_attribute_soup.get_text(strip=True).replace(',', '\n')
        case _:
            return infobox_attribute_soup.get_text(strip=True).replace(',', '\n')


def generate_infobox_data(infobox_soup: Tag) -> dict:
    data_dict = {
        'title': infobox_soup.find('h2', {'class': 'pi-item pi-item-spacing pi-title'}).get_text(),
        'img_url': get_highest_res_img_link(infobox_soup.select_one('a > img')['src']),
    }

    merged_class = infobox_soup['class']
    if 'pi-theme-Col' in merged_class:
        data_dict['color'] = Faction.COLONIAL.value
    elif 'pi-theme-War' in merged_class:
        data_dict['color'] = Faction.WARDEN.value
    else:
        data_dict['color'] = Faction.NEUTRAL.value

    for infobox_attribute in infobox_soup.select('section > div'):
        attribute_title = infobox_attribute.select('h3')[0].get_text()
        data_dict[attribute_title] = handle_specific_attribute(infobox_attribute.select_one('div[class^="pi-data-value pi-font"]'), attribute_title)

    return data_dict


def scrap_wiki(url: str, name: str) -> dict:
    # Request to the given url, check if response is valid
    response = requests.get(url)
    if not response:
        return {}

    # Whole page soup data
    soup = BeautifulSoup(response.content, features='lxml')

    # Description soup and retrieving (we make sure the description exists)
    desc_soup = soup.select_one('table > tbody > tr > td > i')
    entry_desc = desc_soup.get_text() if desc_soup else ''

    # Infobox handling within a function to allow for loop later on
    for infobox in soup.select('aside[class^="portable-infobox noexcerpt pi-background"]'):
        wiki_response_dict = generate_infobox_data(infobox)
        if name in {wiki_response_dict['title'], f'{wiki_response_dict['title']} (Tier 1)', f'{wiki_response_dict['title']} (Battleship)'}:
            wiki_response_dict['description'] = entry_desc
            return wiki_response_dict

    return {}
