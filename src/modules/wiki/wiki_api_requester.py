import asyncio
from collections.abc import Callable

import requests
from aiohttp import ClientSession


async def fetch_response(url: str, attribute_name: str, retrieval_pattern: Callable, queue: asyncio.Queue) -> None:
    async with ClientSession() as session, session.get(url) as response:
        await queue.put({attribute_name: retrieval_pattern(await response.json())})


async def get_entry_attributes(entry_name: str, entry_table: str) -> dict:
    session = requests.Session()

    # Retrieve all fields of entry_table
    all_table_fields_response = session.get(
        timeout=5,
        url=f'https://foxhole.wiki.gg/api.php?action=cargofields&format=json&table={entry_table}',
    )
    if not all_table_fields_response.ok:
        return {}
    all_table_fields = list(all_table_fields_response.json().get('cargofields'))

    # Retrieve associated entry_name data using fields of previous request
    response = session.get(
        timeout=5,
        url=f'https://foxhole.wiki.gg/api.php?action=cargoquery&format=json&tables={entry_table}&fields={','.join(all_table_fields)}&where=name="{entry_name}"',
    )
    if not response.ok:
        return {}
    data_dict = response.json().get('cargoquery')[0].get('title')

    queue = asyncio.Queue()

    async with asyncio.TaskGroup() as group:
        # Request the image via its url (should exist for all requested tables)
        group.create_task(fetch_response(f'https://foxhole.wiki.gg/api.php?action=query&titles=File:{data_dict.get('image')}&prop=imageinfo&iiprop=url&format=json', 'image_url', lambda x: (page_dict := x['query']['pages'])[next(iter(page_dict))]['imageinfo'][0]['url'], queue))
        # Request the armor type and specification via its armor name
        if data_dict.get('armour type') is not None:
            group.create_task(fetch_response(f'https://foxhole.wiki.gg/api.php?action=cargoquery&format=json&tables=damagetypes&fields=name,{data_dict.get('armour type')}', 'armour_attributes', lambda x: {row['title']['name']: row['title'][data_dict['armour type']] for row in x['cargoquery']}, queue))
        if data_dict.get('map icon') is not None:
            group.create_task(fetch_response(f'https://foxhole.wiki.gg/api.php?action=query&titles=File:{data_dict.get('map icon')}&prop=imageinfo&iiprop=url&format=json', 'map_icon_url', lambda x: (page_dict := x['query']['pages'])[next(iter(page_dict))]['imageinfo'][0]['url'], queue))
        if data_dict.get('ammo') is not None:
            group.create_task(fetch_response(f'https://foxhole.wiki.gg/api.php?action=cargoquery&format=json&tables=itemdata&fields=damage,damage_rng,damage_type&where=name="{data_dict.get('ammo')}"', 'ammo_info', lambda x: x['cargoquery'][0]['title'], queue))

    while not queue.empty():
        data_dict |= await queue.get()
    return data_dict
