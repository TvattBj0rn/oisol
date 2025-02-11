from .oisol_enums import ResourcesNames, TimeDuration

# This dict contains all existing facility buildings with crafts and their queues per variant.
# FACILITY_QUEUES (dict) = building_name: building_variants (dict) -> building_variants should include the base one with key building_name
# building_variants (dict) = variant_name: variants_queues (list)
# variants_queues (list) = [({inputs_costs (dict)}, outputs (dict), time_duration (int))]
FACILITIES_QUEUES = {
    'Ammunition Factory': {
        'Ammunition Factory': [
            # 250mm
            (
                {
                    ResourcesNames.CONSTRUCTION_MATERIALS: 5,
                    ResourcesNames.HEAVY_EXPLOSIVE_POWDER: 24,
                    ResourcesNames.POWER: 4,
                },
                {
                    ResourcesNames.MM_250: 1,
                },
                TimeDuration(seconds=30).time,
            ),
            # Flame Ammo
            (
                {
                    ResourcesNames.CONSTRUCTION_MATERIALS: 1,
                    ResourcesNames.HEAVY_EXPLOSIVE_POWDER: 4,
                    ResourcesNames.POWER: 4,
                },
                {
                    ResourcesNames.FLAME_AMMO: 1
                },
                TimeDuration(seconds=25).time,
            ),
            # Sea Mine
            (
                {
                    ResourcesNames.CONSTRUCTION_MATERIALS: 1,
                    ResourcesNames.HEAVY_EXPLOSIVE_POWDER: 8,
                    ResourcesNames.POWER: 4,
                },
                {
                    ResourcesNames.SEA_MINE: 1,
                },
                TimeDuration(minutes=1, seconds=30).time,
            ),
            # Thermal Shielding
            (
                {
                    ResourcesNames.CONSTRUCTION_MATERIALS: 2,
                    ResourcesNames.ASSEMBLY_MATERIALS_IV: 5,
                    ResourcesNames.POWER: 4,
                },
                {
                    ResourcesNames.THERMAL_SHIELDING: 1,
                },
                TimeDuration(minutes=25).time,
            ),
            # Infantry Mine
            (
                {
                    ResourcesNames.EXPLOSIVE_POWDER: 2,
                    ResourcesNames.CONSTRUCTION_MATERIALS: 2,
                    ResourcesNames.POWER: 4,
                },
                {
                    ResourcesNames.INFANTRY_MINE: 1,
                },
                TimeDuration(seconds=25).time,
            ),
            # Tank Mine
            (
                {
                    ResourcesNames.HEAVY_EXPLOSIVE_POWDER: 2,
                    ResourcesNames.CONSTRUCTION_MATERIALS: 2,
                    ResourcesNames.POWER: 4,
                },
                {
                    ResourcesNames.TANK_MINE: 1,
                },
                TimeDuration(seconds=25).time,
            ),
        ],
    }
}