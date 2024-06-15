import requests
from bs4 import BeautifulSoup, Tag
from typing import Optional, Tuple
from modules.utils import Faction


def get_indexes(tbody: Tag) -> dict:
    indexes_dict = dict()
    for i, category in enumerate(tbody.select('tr > th')):
        indexes_dict[i] = category.select_one('a')['title'] if category.has_attr('style') else category.get_text(strip=True)
    return indexes_dict


def get_index_from_name(headers_indexes: dict) -> int:
    for name, age in headers_indexes.items():
        if age == 'Name':
            return name


def get_entry_row(tbody: Tag, headers_indexes: dict, name: str) -> Optional[Tag]:
    for tr in tbody.select('tr'):
        if tr.findChild('th'):
            continue
        name_index = get_index_from_name(headers_indexes)
        if tr.select('td')[name_index].get_text(strip=True) == name:
            return tr


def extract_td_data(td: Tag) -> dict | str:
    # if not td.findChildren():

    if td.findChild('img'):
        return f"https://foxhole.wiki.gg{td.findChild('img')['src']}"
    if len(td.findChildren('hr')) == 1:
        hmtk = td.get_text(strip=True, separator=' ').split()
        return {'disabled': hmtk[0], 'kill': hmtk[1]}
    if len(td.findChildren('hr')) == 2:
        hmtk = td.get_text(strip=True, separator=' ').split()
        return {'S': hmtk[0], 'M': hmtk[1], 'L': hmtk[2]}
    return td.get_text(strip=True)


def scrap_health(url: str, name: str) -> dict:
    wiki_response_dict = {}
    # Request to the given url, check if response is valid
    response = requests.get(url)
    if not response:
        return dict()

    # Whole page soup data
    soup = BeautifulSoup(response.content, features="lxml")

    header_indexes = dict()
    row = None

    for tbody in soup.select('tbody'):
        header_indexes = get_indexes(tbody)
        row = get_entry_row(tbody, header_indexes, name)
        if row:
            break
    if not row:
        return dict()

    for i, td in enumerate(row.select('td')):
        wiki_response_dict[header_indexes[i]] = extract_td_data(td)

    for k in ['7.62mm', '7.92mm', '9mm', 'A3 Harpa Fragmentation Grenade', 'Flamethrower Ammo', 'Flame Ammo', 'Shrapnel Mortar Shell', 'Bomastone Grenade']:
        wiki_response_dict.pop(k, None)
    print(wiki_response_dict)
    return wiki_response_dict


def scrap_main_picture(url: str) -> Optional[Tuple[str, int]]:
    # Request to the given url, check if response is valid
    response = requests.get(url)
    if not response:
        return None

    # Whole page soup data
    soup = BeautifulSoup(response.content, features="lxml")
    return f"https://foxhole.wiki.gg{soup.select_one('aside > figure > a > img')['src']}", scrap_faction_color(soup)


def scrap_faction_color(soup: Tag) -> hex:
    infobox_soup = soup.select_one('aside')
    merged_class = set(infobox_soup['class'])
    if 'pi-theme-Col' in merged_class:
        return Faction.COLONIAL.value
    elif 'pi-theme-War' in merged_class:
        return Faction.WARDEN.value
    return Faction.NEUTRAL.value
