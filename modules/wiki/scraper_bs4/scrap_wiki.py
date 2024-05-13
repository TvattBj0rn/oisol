import unicodedata

import requests
from bs4 import BeautifulSoup, Tag


# TODO: specific cases to handle, all bridges, except field bridge, lk & mounted (we want deployed not item form)


def handle_specific_attribute(infobox_attribute_soup: Tag, attr_title: str) -> dict | str:
    attr_dict = dict()
    match attr_title:
        case 'Resistance(damage reduction)':
            attr_dict['type'] = infobox_attribute_soup.select('div[class^="pi-data-value pi-font"]')[0].get_text(strip=True).split('-')[0]
            for damage_reduction in infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > code'):
                attr_dict[damage_reduction.find('a')['title']] = damage_reduction.get_text(strip=True)
            return attr_dict
        case 'Subsystems disable chance':
            disable_chances = [f'{x}%' for x in infobox_attribute_soup.select('div[class^="pi-data-value pi-font"]')[0].get_text(strip=True).split('%') if x]
            subsystem_icon_soup = infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > a > img')
            for subsystem_index in range(len(subsystem_icon_soup)):
                attr_dict[subsystem_icon_soup[subsystem_index]['alt'].strip()] = disable_chances[subsystem_index]
            return attr_dict
        case 'Cost':
            if infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > p > span'):
                for cost in infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > p > span'):
                    attr_dict[cost.find('a')['title']] = cost.get_text(strip=True)
                if infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > p > a'):
                    attr_dict['chassis'] = f"""\nChassis: {infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > p > a')[0].get_text()}"""
                return attr_dict
            for cost in infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > span'):
                attr_dict[cost.find('a')['title']] = cost.get_text(strip=True)
            return attr_dict
        case 'Intel Icon' | 'Intel Icon (enemy)' | 'Map Icon' | 'Map Icon (allied)':
            return {infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > a > img')[0]['alt'].removesuffix('.png'): ''}
        case 'Construction Tool':
            if infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > span')[0].get_text(strip=True) == 'pressE':
                return {'': 'press E'}
            return {infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > span > a')[0]['title']: ''}
        case 'Repair Cost':
            return {'Basic Materials': infobox_attribute_soup.select('div[class^="pi-data-value pi-font"]')[0].get_text(strip=True)}
        case 'Fuel Capacity':
            attr_dict[''] = infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > a')[0].get_text(strip=True)
            for fuel in infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > span'):
                attr_dict[fuel.find('a')['title']] = ''
            return attr_dict
        case 'Ammo' | 'Ammunition':
            main_ammo = infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > a')[0].get_text(strip=True)
            attr_dict[main_ammo] = main_ammo
            for ammo in infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > p > a'):
                attr_dict[ammo.get_text(strip=True)] = ammo.get_text(strip=True)
            return attr_dict
        case 'Ammunition':
            return {infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > a')[0].get_text(strip=True): infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > a')[0].get_text(strip=True)}
        case 'Decay':
            decay = infobox_attribute_soup.select('div[class^="pi-data-value pi-font"]')[0].get_text().split('Duration: ')
            return f'{decay[0]}\nDuration: {decay[1]}'
        case _:
            return infobox_attribute_soup.select('div[class^="pi-data-value pi-font"]')[0].get_text(strip=True).replace(',', '\n')


def generate_infobox_data(infobox_soup: Tag, name: str) -> dict:
    # These two are constants, we expect them whatever the entry is
    data_dict = {
        'title': infobox_soup.find('h2', {'class': 'pi-item pi-item-spacing pi-title'}).get_text(),
        'img_url': f"https://foxhole.wiki.gg{infobox_soup.select('figure > a > img')[0]['src']}",
    }

    for infobox_attribute in infobox_soup.select('section > div'):
        attribute_title = infobox_attribute.select('h3')[0].get_text().strip()
        data_dict[attribute_title] = handle_specific_attribute(infobox_attribute, attribute_title)

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
        if name == wiki_response_dict['title']:
            wiki_response_dict['description'] = entry_desc
            return wiki_response_dict

    return dict()
