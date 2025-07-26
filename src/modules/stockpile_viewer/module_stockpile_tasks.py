from __future__ import annotations

import re
import sqlite3
from multiprocessing import Pool, cpu_count
from typing import TYPE_CHECKING

from discord.ext import commands, tasks

from src.utils import OISOL_HOME_PATH, FoxholeAPIWrapper, MapIcon, Shard

if TYPE_CHECKING:
    from main import Oisol


class StockpileTasks(commands.Cog):
    """
    This class handles the database of available stockpiles for each shard. It does not depend on any of the guild the
    bot is a member of. When a new war start on a shard, the bot update the db's rows with the associated shard.
    """
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
            single_region_stockpiles.extend((
                    api_wrapper.shard_name,
                    war_data['warNumber'],
                    war_data['conquestStartTime'],
                    re.sub(r'(\w)([A-Z])', r'\1 \2', region.replace('Hex', '')),
                    *item,
                ) for item in ordered_items
            )
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
            with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
                cursor = conn.cursor()
                last_war_start_time = cursor.execute(
                    'SELECT MAX(ConquestStartTime) FROM StockpilesZones WHERE Shard == ?',
                    (shard_api.shard_name,),
                ).fetchone()[0]
                # If war has not started yet
                if not current_war_data['conquestStartTime']:
                    return
                # New war has started
                if last_war_start_time is None or current_war_data['conquestStartTime'] > last_war_start_time:
                    if not (latest_stockpiles := self._get_latest_stockpiles_zones(shard_api, current_war_data)):
                        return
                    if last_war_start_time is not None:
                        cursor.execute(
                            'DELETE FROM StockpilesZones WHERE ConquestStartTime == ? AND Shard == ?',
                            (last_war_start_time, shard_api.shard_name),
                        )
                    cursor.executemany(
                        'INSERT INTO StockpilesZones (Shard, WarNumber, ConquestStartTime, Region, Subregion, Type) VALUES (?, ?, ?, ?, ?, ?)',
                        latest_stockpiles,
                    )
                    conn.commit()
                    self.bot.logger.task(f'Available stockpiles were updated for {shard_api.shard_name}')

    @tasks.loop(minutes=2)
    async def refresh_able_shard_stockpiles_subregions(self) -> None:
        self._update_stockpile_subregions(FoxholeAPIWrapper())

    @tasks.loop(minutes=2)
    async def refresh_baker_shard_stockpiles_subregions(self) -> None:
        self._update_stockpile_subregions(FoxholeAPIWrapper(shard=Shard.BAKER))

    @tasks.loop(minutes=2)
    async def refresh_charlie_shard_stockpiles_subregions(self) -> None:
        self._update_stockpile_subregions(FoxholeAPIWrapper(shard=Shard.CHARLIE))
