from src.modules.wiki.scrapers.scrap_health import scrap_health
from src.modules.wiki.scrapers.scrap_wiki import scrap_wiki
from src.utils.resources import (
    ALL_WIKI_ENTRIES,
    STRUCTURES_WIKI_ENTRIES,
    VEHICLES_WIKI_ENTRIES,
)


def test_health_command_structures_entries():
    for entry in STRUCTURES_WIKI_ENTRIES:
        if (
                entry['name'].startswith(('Bunker Base', 'Safe House', 'Town Base'))
                and entry['name'].endswith('(Tier 1)')
        ):
            entry['name'] = entry['name'].removesuffix(' (Tier 1)')
        entry_output = scrap_health('https://foxhole.wiki.gg/wiki/Structure_Health', entry['name'])
        assert 'Name' in entry_output, f'Invalid structure entry: {entry}'


def test_health_command_vehicles_entries():
    for entry in VEHICLES_WIKI_ENTRIES:
        entry_output = scrap_health('https://foxhole.wiki.gg/wiki/Vehicle_Health', entry['name'])
        assert 'Name' in entry_output, f'Invalid vehicle entry: {entry}'


def test_wiki_command_all_entries():
    for entry in ALL_WIKI_ENTRIES:
        entry_output = scrap_wiki(entry['url'], entry['name'])
        assert 'title' in entry_output, f'Invalid wiki entry: {entry}'
