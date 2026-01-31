import sqlite3

import pytest

from src.modules.wiki.health_embed_templates import HealthEntryEngine
from src.modules.wiki.wiki_embeds_templates import WikiTemplateFactory
from src.modules.wiki.production_embed_templates import ProductionTemplate
from src.modules.wiki.module_wiki import HEALTH_DATA, ModuleWiki, PRODUCTION_DATA, WIKI_DATA
from src.utils import WikiTables, OISOL_HOME_PATH

HEALTH_TEST_DATA = [f'{entry['name']}@{entry['table']}' for entry in HEALTH_DATA if entry['table'] != 'custom_map']
PRODUCTION_TEST_DATA = [f'{entry['name']}@{entry['table']}' for entry in PRODUCTION_DATA if entry['table'] != 'structures']
WIKI_TEST_DATA = [f'{entry['name']}@{entry['table']}' for entry in WIKI_DATA if entry['table'] != 'maps']


@pytest.mark.parametrize('search_request', HEALTH_TEST_DATA)
def test_health_command(search_request: str):
    search_request, table_name = search_request.split('@')
    entry_data = ModuleWiki.retrieve_row_from_name(table_name, search_request)

    # Compute health of search_request & generate embed
    entry_embed = HealthEntryEngine(entry_data, {}).get_generated_embed()

    assert len(entry_embed), f'Embed is empty for {search_request}'


@pytest.mark.parametrize('search_request', WIKI_TEST_DATA)
def test_wiki_command(search_request: str):
    search_request, table_name = search_request.split('@')
    entry_data = ModuleWiki.retrieve_row_from_name(table_name, search_request)

    # Compute wiki of search_request & generate embed
    entry_embed = WikiTemplateFactory(entry_data, {}).get(WikiTables(table_name)).generate_embed_data()

    assert len(entry_embed), f'Embed is empty for {search_request}'


@pytest.mark.parametrize('search_request', WIKI_TEST_DATA)
def test_production_command(search_request: str):
    search_request, table_name = search_request.split('@')
    entry_data = ModuleWiki.retrieve_row_from_name(table_name, search_request)

    with sqlite3.connect(OISOL_HOME_PATH / 'foxhole_wiki_mirror.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        production_rows = cursor.execute(
            'SELECT * FROM productionmerged3 WHERE Output == ?',
            (search_request,),
        ).fetchall()

        production_data = ProductionTemplate([dict(row) for row in production_rows], search_request, {})
        entry_embeds = production_data.get_generated_embeds()

    assert len(entry_embeds), f'Embed is empty for {search_request}'
