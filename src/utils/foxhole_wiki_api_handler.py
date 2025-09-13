import asyncio
from itertools import compress

import aiohttp
from aiohttp import ClientResponse, ClientSession


class FoxholeWikiAPIWrapper:
    def __init__(self, **kwargs):
        self.__entry_point = 'https://foxhole.wiki.gg/api.php?'
        self.__session = aiohttp.ClientSession(**kwargs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        return await self.close()

    async def close(self) -> None:
        if not self.__session.closed:
            await self.__session.close()

    def get_active_session(self) -> ClientSession:
        return self.__session

    @staticmethod
    async def __response_handler(response: ClientResponse) -> dict | list | None:
        match response.status:
            # Expected output, can be list or dict
            case 200:
                return await response.json()
            case _:
                return None

    async def wiki_search_request(self, search_request: str, do_resolve_redirect: bool = True) -> dict | None:
        """
        Method to make a search request using the wiki's browser via API.
        Example:
        search_request -> sphata, (the typo is voluntary to prove the case)
        would result in -> {"85K-a “Spatha”": "https://foxhole.wiki.gg/wiki/85K-a_%E2%80%9CSpatha%E2%80%9D"}
        :param search_request: user input to use for the search
        :param do_resolve_redirect: whether to return the redirect itself (False) or its target (True)
        :return: None in case of unexpected error, else dict of resulting search request with top key being the best result
        """
        redirect_status = 'resolve' if do_resolve_redirect else 'return'

        async with self.__session.get(
                f'{self.__entry_point}action=opensearch&search={search_request}&redirects={redirect_status}',
                timeout=5,
        ) as async_response:
            response = await self.__response_handler(async_response)

            # An unexpected error occurred
            if response is None:
                return None

            # The output is as expected, return a dict where k is the entry's full name, and v its wiki page url
            return dict(zip(response[1], response[-1], strict=True))

    async def fetch_cargo_tables(self) -> list | None:
        """
        Fetch all available cargo tables
        :return: A list of available cargo tables, None in case of an unexpected error
        """
        async with self.__session.get(
            f'{self.__entry_point}action=cargotables&format=json',
            timeout=5,
        ) as async_response:
            response = await self.__response_handler(async_response)

        if response is None:
            return None

        return response['cargotables']

    async def fetch_cargo_table_fields(self, table_name: str) -> list | None:
        """
        Fetch all available fields from a table
        :param table_name: name of the table to fetch the fields from
        :return: list of fetched fields from table
        """
        async with self.__session.get(
            f'{self.__entry_point}action=cargofields&format=json&table={table_name}',
            timeout=5,
        ) as async_response:
            response = await self.__response_handler(async_response)

        if response is None:
            return None
        return list(response['cargofields'])

    async def is_name_in_table(self, session: ClientSession, table: str, name: str) -> bool:
        """
        Check if a name is in a table, using the "name" field.
        This is used as a sub method to a larger asyncio process, thus the session parameter.
        :param session: session to use that is not the wrapper session
        :param table: table to check the name for
        :param name: name to check inside the "name" column of the table
        :return: a boolean indicating if the name was found in the table
        """
        async with session.get(
            f'{self.__entry_point}action=cargoquery&format=json&tables={table}&fields=name&where=_PageName="{name}" or name="{name}"',
            timeout=5,
        ) as async_response:
            response = await self.__response_handler(async_response)

            # In case of error during the request, None will be returned but will fall back to False anyway
            return bool(response.get('cargoquery', False))

    async def is_page_wiki_page(self, session: ClientSession, pages_names: list) -> list[bool]:
        """
        Use the API to parse a page and retrieve its category to determine its status
        :param session: session to use
        :param pages_names: pages to parse
        :return: If page is a list of ambiguate pages (False) or a direct wiki page (True)
        """
        masked_pages_names = pages_names.copy()

        async with session.get(f'https://foxhole.wiki.gg/api.php?action=query&titles={'|'.join(pages_names)}&format=json&prop=pageprops&redirects=True') as async_response:
            response = await self.__response_handler(async_response)

        # Create dict of potential redirections, to get the reverse available
        redirections = {redirection['to']: redirection['from'] for redirection in response['query']['redirects']} if 'redirects' in response['query'] else {}

        for page in response['query']['pages'].values():
            # Check for reverse redirection
            title = redirections.get(page['title'], page['title'])

            # Create mask by checking if a page has a version related description
            masked_pages_names[masked_pages_names.index(title)] = bool('pageprops' in page and page['pageprops']['description'].startswith('This article is considered accurate for the current version'))
        return masked_pages_names

    async def find_table_from_value_name(self, value_name: str, context_tables: list) -> str | None:
        """
        Find a full name in the context tables, it is assumed all context tables have a "name" field
        :param value_name: name to find in tables
        :param context_tables: tables to search in
        :return: table where value_name was found, None otherwise
        """

        async with aiohttp.ClientSession() as session: # Create a new session for the gather to prevent closing the main one
            mask = await asyncio.gather(*(self.is_name_in_table(session, table, value_name) for table in context_tables))

        return next(compress(context_tables, mask), None)

    async def retrieve_image_url_from_name(self, session: ClientSession, image_file_name: str) -> str | None:
        """
        Retrieve an image url via the API using its file name
        :param session: session to use that is not the wrapper session
        :param image_file_name: image file name
        :return: url to the image
        """
        async with session.get(
            f'https://foxhole.wiki.gg/api.php?action=query&titles=File:{image_file_name}&prop=imageinfo&iiprop=url&format=json',
            timeout=5,
        ) as async_response:
            response = await self.__response_handler(async_response)

        if response is None:
            return None

        return (page_dict := response['query']['pages'])[next(iter(page_dict))]['imageinfo'][0]['url']

    async def retrieve_armor_attributes(self, session: ClientSession, armor_name: str) -> dict | None:
        """
        Retrieve resistances attributes for a specific game armor
        :param session: session to use that is not the wrapper session
        :param armor_name: armor to retrieve the attributes from
        :return: dict where k is the resistance name and v its resistance value
        """
        async with session.get(
            f'https://foxhole.wiki.gg/api.php?action=cargoquery&format=json&tables=damagetypes&fields=name,{armor_name}',
            timeout=5,
        ) as async_response:
            response = await self.__response_handler(async_response)

        if response is None:
            return None

        return {armor_attr['title']['name']: armor_attr['title'][armor_name] for armor_attr in response['cargoquery']}

    async def retrieve_damage_emitters(self, session: ClientSession) -> list | None:
        async with session.get(
            'https://foxhole.wiki.gg/api.php?action=cargoquery&format=json&tables=itemdata&fields=name,damage,damage_type,damage_rng,damage_no_bug&where=damage!=%22null%22',
            timeout=5,
        ) as async_response:
            response = await self.__response_handler(async_response)

        if response is None:
            return None

        return [entry['title'] for entry in response['cargoquery']]

    async def retrieve_row_data_from_table(self, target_fields: list[str], table_name: str, target_name: str) -> dict | None:
        """
        Method to retrieve data during health process
        :param target_fields: columns to retrieve from the table
        :param table_name: either "structures" or "vehicles"
        :param target_name: used to target column "name" where row value is target_name
        :return: target & damage data
        """
        async with aiohttp.ClientSession() as session:
            async_vehicle_data = await session.get(
                f'{self.__entry_point}action=cargoquery&format=json&tables={table_name}&fields={','.join(target_fields)}&where=_PageName="{target_name}" or name="{target_name}"')
            row_data = (await self.__response_handler(async_vehicle_data))['cargoquery'][0]['title']

            # tasks that can be run independently at once, format -> [(foo, args)],
            # result of gather is a list of each method result, following the call order
            tasks_stack = []
            if 'image' in row_data:
                tasks_stack.append((self.retrieve_image_url_from_name, session, row_data['image']))
            if 'armour type' in row_data:
                tasks_stack.append((self.retrieve_armor_attributes, session, row_data['armour type']))
            tasks_stack.append((self.retrieve_damage_emitters, session))

            res = await asyncio.gather(*(foo(*args) for foo, *args in tasks_stack))

        row_data['image_url'] = res[0]
        row_data['damages'] = res[-1]

        if len(res) == 3:
            row_data['armor_attributes'] = res[1]

        return row_data
