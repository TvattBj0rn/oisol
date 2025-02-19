from __future__ import annotations

import configparser
import functools
import logging
import pathlib
import random
import re
from multiprocessing import Pool, cpu_count
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands, tasks

from src.utils import (
    OISOL_HOME_PATH,
    DataFilesPath,
    EmbedIds,
    Faction,
    FoxholeAPIWrapper,
    FoxholeBuildings,
    MapIcon,
    Shard,
    sort_nested_dicts_by_key,
    update_discord_interface,
)

if TYPE_CHECKING:
    from main import Oisol


@functools.lru_cache
def get_shard_stockpiles_subregions(bot: Oisol, shard_name: str, _code: str) -> list[str]:
    """
    :param bot: Oisol instance
    :param shard_name: Shard to pull the data from, either ABLE, BAKER or CHARLIE
    :param _code: Arbitrary value to detect new command run (new code means new stock means need to rerun the full func)
    :return: List of all available stockpiles in a given shard
    """
    stockpiles_subregions = bot.cursor.execute(
        f"SELECT Region, Subregion FROM StockpilesZones WHERE Shard == '{shard_name}'",
    ).fetchall()
    return [' | '.join(subregion) for subregion in stockpiles_subregions]


@functools.lru_cache
def get_current_shard(path: pathlib.Path, _code: str) -> str:
    """
    :param path: path to read the config from
    :param _code: Arbitrary value to detect new command run (new code means new stock means need to rerun the full func)
    :return: Current shard of the guild from the config file (Able as default value)
    """
    config = configparser.ConfigParser()
    config.read(path)
    return config.get('default', 'shard', fallback=Shard.ABLE.name)


class ModuleStockpiles(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot

    @app_commands.command(name='stockpile-view', description='Get the new stockpile interface')
    async def stockpile_view(self, interaction: discord.Interaction) -> None:
        logging.info(f'[COMMAND] stockpile-view command by {interaction.user.name} on {interaction.guild.name}')
        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')

        if not config.has_section('stockpile'):
            config.add_section('stockpile')
        config.set('stockpile', 'channel', str(interaction.channel_id))

        with open(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini', 'w', newline='') as configfile:
            config.write(configfile)
        await interaction.response.send_message(
            embed=self.refresh_stockpile_interface(self.bot, interaction.guild_id),
        )

    @staticmethod
    def refresh_stockpile_interface(bot: Oisol, guild_id: int) -> discord.Embed:
        """
        This method is also used in the config module
        :param bot: Oisol instance
        :param guild_id: id of the guild the command is executed from
        :return:
        """
        # Get group Stockpiles from db
        guild_stockpiles = bot.cursor.execute(
            f'SELECT Region, Subregion, Code, Name, Type FROM GroupsStockpiles WHERE GroupId == {guild_id}',
        ).fetchall()

        # Group stockpiles by regions
        grouped_stockpiles = {}
        for stockpile in guild_stockpiles:
            if stockpile[0] not in grouped_stockpiles:
                grouped_stockpiles[stockpile[0]] = {}
            if f'{stockpile[1]}_{stockpile[4]}' not in grouped_stockpiles[stockpile[0]]:
                grouped_stockpiles[stockpile[0]][f'{stockpile[1]}_{stockpile[4]}'] = {}
            grouped_stockpiles[stockpile[0]][f'{stockpile[1]}_{stockpile[4]}'][stockpile[3]] = stockpile[2] if len(str_stockpile := str(stockpile[2])) == 6 else f'0{str_stockpile}'

        # Sort all keys in dict and subdicts by key
        sorted_grouped_stockpiles = sort_nested_dicts_by_key(grouped_stockpiles)

        # Get group faction
        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{guild_id}.ini')
        group_faction = config.get('regiment', 'faction', fallback='NEUTRAL')

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

        return discord.Embed().from_dict(
            {
                'title': 'Stockpiles | <:region:1130915923704946758>',
                'color': Faction[group_faction].value,
                'footer': {'text': EmbedIds.STOCKPILES_VIEW.value},
                'fields': embed_fields,
            },
        )

    @app_commands.command(name='stockpile-create', description='Create a new stockpile')
    async def stockpile_create(self, interaction: discord.Interaction, code: str, localisation: str, *, name: str) -> None:
        logging.info(f'[COMMAND] stockpile-create command by {interaction.user.name} on {interaction.guild.name}')
        # Case where a user entered an invalid sized code
        if len(code) != 6:
            await interaction.response.send_message('> The code must be a 6-digits code', ephemeral=True, delete_after=5)
            return
        # Case where a user entered a code without digits only
        if not code.isdigit():
            await interaction.response.send_message('> The code contains non digit characters', ephemeral=True, delete_after=5)
            return
        # Case where a user did not select a provided localisation
        if ' | ' not in localisation or localisation.startswith(' | '):
            await interaction.response.send_message('> The localisation you entered is incorrect, displayed localisations are clickable', ephemeral=True, delete_after=5)
            return

        region, subregion = localisation.split(' | ')  # Only one '|' -> 2 splits
        shard_name = get_current_shard(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini', code)
        stockpile_type = self.bot.cursor.execute(
            'SELECT Type FROM StockpilesZones WHERE Shard == (?) AND Subregion == (?)',
            (shard_name, subregion),
        ).fetchone()[0]

        self.bot.cursor.execute(
            'INSERT INTO GroupsStockpiles (GroupId, Region, Subregion, Code, Name, Type) VALUES (?, ?, ?, ?, ?, ?)',
            (interaction.guild_id, region, subregion, code, name, stockpile_type),
        )
        self.bot.connection.commit()

        await update_discord_interface(
            interaction,
            EmbedIds.STOCKPILES_VIEW.value,
            embed=self.refresh_stockpile_interface(self.bot, interaction.guild_id),
        )

        await interaction.response.send_message('> Stockpile was properly generated', ephemeral=True, delete_after=5)

    @app_commands.command(name='stockpile-delete', description='Delete a specific stockpile using its code')
    async def stockpile_delete(self, interaction: discord.Interaction, stockpile_code: str) -> None:
        logging.info(f'[COMMAND] stockpile-delete command by {interaction.user.name} on {interaction.guild.name}')
        self.bot.cursor.execute(
            f'DELETE FROM GroupsStockpiles WHERE GroupId == {interaction.guild_id} AND Code == {stockpile_code}',
        )
        self.bot.connection.commit()

        await update_discord_interface(
            interaction,
            EmbedIds.STOCKPILES_VIEW.value,
            embed=self.refresh_stockpile_interface(self.bot, interaction.guild_id),
        )
        await interaction.response.send_message(f'> The stockpile (code: {stockpile_code}) was properly removed', ephemeral=True, delete_after=5)

    @app_commands.command(name='stockpile-clear', description='Clear all the stockpiles from the server interface')
    async def stockpile_clear(self, interaction: discord.Interaction) -> None:
        logging.info(f'[COMMAND] stockpile-clear command by {interaction.user.name} on {interaction.guild.name}')
        self.bot.cursor.execute(
            f'DELETE FROM GroupsStockpiles WHERE GroupId == {interaction.guild_id}',
        )
        self.bot.connection.commit()

        await update_discord_interface(
            interaction,
            EmbedIds.STOCKPILES_VIEW.value,
            embed=self.refresh_stockpile_interface(self.bot, interaction.guild_id),
        )
        await interaction.response.send_message('> The stockpile interface was properly cleared', ephemeral=True, delete_after=5)

    @stockpile_create.autocomplete('localisation')
    async def region_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        """
        :param interaction: discord command interaction object
        :param current: current input given by the user
        :return: list of possibles autocompletion results using the current input
        """
        code = next((opt['value'] for opt in interaction.data['options'] if opt.get('name', '') == 'code'), '0')
        current_shard = get_current_shard(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini', code)
        stockpiles = get_shard_stockpiles_subregions(self.bot, current_shard, code)

        if not current:
            return [app_commands.Choice(name=city, value=city) for city in random.choices(stockpiles, k=10)]

        current_stockpiles = [stockpile for stockpile in stockpiles if current.lower() in stockpile.lower()][:25]
        return [app_commands.Choice(name=city, value=city) for city in current_stockpiles]


class StockpileTasks(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot
        self.all_regions_stockpiles = []
        # Start tasks
        self.refresh_able_shard_stockpiles_subregions.start()
        self.refresh_baker_shard_stockpiles_subregions.start()
        self.refresh_charlie_shard_stockpiles_subregions.start()

    @staticmethod
    def _prepare_region_data(api_wrapper: FoxholeAPIWrapper, war_data: dict, region: str) -> list[tuple]:
        single_region_stockpiles = []
        map_items = api_wrapper.get_region_specific_icons(region, [MapIcon.SEAPORT.value, MapIcon.STORAGE_DEPOT.value])
        map_label = api_wrapper.get_region_specific_labels(region)
        ordered_items = api_wrapper.get_subregion_from_map_items(map_items, map_label)
        if region == 'MooringCountyHex':
            region = 'TheMoors'
        elif region == 'DeadLandsHex':
            region = 'Deadlands'
        if ordered_items is not None:
            for item in ordered_items:
                single_region_stockpiles.append((
                    api_wrapper.shard_name,
                    war_data['warNumber'],
                    war_data['conquestStartTime'],
                    re.sub(r'(\w)([A-Z])', r'\1 \2', region.replace('Hex', '')),
                    *item,
                ))
        return single_region_stockpiles

    def _save_region_stockpiles(self, region_stockpiles: list[tuple]) -> None:
        self.all_regions_stockpiles += region_stockpiles

    def _get_latest_stockpiles_zones(self, api_wrapper: FoxholeAPIWrapper, war_data: dict) -> list:
        region_list = api_wrapper.get_regions_list()
        pool = Pool(processes=(cpu_count() - 1))
        for region in region_list:
            pool.apply_async(self._prepare_region_data, args=(api_wrapper, war_data, region), callback=self._save_region_stockpiles)
        pool.close()
        pool.join()
        return self.all_regions_stockpiles

    def _update_stockpile_subregions(self, shard_api: FoxholeAPIWrapper) -> None:
        self.all_regions_stockpiles = []
        if current_war_data := shard_api.get_current_war_state():
            last_war_start_time = self.bot.cursor.execute(
                f"SELECT MAX(ConquestStartTime) FROM StockpilesZones WHERE Shard == '{shard_api.shard_name}'",
            ).fetchone()[0]
            # If war has not started yet
            if not current_war_data['conquestStartTime']:
                return
            if last_war_start_time is None or current_war_data['conquestStartTime'] > last_war_start_time:
                if not (latest_stockpiles := self._get_latest_stockpiles_zones(shard_api, current_war_data)):
                    return
                if last_war_start_time is not None:
                    self.bot.cursor.execute(
                        f"DELETE FROM StockpilesZones WHERE ConquestStartTime == {last_war_start_time} AND Shard == '{shard_api.shard_name}'",
                    )
                self.bot.cursor.executemany(
                    'INSERT INTO StockpilesZones (Shard, WarNumber, ConquestStartTime, Region, Subregion, Type) VALUES (?, ?, ?, ?, ?, ?)',
                    latest_stockpiles,
                )
                self.bot.connection.commit()
                logging.info(f'[TASK] Available stockpiles were updated for {shard_api.shard_name}')

    @tasks.loop(minutes=2)
    async def refresh_able_shard_stockpiles_subregions(self) -> None:
        self._update_stockpile_subregions(FoxholeAPIWrapper())

    @tasks.loop(minutes=2)
    async def refresh_baker_shard_stockpiles_subregions(self) -> None:
        self._update_stockpile_subregions(FoxholeAPIWrapper(shard=Shard.BAKER))

    @tasks.loop(minutes=2)
    async def refresh_charlie_shard_stockpiles_subregions(self) -> None:
        self._update_stockpile_subregions(FoxholeAPIWrapper(shard=Shard.CHARLIE))
