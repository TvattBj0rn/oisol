from src.modules.wiki.scrapers.scrap_wiki_entry_health import scrap_health
from src.modules.wiki.scrapers.scrap_wiki_entry_infobox import scrap_wiki
from src.utils.resources import (
    ALL_WIKI_ENTRIES,
    STRUCTURES_WIKI_ENTRIES,
    VEHICLES_WIKI_ENTRIES,
)

import pytest

@pytest.mark.parametrize('entry', STRUCTURES_WIKI_ENTRIES)
def test_health_command_structures_entries(entry):
    if (
            entry['name'].startswith(('Bunker Base', 'Safe House', 'Town Base', 'Medical Room'))
            and entry['name'].endswith('(Tier 1)')
    ):
        entry['name'] = entry['name'].removesuffix(' (Tier 1)')
    entry_output = scrap_health('https://foxhole.wiki.gg/wiki/Structure_Health', entry['name'])
    assert 'Name' in entry_output, f'Invalid structure entry: {entry['name']}'


@pytest.mark.parametrize('entry', VEHICLES_WIKI_ENTRIES)
def test_health_command_vehicles_entries(entry):
    entry_output = scrap_health('https://foxhole.wiki.gg/wiki/Vehicle_Health', entry['name'])
    assert 'Name' in entry_output, f'Invalid vehicle entry: {entry['name']}'


@pytest.mark.parametrize('entry', ALL_WIKI_ENTRIES)
def test_wiki_command_all_entries(entry):
    entry_output = scrap_wiki(entry['url'], entry['name'])
    assert 'title' in entry_output, f'Invalid wiki entry: {entry['name']}'
