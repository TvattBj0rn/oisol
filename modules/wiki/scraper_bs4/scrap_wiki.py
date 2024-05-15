import unicodedata

import requests
from bs4 import BeautifulSoup, Tag


# TODO: specific cases to handle, all bridges, except field bridge, lk & mounted (we want deployed not item form)


def handle_specific_attribute(infobox_attribute_soup: Tag, attr_title: str) -> dict | str:
    attr_dict = dict()
    match attr_title:
        case 'Resistance(damage reduction)':
            attr_dict['type'] = infobox_attribute_soup.get_text(strip=True).split('-')[0]
            for damage_reduction in infobox_attribute_soup.select('code'):
                attr_dict[damage_reduction.find('a')['title']] = damage_reduction.get_text(strip=True)
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


def generate_infobox_data(infobox_soup: Tag, name: str) -> dict:
    # These two are constants, we expect them whatever the entry is
    data_dict = {
        'title': infobox_soup.find('h2', {'class': 'pi-item pi-item-spacing pi-title'}).get_text(),
        'img_url': f"https://foxhole.wiki.gg{infobox_soup.select('figure > a > img')[0]['src']}",
    }

    for infobox_attribute in infobox_soup.select('section > div'):
        attribute_title = infobox_attribute.select('h3')[0].get_text().strip()
        data_dict[attribute_title] = handle_specific_attribute(infobox_attribute.select_one('div[class^="pi-data-value pi-font"]'), attribute_title)

    return data_dict


def scrap_wiki(url: str, name: str) -> dict:
    wiki_response_dict = {}

    # Request to the given url, check if response is valid
    response = requests.get(url)
    if not response:
        return dict()

    # Whole page soup data
    soup = BeautifulSoup(response.content, features="lxml")

    # Description soup and retrieving (we make sure the description exists)
    desc_soup = soup.select('table > tbody > tr > td > i')
    entry_desc = desc_soup[0].get_text() if desc_soup else ''

    # Infobox handling within a function to allow for loop later on
    infoboxs_soup = soup.select('aside[class^="portable-infobox noexcerpt pi-background"]')
    for infobox in infoboxs_soup:
        wiki_response_dict = generate_infobox_data(infobox, name)
        if name == wiki_response_dict['title'] or name == f"{wiki_response_dict['title']} (Tier 1)":
            wiki_response_dict['description'] = entry_desc
            return wiki_response_dict

    return dict()
