from aiohttp import ClientResponse, ClientSession

from src.utils import MapIcon, Shard


class FoxholeAsyncAPIWrapper:
    def __init__(self, shard: Shard = Shard.ABLE):
        self.shard_name = shard.name
        self.shard_endpoint = shard.value

    @staticmethod
    async def _response_handler(response: ClientResponse, etag: str | None) -> tuple[str, dict]:
        match response.status:
            case 200:
                return response.headers['Etag'], await response.json()
            # This data was already returned to the user
            case 304:
                return etag, {}
            # Default / Else
            case _:
                return '', {}

    async def get_current_war_state(self, session: ClientSession) -> dict:
        """
        Returns data about the current state of the war. This data may update every 60 seconds.
        :return: json of the requested data if the response code was 200 else an empty dictionary.
        """

        async with session.get(
                f'{self.shard_endpoint}/worldconquest/war',
                timeout=5,
        ) as response:
            return await response.json()

    async def get_regions_list(self, session: ClientSession) -> list[str]:
        """
        Returns a list of the active World Conquest map names.
        :return: list of world regions if the response code was 200, else an empty list.
        """
        async with session.get(
                f'{self.shard_endpoint}/worldconquest/maps',
                timeout=5,
        ) as response:
            return await response.json()

    async def get_region_war_report(self, session: ClientSession, region: str, etag: str | None = None) -> tuple[str, dict]:
        """
        Returns the number of enlistments, casualties, and other map specific information as well as the etag.
        :param session:
        :param region: the region to pull the data from.
        :param etag: optional tag allowing to check if the data was changed since last interaction.
        :return: etag and region report if the response code was 200, etag and an empty dict if the response code was 304 else an empty string and an empty dict.
        """
        async with session.get(
                f'{self.shard_endpoint}/worldconquest/warReport/{region}',
                timeout=5,
                headers={'If-None-Match': etag} if etag is not None else None,
        ) as response:
            return await self._response_handler(response, etag)

    async def get_region_static_data(self, session: ClientSession, region: str, etag: str | None = None) -> tuple[str, dict]:
        """
        Returns region static information (landmarks, labels, ...) as well as the etag.
        :param session:
        :param region: the region to pull the data from.
        :param etag: optional tag allowing to check if the data was changed since last interaction.
        :return: etag and region report if the response code was 200, etag and an empty dict if the response code was 304 else an empty string and an empty dict.
        """
        async with session.get(
                f'{self.shard_endpoint}/worldconquest/maps/{region}/static',
                timeout=5,
                headers={'If-None-Match': etag} if etag is not None else None,
        ) as response:
            return await self._response_handler(response, etag)

    async def get_region_dynamic_data(self, session: ClientSession, region: str, etag: str | None = None) -> tuple[str, dict]:
        """
        Returns region dynamic information (subregion owner, advanced structures, ...) as well as the etag.
        :param session:
        :param region: the region to pull the data from.
        :param etag: optional tag allowing to check if the data was changed since last interaction.
        :return: etag and region report if the response code was 200, etag and an empty dict if the response code was 304 else an empty string and an empty dict.
        """
        async with session.get(
                f'{self.shard_endpoint}/worldconquest/maps/{region}/dynamic/public',
                timeout=5,
                headers={'If-None-Match': etag} if etag is not None else None,
        ) as response:
            return await self._response_handler(response, etag)

    async def get_region_specific_icons(self, session: ClientSession, region: str, icons_id: list[int]) -> list[dict]:
        """
        Get a list of map items corresponding to icons_id. Etag not required since this function will only be called when data has changed.
        :param session:
        :param region: the region to pull the data from.
        :param icons_id: list of icon to return
        :return: list of map items corresponding to icons_id
        """
        _, dynamic_data = await self.get_region_dynamic_data(session, region)
        if not dynamic_data:
            return []

        return [map_item for map_item in dynamic_data['mapItems'] if map_item['iconType'] in icons_id]

    async def get_region_specific_labels(self, session: ClientSession, region: str, is_major: bool = True) -> list[dict]:
        """
        Get a list of map label corresponding to icons_id. Etag not required since this function will only be called when data has changed.
        :param session:
        :param region: the region to pull the data from.
        :param is_major: expected label type
        :return: list of map items corresponding to icons_id
        """
        _, static_data = await self.get_region_static_data(session, region)
        if not static_data:
            return []

        return [map_item for map_item in static_data['mapTextItems'] if map_item['mapMarkerType'] == ('Major' if is_major else 'Minor')]

    @staticmethod
    def get_subregion_from_map_items(map_items: list[dict], map_labels: list[dict]) -> list[tuple]:
        """
        Get a list of subregion from a list of map items.
        :param map_items: list of map items with coordinates
        :param map_labels: list of map labels with coordinates
        :return: list of subregion from a list of map items
        """
        if not map_items or not map_labels:
            return []

        res = []

        for map_item in map_items:
            closest_label = ''
            closest_x = 1
            closest_y = 1
            for map_label in map_labels:
                if (comparison_x := abs(map_item['x'] - map_label['x'])) + (comparison_y := abs(map_item['y'] - map_label['y'])) < closest_x + closest_y:
                    closest_label = map_label['text']
                    closest_x = comparison_x
                    closest_y = comparison_y
            res.append((closest_label, MapIcon(map_item['iconType']).name))
        return res
