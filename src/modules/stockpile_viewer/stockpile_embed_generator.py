import discord
import os
import pathlib
from src.utils.CsvHandler import CsvHandler
from src.utils.oisol_enums import Faction, EmbedIds, DataFilesPath, Modules
from src.utils.resources import REGIONS_STOCKPILES


def get_sorted_stockpiles(guild_id: str, csv_keys: list) -> (list, dict):
    data_file_path = os.path.join(pathlib.Path('/'), 'oisol', guild_id, DataFilesPath.STOCKPILES.value)
    stockpiles_list = CsvHandler(csv_keys).csv_get_all_data(data_file_path, Modules.STOCKPILE)
    sorted_stockpiles = dict()

    print(stockpiles_list)

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
    print(sorted_regions_list, sorted_stockpiles)
    return sorted_regions_list, sorted_stockpiles


# Split in several function instead of one big function of ~40 lines
def generate_view_stockpile_embed(interaction: discord.Interaction, csv_keys: list) -> discord.Embed:
    sorted_regions_list, sorted_stockpiles = get_sorted_stockpiles(str(interaction.guild.id), csv_keys)

    embed = discord.Embed(
        title=f'Stockpiles | <:region:1130915923704946758>',
        color=Faction.WARDEN.value
    )
    embed.set_footer(text=EmbedIds.STOCKPILES_VIEW.value)
    for region in sorted_regions_list:
        sorted_subregion_list = list(sorted_stockpiles[region].keys())
        sorted_subregion_list.sort()
        embed.add_field(
            name=f'⠀\n{region.upper()}',
            value='',
            inline=False
        )

        for subregion in sorted_subregion_list:
            subregion_stockpiles_values = ''
            for stockpile in sorted_stockpiles[region][subregion]:
                subregion_stockpiles_values = f"{stockpile['name']} **|** {stockpile['code']}" if not subregion_stockpiles_values else subregion_stockpiles_values + f"\n{stockpile['name']} **|** {stockpile['code']}"

            subregion_icon = ''
            for subregion_tuple in REGIONS_STOCKPILES[region]:
                if subregion_tuple[0] == subregion:
                    subregion_icon = subregion_tuple[1]

            embed.add_field(
                name=f'{subregion_icon} **|** {subregion}',
                value=subregion_stockpiles_values,
                inline=False
            )

    return embed
