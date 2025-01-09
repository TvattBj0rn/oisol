import requests
from bs4 import BeautifulSoup, Tag

from src.utils import DAMAGE_TYPES_ATTRIBUTION, Faction


def get_columns_order(tbody: Tag) -> list:
    """
    iterate over a header row of a tbody to get category order
    :param tbody:
    :return: list of categories using wiki order
    """
    # is an icon category if non-blank style else a title category
    return [category.select_one('a')['title'] if category.has_attr('style') and not category['style'].endswith('#000;') else category.get_text(strip=True) for category in tbody.select('tr > th')]


def get_entry_row(tbody: Tag, headers_indexes: list, name: str) -> Tag | None:
    """
    Check for an entry in a damage array (tbody).
    :param tbody: damage array
    :param headers_indexes: columns order
    :param name: entry name
    :return: row object of the entry within the array if the entry is found else None
    """
    for tr in tbody.select('tr'):
        if tr.findChild('th'):
            continue
        # It is assumed that Name will always be scrapped
        if tr.select('td')[headers_indexes.index('Name')].get_text(strip=True) in {name, name.removesuffix(' (Battleship)')}:
            return tr
    return None


def extract_td_data(td: Tag, column_name: str) -> dict | str | tuple:
    if img_path := td.findChild('img'):
        highest_res_img_path = '/'.join(f'https://foxhole.wiki.gg{img_path['src']}'.replace('/thumb', '').split('/')[:-1]) if '/thumb' in img_path['src'] else f'https://foxhole.wiki.gg{img_path['src']}'
        # Structures array format
        if not column_name:
            return highest_res_img_path
        # Vehicles array format
        return td.findChild('a').get_text(strip=True), highest_res_img_path
    # Case for vehicles
    if len(td.findChildren('hr')) == 1:
        hmtk = td.get_text(strip=True, separator=' ').split()
        return {'Disabled': hmtk[0], 'Kill': hmtk[1]}
    # Case for 3-typed structures
    if len(td.findChildren('hr')) == 2:
        hmtk = td.get_text(strip=True, separator=' ').split()
        return {'S': hmtk[0], 'M': hmtk[1], 'L': hmtk[2]}
    return td.get_text(strip=True)


def scrap_health(url: str, name: str) -> dict:
    wiki_response_dict = {}
    # Request to the given url, check if response is valid
    response = requests.get(url)
    if not response:
        return {}

    # Whole page soup data
    soup = BeautifulSoup(response.content, features='lxml')

    header_indexes = []
    row = None

    # There are multiple tbody in a page
    for tbody in soup.select('tbody'):
        header_indexes = get_columns_order(tbody)
        row = get_entry_row(tbody, header_indexes, name)
        if row:
            break
    # Entry was not found in the wiki
    if not row:
        return {}
    for i, td in enumerate(row.select('td')):
        extracted_data = extract_td_data(td, header_indexes[i])
        if isinstance(extracted_data, tuple):
            wiki_response_dict[header_indexes[i]] = extracted_data[0]
            wiki_response_dict[''] = extracted_data[1]
        else:
            wiki_response_dict[header_indexes[i]] = extract_td_data(td, header_indexes[i])
    # In case we are checking for a building but 2 values were retrieved in HP
    if (
            'Class' not in wiki_response_dict
            and isinstance(wiki_response_dict['HP'], dict)
            and len(wiki_response_dict['HP'].keys()) == 2
    ):
        wiki_response_dict['HP']['Health'] = wiki_response_dict['HP'].pop('Disabled')
        wiki_response_dict['HP']['Entrenched'] = wiki_response_dict['HP'].pop('Kill')

    final_response_dict = {k: wiki_response_dict.pop(k) for k in ['', 'Icon', 'Name', 'Class', 'HP'] if k in wiki_response_dict} | {'Damage': {}}
    for k, v in wiki_response_dict.items():
        if DAMAGE_TYPES_ATTRIBUTION[k] not in final_response_dict['Damage']:
            final_response_dict['Damage'][DAMAGE_TYPES_ATTRIBUTION[k]] = {k: v}
        else:
            final_response_dict['Damage'][DAMAGE_TYPES_ATTRIBUTION[k]].update({k: v})

    return final_response_dict


def scrap_main_picture(url: str, name: str) -> tuple:
    # Request to the given url, check if response is valid
    response = requests.get(url)
    if not response:
        return None, None

    # Whole page soup data
    soup = BeautifulSoup(response.content, features='lxml')
    faction_color = scrap_faction_color(soup)

    # In case we have more than one infobox on the same page, we want to retrieve the correct one
    for infobox in soup.select('aside'):
        if not infobox.findChild('h2'):
            continue
        if infobox.select_one('h2').get_text() == name:
            return f"https://foxhole.wiki.gg{infobox.select_one('a > img')['src']}", faction_color

    # If we have a single infobox
    return f"https://foxhole.wiki.gg{soup.select_one('aside').select_one('a > img')['src']}", faction_color


def scrap_faction_color(soup: Tag) -> hex:
    infobox_soup = soup.select_one('aside')
    merged_class = set(infobox_soup['class'])
    if 'pi-theme-Col' in merged_class:
        return Faction.COLONIAL.value
    if 'pi-theme-War' in merged_class:
        return Faction.WARDEN.value
    return Faction.NEUTRAL.value
