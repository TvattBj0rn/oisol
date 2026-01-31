import pytest

from src.modules.wiki.health_embed_templates import HealthEntryEngine
from src.modules.wiki.module_wiki import HEALTH_DATA, ModuleWiki


HEALTH_TEST_DATA = [f'{entry['name']}@{entry['table']}' for entry in HEALTH_DATA if entry['table'] != 'custom_map']


@pytest.mark.parametrize('search_request', HEALTH_TEST_DATA)
def test_health_command(search_request: str):
    search_request, health_table = search_request.split('@')
    entry_data = ModuleWiki.retrieve_row_from_name(health_table, search_request)

    # Compute health of search_request & generate embed
    health_embed = HealthEntryEngine(entry_data, {}).get_generated_embed()

    assert len(health_embed), f'Health embed is empty for {search_request}'
