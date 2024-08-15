import configparser

import discord
import os
import pathlib
from src.utils.CsvHandler import CsvHandler
from src.utils.oisol_enums import Faction, EmbedIds, DataFilesPath
from src.utils.resources import REGIONS_STOCKPILES


def get_sorted_stockpiles(guild_id: int, csv_keys: list) -> (list, dict):
    data_file_path = os.path.join(pathlib.Path('/'), 'oisol', str(guild_id), DataFilesPath.STOCKPILES.value)
    stockpiles_list = CsvHandler(csv_keys).csv_get_all_data(data_file_path)
    sorted_stockpiles = dict()

    for stockpile in stockpiles_list:
        if not stockpile['region'] in sorted_stockpiles.keys():
            sorted_stockpiles[stockpile['region']] = {stockpile['subregion']: [stockpile]}
        else:
            if not stockpile['subregion'] in sorted_stockpiles[stockpile['region']].keys():
                sorted_stockpiles[stockpile['region']][stockpile['subregion']] = [stockpile]
            else:
                sorted_stockpiles[stockpile['region']][stockpile['subregion']].append(stockpile)

    sorted_regions_list = list(sorted_stockpiles.keys())
    sorted_regions_list.sort()
    return sorted_regions_list, sorted_stockpiles


def generate_view_stockpile_embed(interaction: discord.Interaction, csv_keys: list) -> discord.Embed:
    config = configparser.ConfigParser()
    config.read(os.path.join('/', 'oisol', str(interaction.guild_id), DataFilesPath.CONFIG.value))
    sorted_regions_list, sorted_stockpiles = get_sorted_stockpiles(interaction.guild_id, csv_keys)
    embed_fields = []
    for region in sorted_regions_list:
        sorted_subregion_list = list(sorted_stockpiles[region].keys())
        sorted_subregion_list.sort()
        embed_fields.append(
            {
                'name': f'⠀\n{region.upper()}',
                'value': '',
                'inline': False
            }
        )

        for subregion in sorted_subregion_list:
            subregion_stockpiles_values = ''
            for stockpile in sorted_stockpiles[region][subregion]:
                subregion_stockpiles_values = f"{stockpile['name']} **|** {stockpile['code']}" if not subregion_stockpiles_values else subregion_stockpiles_values + f"\n{stockpile['name']} **|** {stockpile['code']}"

            subregion_icon = ''
            for subregion_tuple in REGIONS_STOCKPILES[region]:
                if subregion_tuple[0] == subregion:
                    match config['regiment']['faction']:
                        case 'WARDEN':
                            subregion_icon = subregion_tuple[2]
                        case 'COLONIAL':
                            subregion_icon = subregion_tuple[3]
                        case 'NEUTRAL' | _:  # Neutral is specified for readability
                            subregion_icon = subregion_tuple[1]
                    break

            embed_fields.append(
                {
                    'name': f'{subregion_icon} **|** {subregion}',
                    'value': subregion_stockpiles_values,
                    'inline': False
                }
            )

    return discord.Embed().from_dict(
        {
            'title': f'Stockpiles | <:region:1130915923704946758>',
            'color': Faction[config['regiment']['faction']].value,
            'footer': {'text': EmbedIds.STOCKPILES_VIEW.value},
            'fields': embed_fields
        }
    )
