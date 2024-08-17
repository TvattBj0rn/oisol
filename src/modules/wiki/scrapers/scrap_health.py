import requests
from bs4 import BeautifulSoup, Tag
from typing import Optional
from src.utils.oisol_enums import Faction


def get_indexes(tbody: Tag) -> dict:
    indexes_dict = dict()
    for i, category in enumerate(tbody.select('tr > th')):
        indexes_dict[i] = category.select_one('a')['title'] if category.has_attr('style') else category.get_text(strip=True)
    return indexes_dict


def get_index_from_name(headers_indexes: dict) -> int:
    for index, value in headers_indexes.items():
        if value == 'Name':
            return index


def get_entry_row(tbody: Tag, headers_indexes: dict, name: str) -> Optional[Tag]:
    for tr in tbody.select('tr'):
        if tr.findChild('th'):
            continue
        name_index = get_index_from_name(headers_indexes)
        if tr.select('td')[name_index].get_text(strip=True) in [name, name.removesuffix(' (Battleship)')]:
            return tr


def extract_td_data(td: Tag) -> dict | str:
    if td.findChild('img'):
        return f"https://foxhole.wiki.gg{td.findChild('img')['src']}"
    if len(td.findChildren('hr')) == 1:
        hmtk = td.get_text(strip=True, separator=' ').split()
        return {'Disabled': hmtk[0], 'Kill': hmtk[1]}
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

    # List of ammo type that will never be used for any entry
    for k in [
        '7.62mm',
        '7.92mm',
        '9mm',
        'A3 Harpa Fragmentation Grenade',
        'Flamethrower Ammo',
        'Flame Ammo',
        'Shrapnel Mortar Shell',
        'Bomastone Grenade'
    ]:
        wiki_response_dict.pop(k, None)

    # In case we are checking for a building but 2 values were retrieved in HP
    if 'Class' not in wiki_response_dict.keys() and isinstance(wiki_response_dict['HP'], dict):
        wiki_response_dict['HP']['Health'] = wiki_response_dict['HP'].pop('Disabled')
        wiki_response_dict['HP']['Entrenched'] = wiki_response_dict['HP'].pop('Kill')

    return wiki_response_dict


def scrap_main_picture(url: str, name: str) -> tuple[Optional[str], Optional[int]]:
    # Request to the given url, check if response is valid
    response = requests.get(url)
    if not response:
        return None, None

    # Whole page soup data
    soup = BeautifulSoup(response.content, features='lxml')
    faction_color = scrap_faction_color(soup)

    # In case we have more than one infobox on the same page, we want to retrieve the correct one
    for infobox in soup.select('aside'):
        if not infobox.has_attr('h2'):
            continue
        if infobox.select_one('h2').get_text() == name:
            return f"https://foxhole.wiki.gg{infobox.select_one('figure > a > img')['src']}", faction_color

    return f"https://foxhole.wiki.gg{soup.select_one('aside > figure > a > img')['src']}", faction_color


def scrap_faction_color(soup: Tag) -> hex:
    infobox_soup = soup.select_one('aside')
    merged_class = set(infobox_soup['class'])
    if 'pi-theme-Col' in merged_class:
        return Faction.COLONIAL.value
    elif 'pi-theme-War' in merged_class:
        return Faction.WARDEN.value
    return Faction.NEUTRAL.value
