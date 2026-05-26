import asyncio

import aiohttp

from src.utils import FoxholeAsyncAPIWrapper

async def main():
    api = FoxholeAsyncAPIWrapper()
    async with aiohttp.ClientSession() as session:
        list_res = await api.get_regions_list(session)
        data_res = await api.get_region_specific_icons(session, 'TyrantFoothillsHex', [45, 56, 57, 58])
    print(data_res)

if __name__ == '__main__':
    asyncio.run(main())
