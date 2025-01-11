import re

import requests
from bs4 import BeautifulSoup, Tag

from src.utils import EMOJIS_FROM_DICT, Faction


def scrap_production(url: str) -> dict:
    """
    Generate data from a user given url
    :param url: wiki page url
    :return: dict of entry parameters
    """

    # Request to the given url, check if response is valid
    response = requests.get(url)
    if not response:
        return {}

    # Whole page soup data
    soup = BeautifulSoup(response.content, features='lxml')

    # Find Production or Acquisition title and grab the next table (production table)
    production_wikitable = soup.find('h2', text=('Production', 'Acquisition')).find_next_sibling('table')
    wiki_response_dict = {column_name.get_text(strip=True): [] for column_name in production_wikitable.find('tr').find_all('th')}

    # Iterate on rows that are not the title columns
    for tr in production_wikitable.find('tr').find_next_siblings('tr'):
        tr: Tag  # for type hinting
        if 'Color' not in wiki_response_dict and tr.has_attr('style'):
            if 'colonial-color' in tr['style']:
                wiki_response_dict['Color'] = Faction.COLONIAL.value
            elif 'warden-color' in tr['style']:
                wiki_response_dict['Color'] = Faction.WARDEN.value
        remover_pattern = r'^(\d+ )?(x )?(\d+ x )?(Crate of )?(\d+ x )?'
        for i, td in enumerate(tr.find_all('td')):
            td: Tag
            match i:
                # 0 -> Struct: name & icon
                case 0:
                    wiki_response_dict[list(wiki_response_dict.keys())[i]].append(
                        ((struct_name := td.select_one('a')['title']), EMOJIS_FROM_DICT.get(struct_name, struct_name)),
                    )
                # 1 -> Inputs split 'a' tags no children (text) & 'a' tags children (icon)
                case 1:
                    # second comprehension because there is at least one case of string operations generating empty strings
                    split_text = [x for x in [substr.replace('\xa0', ' ').strip() for substr in td.get_text(separator='\n').splitlines() if substr and substr != '\xa0'] if x]
                    wiki_response_dict[list(wiki_response_dict.keys())[i]].append(
                        [((input_row := ' '.join((x, y))), EMOJIS_FROM_DICT.get((item_name := re.sub(remover_pattern, '', input_row)), item_name)) for x, y in zip(split_text[::2], split_text[1::2], strict=True)],
                    )
            # 2 -> Outputs
                case 2:
                    split_text = [substr.replace('\xa0', ' ').strip() for substr in td.get_text(separator='\n').splitlines() if substr and substr != '\xa0']
                    if not len(split_text) % 2 and not split_text[0].strip().isdigit():
                        wiki_response_dict[list(wiki_response_dict.keys())[i]].append(
                            [(output_row := (' '.join((x, y))), re.sub(remover_pattern, '', output_row)) for x, y in zip(split_text[::2], split_text[1::2], strict=True)],
                        )
                    else:
                        wiki_response_dict[list(wiki_response_dict.keys())[i]].append(
                            [((output_row := ' '.join(split_text)), re.sub(remover_pattern, '', output_row))],
                        )
                # 3 -> Time column: get text (time or hammer hits)
                case 3:
                    wiki_response_dict[list(wiki_response_dict.keys())[i]].append(td.get_text(' ', strip=True))
    if 'Color' not in wiki_response_dict:
        wiki_response_dict['Color'] = Faction.NEUTRAL.value
    return wiki_response_dict
