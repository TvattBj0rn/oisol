from __future__ import annotations

import aiohttp
import asyncio

from typing import TYPE_CHECKING

from discord.ext import commands, tasks

from src.utils import Shard, CacheKeys, MapIcon
from src.utils.foxhole_api_handler import FoxholeAsyncAPIWrapper

if TYPE_CHECKING:
    from main import Oisol


class WorldSpawnsStatus(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot

        self.tasks_status_tracker = []

        # Create cog related cache
        if CacheKeys.WORLD_SPAWNS_STATUS not in self.bot.cache:
            self.bot.cache[CacheKeys.WORLD_SPAWNS_STATUS] = {}

        # Ensure cache is created for all shards
        for shard_name in [
            Shard.ABLE.name,
            Shard.BAKER.name,
            Shard.CHARLIE.name
        ]:
            if shard_name not in self.bot.cache[CacheKeys.WORLD_SPAWNS_STATUS]:
                self.bot.cache[CacheKeys.WORLD_SPAWNS_STATUS][shard_name] = {}

        # Start tasks
        self.update_able_world_spawn_cache.start()
        self.update_baker_world_spawn_cache.start()
        self.update_charlie_world_spawn_cache.start()
        self.cog_activation_report.start()

    @staticmethod
    async def _get_region_world_spawn_status(session: aiohttp.ClientSession, shard_api: FoxholeAsyncAPIWrapper, region: str) -> list:
        region_world_spawn_map_items = await shard_api.get_region_specific_icons(
            session,
            region,
            [
                MapIcon.TOWN_BASE_1.value, # Tier 1 Town base
                MapIcon.TOWN_BASE_2.value, # Tier 2 Town base
                MapIcon.TOWN_BASE_3.value, # Tier 3 Town base
                MapIcon.RELIC_BASE_1.value, # Relic base
            ],
        )
        region_labels = await shard_api.get_region_specific_labels(
            session,
            region,
            is_major=True,
        )

        return shard_api.get_subregion_from_map_items(region_world_spawn_map_items, region_labels)

    def _update_world_spawn_cache(self, new_data: list, shard_name: str) -> None:
        """
        Add retrieved data to the cache
        :param new_data: global list of regions lists of subregions tuples
        :param shard_name: name of the shard to update the cache to
        """
        self.bot.cache[shard_name] = dict(subregion for region in new_data for subregion in region)

    async def _update_shard_world_spawn_cache(self, shard_api: FoxholeAsyncAPIWrapper):
        async with aiohttp.ClientSession() as session:
            available_regions_list = await shard_api.get_regions_list(session)
            res = await asyncio.gather(*(self._get_region_world_spawn_status(session, shard_api, region) for region in available_regions_list))

        # Update bot shard cache
        self._update_world_spawn_cache(res, shard_api.shard_name)

        # Update status tracker, to prevent having a log displayed every 2 minutes on the console
        self.tasks_status_tracker.append(shard_api.shard_name)


    @tasks.loop(minutes=2)
    async def update_able_world_spawn_cache(self):
        await self._update_shard_world_spawn_cache(FoxholeAsyncAPIWrapper())

    @tasks.loop(minutes=2)
    async def update_baker_world_spawn_cache(self):
        await self._update_shard_world_spawn_cache(FoxholeAsyncAPIWrapper(shard=Shard.BAKER))

    @tasks.loop(minutes=2)
    async def update_charlie_world_spawn_cache(self):
        await self._update_shard_world_spawn_cache(FoxholeAsyncAPIWrapper(shard=Shard.CHARLIE))

    @tasks.loop(hours=24)
    async def cog_activation_report(self):
        self.bot.logger.task(f'The world_spawn_status cache was updated {len(self.tasks_status_tracker)} times: {self.tasks_status_tracker} in the last 24 hours')
        self.tasks_status_tracker.clear()
