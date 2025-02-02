import requests

from src.utils import Shard


class FoxholeAPIWrapper:
    def __init__(self, shard: Shard = Shard.ABLE):
        self.shard = shard.value

    @staticmethod
    def _response_handler(response: requests.Response, etag: str | None) -> tuple[str, dict]:
        match response.status_code:
            case 200:
                return response.headers['Etag'], response.json()
            case 304:
                return etag, {}
            # Default / Else
            case _:
                return '', {}

    def get_current_war_state(self) -> dict:
        """
        Returns data about the current state of the war. This data may update every 60 seconds.
        :return: json of the requested data if the response code was 200 else an empty dictionary.
        """
        if (response := requests.get(f'{self.shard}/worldconquest/war')).status_code == 200:
            return response.json()
        return {}

    def get_regions_list(self) -> list:
        """
        Returns a list of the active World Conquest map names.
        :return: list of world regions if the response code was 200, else an empty list.
        """
        if (response := requests.get(f'{self.shard}/worldconquest/maps')).status_code == 200:
            return response.json()
        return []

    def get_region_war_report(self, region: str, etag: str | None = None) -> tuple[str, dict]:
        """
        Returns the number of enlistments, casualties, and other map specific information as well as the etag.
        :param region: the region to pull the data from.
        :param etag: optional tag allowing to check if the data was changed since last interaction.
        :return: etag and region report if the response code was 200, etag and an empty dict if the response code was 304 else an empty string and an empty dict.
        """
        return self._response_handler(
            requests.get(
                f'{self.shard}/worldconquest/warReport/{region}',
                headers={'If-None-Match': etag}),
            etag,
        )

    def get_region_static_data(self, region: str, etag: str | None = None) -> tuple[str, dict]:
        """
        Returns region static information (landmarks, labels, ...) as well as the etag.
        :param region: the region to pull the data from.
        :param etag: optional tag allowing to check if the data was changed since last interaction.
        :return: etag and region report if the response code was 200, etag and an empty dict if the response code was 304 else an empty string and an empty dict.
        """
        return self._response_handler(
            requests.get(
                f'{self.shard}/worldconquest/maps/{region}/static',
                headers={'If-None-Match': etag}),
            etag,
        )

    def get_region_dynamic_data(self, region: str, etag: str | None = None) -> tuple[str, dict]:
        """
        Returns region dynamic information (subregion owner, advanced structures, ...) as well as the etag.
        :param region: the region to pull the data from.
        :param etag: optional tag allowing to check if the data was changed since last interaction.
        :return: etag and region report if the response code was 200, etag and an empty dict if the response code was 304 else an empty string and an empty dict.
        """
        return self._response_handler(
            requests.get(
                f'{self.shard}/worldconquest/maps/{region}/dynamic/public',
                headers={'If-None-Match': etag}),
            etag,
        )
