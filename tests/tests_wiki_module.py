import pytest
import requests

from src.modules.wiki.health_embed_templates import HealthEntryEngine
from src.modules.wiki.module_wiki import HEALTH_DATA


VEHICLES_TABLE_ALL_FIELDS = ['version', 'codename', 'aliases', 'name', 'image', 'imageOverride', 'staticImage', 'type', 'vehicle_type', 'vehicle_hp', 'disable', 'repair', 'armour_type', 'armour_hp', 'min_pen_chance', 'max_pen_chance', 'disable_chance_tracks', 'disable_chance_fueltank', 'disable_chance_turret', 'disable_chance_turret2', 'crew', 'passengers', 'slots', 'build_location', 'tier_cost', 'variants', 'chassis', 'faction', 'fuelcap', 'fueltype', 'fuelrate', 'fuelrate_water', 'fuelrate_boost', 'fuelrate_boost_water', 'speed', 'offspeed', 'waterspeed', 'boostspeed', 'boostspeed_off', 'boostspeed_water', 'zero_encumbrance_speed_mod', 'max_encumbrance_speed_mod', 'mobility', 'snow_immune', 'trigger_mines', 'shippable_size', 'storable', 'towing_power', 'towed_weight', 'intel_range', 'status', 'GalleryName', 'A1_ArmamentName', 'A1_ArmamentDesc', 'A1_AmmoName', 'A1_AmmoName2', 'A1_AmmoName3', 'A1_AmmoName4', 'A1_AmmoName5', 'A1_ReloadTime', 'A1_FiringTime', 'A1_RangeMax', 'A1_RangeEffective', 'A1_FireRate', 'A1_MagazineSize', 'A1_FiringArc', 'A1_RotationSpeed', 'A1_VelocityMod', 'A1_DeploymentNeeded', 'A1_ArtyAccMin', 'A1_ArtyAccMax', 'A1_ReloadImmobilizes', 'A1_HalfAngleMin', 'A1_HalfAngleMax', 'A1_Stability', 'A1_DirectFireRange', 'A2_ArmamentName', 'A2_ArmamentDesc', 'A2_AmmoName', 'A2_AmmoName2', 'A2_AmmoName3', 'A2_AmmoName4', 'A2_AmmoName5', 'A2_ReloadTime', 'A2_FiringTime', 'A2_RangeMax', 'A2_RangeEffective', 'A2_FireRate', 'A2_MagazineSize', 'A2_FiringArc', 'A2_RotationSpeed', 'A2_VelocityMod', 'A2_DeploymentNeeded', 'A2_ArtyAccMin', 'A2_ArtyAccMax', 'A2_ReloadImmobilizes', 'A2_HalfAngleMin', 'A2_HalfAngleMax', 'A2_Stability', 'A2_DirectFireRange', 'A3_ArmamentName', 'A3_ArmamentDesc', 'A3_AmmoName', 'A3_AmmoName2', 'A3_AmmoName3', 'A3_AmmoName4', 'A3_AmmoName5', 'A3_ReloadTime', 'A3_FiringTime', 'A3_RangeMax', 'A3_RangeEffective', 'A3_FireRate', 'A3_MagazineSize', 'A3_FiringArc', 'A3_RotationSpeed', 'A3_VelocityMod', 'A3_DeploymentNeeded', 'A3_ArtyAccMin', 'A3_ArtyAccMax', 'A3_ReloadImmobilizes', 'A3_HalfAngleMin', 'A3_HalfAngleMax', 'A3_Stability', 'A3_DirectFireRange', 'A4_ArmamentName', 'A4_ArmamentDesc', 'A4_AmmoName', 'A4_AmmoName2', 'A4_AmmoName3', 'A4_AmmoName4', 'A4_AmmoName5', 'A4_ReloadTime', 'A4_FiringTime', 'A4_RangeMax', 'A4_RangeEffective', 'A4_FireRate', 'A4_MagazineSize', 'A4_FiringArc', 'A4_RotationSpeed', 'A4_VelocityMod', 'A4_DeploymentNeeded', 'A4_ArtyAccMin', 'A4_ArtyAccMax', 'A4_ReloadImmobilizes', 'A4_HalfAngleMin', 'A4_HalfAngleMax', 'A4_Stability', 'A4_DirectFireRange']
STRUCTURES_TABLE_ALL_FIELDS = ['version', 'codename', 'aliases', 'name', 'image', 'imageOverride', 'staticImage', 'map_icon', 'map_icon_for_image', 'intelligence_icon', 'construction_type', 'type', 'built_with', 'build_material', 'build_amount', 'repair', 'maintenance_amount', 'slots', 'wrenchable', 'structure_hp', 'structure_hp_entrenched', 'armour_type', 'intel_range', 'faction', 'base_tier', 'decay_start', 'decay_duration', 'decay_RDZ_immune', 'husk_hp', 'husk_decay_start', 'husk_decay_duration', 'facility', 'ai_range', 'retaliation_range', 'firing_range_inac', 'fuelcap', 'fuelduration', 'fuelrate', 'fueltype', 'status', 'GalleryName', 'A1_ArmamentName', 'A1_ArmamentDesc', 'A1_AmmoName', 'A1_AmmoName2', 'A1_AmmoName3', 'A1_AmmoName4', 'A1_AmmoName5', 'A1_ReloadTime', 'A1_FiringTime', 'A1_RangeMax', 'A1_RangeEffective', 'A1_FireRate', 'A1_MagazineSize', 'A1_FiringArc', 'A1_RotationSpeed', 'A1_VelocityMod', 'A1_DeploymentNeeded', 'A1_ArtyAccMin', 'A1_ArtyAccMax', 'A1_ReloadImmobilizes', 'A1_HalfAngleMin', 'A1_HalfAngleMax', 'A1_Stability', 'A1_DirectFireRange']

HEALTH_TEST_DATA = [f'{entry['name']}@{entry['table']}' for entry in HEALTH_DATA if entry['table'] != 'custom_map']


def request_table_data(table_full_fields: list[str], table_name: str) -> dict[str, dict[str, str]] | None:
    res = requests.get(
        f'https://foxhole.wiki.gg/api.php?action=cargoquery&format=json&tables={table_name}&fields={','.join(table_full_fields)}&limit=500',
        timeout=5,
    )
    if res.status_code == 200:
        res = res.json()
        return {v['name']: v for entry_res in res['cargoquery'] for k, v in entry_res.items()}
    return None


@pytest.fixture(scope='session')
def structure_data():
    return request_table_data(STRUCTURES_TABLE_ALL_FIELDS, 'structures')


@pytest.fixture(scope='session')
def vehicle_data():
    return request_table_data(VEHICLES_TABLE_ALL_FIELDS, 'vehicles')


@pytest.mark.asyncio
@pytest.mark.parametrize('search_request', HEALTH_TEST_DATA)
async def test_health_command(structure_data, vehicle_data, search_request: str):
    search_request, health_table = search_request.split('@')


    if health_table == 'vehicles':
        entry_data = vehicle_data[search_request]
    else:
        entry_data = structure_data[search_request]

    entry_data['name'] = search_request

    entry_data['armour type'] = 'None'
    entry_data['image_url'] = ''
    entry_data['damages'] = ''
    entry_data['armor_attributes'] = ''

    # Compute health of search_request & generate embed
    health_embed = HealthEntryEngine(entry_data).get_generated_embed()

    assert len(health_embed), f'Health embed is empty for {search_request}'
