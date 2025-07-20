import configparser
import sqlite3
from datetime import datetime

from src.utils import (
    OISOL_HOME_PATH,
    DataFilesPath,
    Faction,
    FoxholeBuildings,
    sort_nested_dicts_by_key,
)


def get_stockpiles_list(association_id: str, message_id: int, group_faction: str) -> list:
    """
    :param association_id: interface group id
    :param message_id: interface message id
    :param group_faction: faction of the discord
    :return: list of fields used for discord.Embed creation
    """
    # Retrieve data from db
    with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
        guild_stockpiles = conn.cursor().execute(
            'SELECT Region, Subregion, Code, Name, Type FROM GroupsStockpilesList WHERE AssociationId == ?',
            (association_id,)
        ).fetchall()

    # Group stockpiles by regions
    grouped_stockpiles = {}
    for region, subregion, code, name, building_type in guild_stockpiles:
        if region not in grouped_stockpiles:
            grouped_stockpiles[region] = {}
        if f'{subregion}_{building_type}' not in grouped_stockpiles[region]:
            grouped_stockpiles[region][f'{subregion}_{building_type}'] = {}
        grouped_stockpiles[region][f'{subregion}_{building_type}'][name] = code

    # Sort all keys in dict and subdicts by key
    sorted_grouped_stockpiles = sort_nested_dicts_by_key(grouped_stockpiles)

    # Set stockpiles to discord fields format
    embed_fields = []
    for region, v in sorted_grouped_stockpiles.items():
        value_string = ''
        for subregion_type, vv in v.items():
            value_string += f'**{subregion_type.split('_')[0]}** ({FoxholeBuildings[f'{'_'.join(subregion_type.split('_')[1:])}_{group_faction}'].value})\n'
            for name, code in vv.items():
                value_string += f'{name} **|** {code}\n'
            value_string += '\n'
        embed_fields.append({'name': f'‎\n**__{region.upper()}__**', 'value': value_string, 'inline': True})

    return embed_fields


def get_stockpile_info(guild_id: int, association_id: str, *, interface_name: str | None = None, message_id: int | None = None) -> dict:
    """
    Retrieve information as embed format
    :param association_id: id of the interface group
    :param interface_name: name displayed on the interface
    :param guild_id: id of the discord
    :param message_id: id of the interface (message id)
    :return: formatted information as dict following embed format
    """
    stockpile_interface = {}

    # Header part
    if interface_name is not None:
        stockpile_interface['title'] = f'<:region:1130915923704946758> | Stockpiles | {interface_name}'
    else:
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            stockpile_interface['title'] = f'<:region:1130915923704946758> | Stockpiles | {cursor.execute(f'SELECT InterfaceName FROM AllInterfacesReferences WHERE MessageId == ?', (message_id,)).fetchone()[0]}'

    # Get group faction
    config = configparser.ConfigParser()
    config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{guild_id}.ini')

    group_faction = config.get('regiment', 'faction', fallback='NEUTRAL')
    stockpile_interface['color'] = Faction[group_faction].value
    stockpile_interface['timestamp'] = str(datetime.now())

    # Body part
    if message_id is not None:
        stockpile_interface['fields'] = get_stockpiles_list(association_id, message_id, group_faction)

    return stockpile_interface
