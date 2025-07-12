from src.modules.wiki.wiki_api_requester import get_entry_attributes
from src.utils import ALL_WIKI_ENTRIES

import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize('entry', ALL_WIKI_ENTRIES)
async def test_wiki_command_all_entries(entry: dict):
    entry_output = await get_entry_attributes(entry_name=entry['name'], entry_table=entry['wiki_table'].value)
    # 50 is an arbitrary value, the table used has over 150 columns
    assert len(entry_output) > 50, f'Invalid wiki entry: {entry['name']}'

