from __future__ import annotations

import asyncio
import itertools
import re
import sqlite3
from typing import TYPE_CHECKING

import aiohttp
from discord.ext import commands, tasks

from src.utils import OISOL_HOME_PATH, FoxholeAsyncAPIWrapper, MapIcon, Shard

if TYPE_CHECKING:
    from main import Oisol


class TaskUpdateAvailableStockpiles(commands.Cog):
    """
    This class handles the database of available stockpiles for each shard. It does not depend on any of the guild the
    bot is a member of. When a new war start on a shard, the bot update the db's rows with the associated shard.
    """
    def __init__(self, bot: Oisol):
        self.bot = bot
        self.all_regions_stockpiles = []

        # Start tasks
        if Shard.ABLE.name in self.bot.connected_shards:
            self.refresh_able_shard_stockpiles_subregions.start()
        if Shard.BAKER.name in self.bot.connected_shards:
            self.refresh_baker_shard_stockpiles_subregions.start()
        if Shard.CHARLIE.name in self.bot.connected_shards:
            self.refresh_charlie_shard_stockpiles_subregions.start()

    @staticmethod
    async def _prepare_region_data(session: aiohttp.ClientSession, api_wrapper: FoxholeAsyncAPIWrapper, war_data: dict, region: str) -> list[tuple]:
        single_region_stockpiles = []

        map_tasks_array = {
            api_wrapper.get_region_specific_icons: [session, region, [MapIcon.SEAPORT.value, MapIcon.STORAGE_DEPOT.value]],
            api_wrapper.get_region_specific_labels: [session, region],
        }
        map_items, map_labels = await asyncio.gather(*[foo(*args) for foo, args in map_tasks_array.items()])
        ordered_items = api_wrapper.get_subregion_from_map_items(map_items, map_labels)

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

    async def _get_latest_stockpiles_zones(self, session: aiohttp.ClientSession, api_wrapper: FoxholeAsyncAPIWrapper, war_data: dict) -> list:
        # Retrieve shard's list of active regions
        region_list = await api_wrapper.get_regions_list(session)

        # Retrieve region stockpiles with format: tuple[shard, war_number, war_start_time, region, subregion, type[Seaport, Storage Depot]]
        result = await asyncio.gather(*[self._prepare_region_data(session, api_wrapper, war_data, region) for region in region_list])

        # Return flattened version from list of lists len 1 of tuple to list of tuples
        return list(itertools.chain(*result))

    async def _update_stockpile_subregions(self, shard_api: FoxholeAsyncAPIWrapper) -> None:
        self.all_regions_stockpiles = []
        session = aiohttp.ClientSession()

        if not (current_war_data := await shard_api.get_current_war_state(session)):
            return
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
                if not (latest_stockpiles := await self._get_latest_stockpiles_zones(session, shard_api, current_war_data)):
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
        await session.close()

    @tasks.loop(minutes=2)
    async def refresh_able_shard_stockpiles_subregions(self) -> None:
        await self._update_stockpile_subregions(FoxholeAsyncAPIWrapper())

    @tasks.loop(minutes=2)
    async def refresh_baker_shard_stockpiles_subregions(self) -> None:
        await self._update_stockpile_subregions(FoxholeAsyncAPIWrapper(shard=Shard.BAKER))

    @tasks.loop(minutes=2)
    async def refresh_charlie_shard_stockpiles_subregions(self) -> None:
        await self._update_stockpile_subregions(FoxholeAsyncAPIWrapper(shard=Shard.CHARLIE))
