import requests
from bs4 import BeautifulSoup, Tag
from modules.utils import Faction
from typing import Optional


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
            print(f'found name: {name}')
            return tr


def extract_td_data(td: Tag) -> dict | str:
    # if not td.findChildren():

    if td.findChild('img'):
        return f"https://foxhole.wiki.gg{td.findChild('img')['src']}"
    if td.findChildren('hr'):
        hmtk = td.get_text(strip=True, separator=' ').split()
        return {'disabled': hmtk[0], 'kill': hmtk[1]}
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

    print(wiki_response_dict)
