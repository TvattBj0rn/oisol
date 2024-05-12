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
            subsystem_icon_soup = infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > a')
            for subsystem_index in range(len(subsystem_icon_soup)):
                attr_dict[subsystem_icon_soup[subsystem_index]['title'].strip()] = disable_chances[subsystem_index]
            return attr_dict
        case 'Cost':
            if infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > p > span'):
                for cost in infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > p > span'):
                    attr_dict[cost.find('a')['title']] = cost.get_text(strip=True)
                if infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > p > a'):
                    attr_dict['chassis'] = infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > p > a')[0].get_text()
                return attr_dict
            for cost in infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > span'):
                attr_dict[cost.find('a')['title']] = cost.get_text(strip=True)
            if infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > a'):
                attr_dict['chassis'] = infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > a')[0].get_text()
            return attr_dict
        case 'Intel Icon' | 'Intel Icon (enemy)':
            return {infobox_attribute_soup.select('div[class^="pi-data-value pi-font"] > a > img')[0]['alt'].removesuffix('.png'): ''}
        case _:
            return infobox_attribute_soup.select('div[class^="pi-data-value pi-font"]')[0].get_text(strip=True).replace(',', '\n')


def generate_infobox_data(infobox_soup: Tag, data_dict: dict) -> dict:
    # These two are constants, we expect them whatever the entry is
    data_dict['title'] = infobox_soup.find('h2', {'class': 'pi-item pi-item-spacing pi-title'}).get_text()
    data_dict['img_url'] = f"https://foxhole.wiki.gg{infobox_soup.select('figure > a > img')[0]['src']}"

    for infobox_attribute in infobox_soup.select('section > div'):
        attribute_title = infobox_attribute.select('h3')[0].get_text().strip()
        data_dict[attribute_title] = handle_specific_attribute(infobox_attribute, attribute_title)

    return data_dict


def scrap_wiki(url: str) -> dict:
    wiki_response_dict = {}

    # Request to the given url, check if response is valid
    response = requests.get(url)
    if not response:
        return dict()

    # Whole page soup data
    soup = BeautifulSoup(response.content, features="lxml")

    # Description soup and retrieving (we make sure the description exists)
    desc_soup = soup.select('table > tbody > tr > td > i')
    if desc_soup:
        wiki_response_dict['description'] = desc_soup[0].get_text()
    else:
        wiki_response_dict['description'] = ''

    # Infobox handling within a function to allow for loop later on
    infobox_soup = soup.select('aside[class^="portable-infobox noexcerpt pi-background"]')[0]
    wiki_response_dict = generate_infobox_data(infobox_soup, wiki_response_dict)

    return wiki_response_dict
