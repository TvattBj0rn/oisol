from src.modules.wiki.scrapers.scrap_wiki_entry_health import scrap_health
from src.modules.wiki.scrapers.scrap_wiki_entry_infobox import scrap_wiki
from src.modules.wiki.scrapers.scrap_wiki_entry_production import scrap_production
from src.utils import (
    ALL_WIKI_ENTRIES,
    PRODUCTION_ENTRIES,
    STRUCTURES_WIKI_ENTRIES,
    VEHICLES_WIKI_ENTRIES,
)

import pytest

@pytest.mark.parametrize('entry', STRUCTURES_WIKI_ENTRIES)
def test_health_command_structures_entries(entry):
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


@pytest.mark.parametrize('entry', PRODUCTION_ENTRIES)
def test_production_command_entries(entry):
    entry_output = scrap_production(entry['url'])
    assert all(k in entry_output for k in ['Structure', 'Input(s)', 'Output']), f'Invalid production entry: {entry['name']}'
