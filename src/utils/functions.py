from __future__ import annotations

import configparser
import operator
from configparser import ConfigParser
from sqlite3 import Connection

from discord import Role

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

def get_user_access_level(
        conn: Connection,
        user_roles: list[Role],
        guild_id: str,
        channel_id: str,
        message_id: str,
) -> int:
    """
    Retrieve interface roles to compare the user's roles
    :param conn: Connection object from caller with context
    :param user_roles: user discord roles
    :param guild_id: interaction guild id
    :param channel_id: interaction channel id
    :param message_id: interaction message id
    :return: an integer corresponding to the user's level of access on interface
    """
    # Get all user roles ids to compare with the interface roles
    user_roles_ids = {role.id for role in user_roles}

    # Retrieve the roles ids & access levels of the interface
    all_interface_permissions = conn.cursor().execute(
        'SELECT DiscordId, Level FROM GroupsInterfacesAccess WHERE GroupId == ? AND ChannelId == ? AND MessageId = ?',
        (guild_id, int(channel_id), message_id),
    ).fetchall()

    # Get user level of access on this interface
    user_level = 1
    for role_id, access_level in all_interface_permissions:
        if int(role_id) in user_roles_ids and access_level > user_level:
            user_level = access_level
        if user_level == 5:  # The user has the maximum level of access, no need to iterate further
            break
    return user_level
