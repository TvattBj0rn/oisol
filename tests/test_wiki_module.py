from src.modules.wiki.scrapers.scrap_wiki_entry_health import scrap_health
from src.utils import (
    STRUCTURES_WIKI_ENTRIES,
    VEHICLES_WIKI_ENTRIES,
)

import pytest


def health_command_entries_pairs():
    return [
        *(('https://foxhole.wiki.gg/wiki/Structure_Health', entry) for entry in STRUCTURES_WIKI_ENTRIES),
        *(('https://foxhole.wiki.gg/wiki/Vehicle_Health', entry) for entry in VEHICLES_WIKI_ENTRIES),
    ]


@pytest.mark.parametrize('url, entry', health_command_entries_pairs())
def test_health_command_entries(url: str, entry: dict):
    entry_output = scrap_health(url, entry['name'])
    assert 'Name' in entry_output, f'Invalid entry: {entry['name'], url}'
