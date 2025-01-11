import requests
from bs4 import BeautifulSoup, Tag

from src.utils import DAMAGE_TYPES_ATTRIBUTION, Faction, get_highest_res_img_link


def get_columns_order(tbody: Tag) -> list:
    """
    iterate over a header row of a tbody to get category order
    :param tbody: damage array
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


def extract_td_data(td: Tag) -> dict | str | tuple:
    """
    Analyse a specific column of a row and returns its formatted value
    :param td: specific column
    :return: formatted td value
    """
    if (img_path := td.findChild('img')) and img_path.has_attr('src'):
        return td.findChild('a').get_text(strip=True), get_highest_res_img_link(img_path['src'])
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
    """
    Generate data from a user given url
    :param url: wiki page url
    :param name: name of the entry
    :return: dict of entry parameters
    """
    # Request to the given url, check if response is valid
    response = requests.get(url)
    if not response:
        return {}

    wiki_response_dict = {}
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
    # If a row is faction colored, it is selected
    if row.has_attr('style'):
        if 'foxhole-colonial-color' in row['style']:
            wiki_response_dict['Color'] = Faction.COLONIAL.value
        elif 'foxhole-warden-color' in row['style']:
            wiki_response_dict['Color'] = Faction.WARDEN.value
    # Faction neutral row / no color
    if 'Color' not in wiki_response_dict:
        wiki_response_dict['Color'] = Faction.NEUTRAL.value

    for i, td in enumerate(row.select('td')):
        extracted_data = extract_td_data(td)
        if isinstance(extracted_data, tuple):
            wiki_response_dict[header_indexes[i]] = extracted_data[0]
            wiki_response_dict['img_url'] = extracted_data[1]
        else:
            wiki_response_dict[header_indexes[i]] = extracted_data
    # In case we are checking for a building but 2 values were retrieved in HP
    if (
            'Class' not in wiki_response_dict
            and isinstance(wiki_response_dict['HP'], dict)
            and len(wiki_response_dict['HP'].keys()) == 2
    ):
        wiki_response_dict['HP']['Health'] = wiki_response_dict['HP'].pop('Disabled')
        wiki_response_dict['HP']['Entrenched'] = wiki_response_dict['HP'].pop('Kill')

    final_response_dict = {k: wiki_response_dict.pop(k) for k in ['img_url', 'Icon', 'Name', 'Class', 'HP', 'Color'] if k in wiki_response_dict} | {'Damage': {}}
    for k, v in wiki_response_dict.items():
        if DAMAGE_TYPES_ATTRIBUTION[k] not in final_response_dict['Damage']:
            final_response_dict['Damage'][DAMAGE_TYPES_ATTRIBUTION[k]] = {k: v}
        else:
            final_response_dict['Damage'][DAMAGE_TYPES_ATTRIBUTION[k]].update({k: v})

    print(final_response_dict)
    return final_response_dict
