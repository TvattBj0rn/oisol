import configparser
import operator
from configparser import ConfigParser

from .oisol_enums import Faction, Language, Shard


def safeguarded_nickname(nickname: str) -> str:
    """
    Function required as discord does not allow for nicknames longer than 32 characters.
    :param nickname: wanted name
    :return: nickname equal or shortened to 32 chars
    """
    return nickname[:32 - len(nickname)] if len(nickname) > 32 else nickname


def repair_default_config_dict(current_config: ConfigParser | None = None) -> ConfigParser:
    """
    Function that updates the configuration of a given config file by completing the missing values with the expected
    default values. If not config is passed as parameter, the function will return the default config file.
    :param current_config: Optional current config file to update.
    :return: update default config file.
    """
    final_config = configparser.ConfigParser()

    section_name = 'default'
    final_config.add_section(section_name)
    final_config.set(section_name, 'language', Language.EN.name if not current_config or not current_config.has_option(section_name, 'language') else current_config.get(section_name, 'language'))
    final_config.set(section_name, 'shard', Shard.ABLE.name if not current_config or not current_config.has_option(section_name, 'shard') else current_config.get(section_name, 'shard'))

    section_name = 'register'
    final_config.add_section(section_name)
    final_config.set(section_name, 'input', '' if not current_config or not current_config.has_option(section_name, 'input') else current_config.get(section_name, 'input'))
    final_config.set(section_name, 'output', '' if not current_config or not current_config.has_option(section_name, 'output') else current_config.get(section_name, 'output'))
    final_config.set(section_name, 'promoted_get_tag', 'False' if not current_config or not current_config.has_option(section_name, 'promoted_get_tag') else current_config.get(section_name, 'promoted_get_tag'))
    final_config.set(section_name, 'recruit_id', '' if not current_config or not current_config.has_option(section_name, 'recruit_id') else current_config.get(section_name, 'recruit_id'))

    section_name = 'regiment'
    final_config.add_section(section_name)
    final_config.set(section_name, 'faction', Faction.NEUTRAL.name if not current_config or not current_config.has_option(section_name, 'faction') else current_config.get(section_name, 'faction'))
    final_config.set(section_name, 'name', '' if not current_config or not current_config.has_option(section_name, 'name') else current_config.get(section_name, 'name'))
    final_config.set(section_name, 'tag', '' if not current_config or not current_config.has_option(section_name, 'tag') else current_config.get(section_name, 'tag'))

    return final_config


def get_highest_res_img_link(img_path: str) -> str:
    """
    Create a link with the given img path. If the given image is a thumbnail, a pattern is applied to get the full res path
    :param img_path: internal picture path
    :return: external link to the correct picture
    """
    return '/'.join(f'https://foxhole.wiki.gg{img_path}'.replace('/thumb', '').split('/')[:-1]) if '/thumb' in img_path else f'https://foxhole.wiki.gg{img_path}'


def sort_nested_dicts_by_key(input_dict: dict) -> dict:
    return {
        k: sort_nested_dicts_by_key(v) if isinstance(v, dict) else v for k, v in sorted(
            input_dict.items(),
            key=operator.itemgetter(0),
        )
    }


def convert_time_to_readable_time(value: float) -> str:
    """
    Take a float time value and converts it to a readable format.
    e.g -> 72.345 will return '72:20:42'
    :param value: float time value to convert
    :return: string readable time value
    """
    seconds = value * 3600
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return f'{int(h)}:{int(m):02d}:{int(s):02d}h'
