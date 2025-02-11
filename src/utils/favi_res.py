from .oisol_enums import MaterialsNames, TimeDuration

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
                    MaterialsNames.CONSTRUCTION_MATERIALS: 5,
                    MaterialsNames.HEAVY_EXPLOSIVE_POWDER: 24,
                    MaterialsNames.POWER: 4,
                },
                {
                    MaterialsNames.MM_250: 1,
                },
                TimeDuration(seconds=30).time,
            ),
            # Flame Ammo
            (
                {
                    MaterialsNames.CONSTRUCTION_MATERIALS: 1,
                    MaterialsNames.HEAVY_EXPLOSIVE_POWDER: 4,
                    MaterialsNames.POWER: 4,
                },
                {
                    MaterialsNames.FLAME_AMMO: 1
                },
                TimeDuration(seconds=25).time,
            ),
            # Sea Mine
            (
                {
                    MaterialsNames.CONSTRUCTION_MATERIALS: 1,
                    MaterialsNames.HEAVY_EXPLOSIVE_POWDER: 8,
                    MaterialsNames.POWER: 4,
                },
                {
                    MaterialsNames.SEA_MINE: 1,
                },
                TimeDuration(minutes=1, seconds=30).time,
            ),
            # Thermal Shielding
            (
                {
                    MaterialsNames.CONSTRUCTION_MATERIALS: 2,
                    MaterialsNames.ASSEMBLY_MATERIALS_IV: 5,
                    MaterialsNames.POWER: 4,
                },
                {
                    MaterialsNames.THERMAL_SHIELDING: 1,
                },
                TimeDuration(minutes=25).time,
            ),
            # Infantry Mine
            (
                {
                    MaterialsNames.EXPLOSIVE_POWDER: 2,
                    MaterialsNames.CONSTRUCTION_MATERIALS: 2,
                    MaterialsNames.POWER: 4,
                },
                {
                    MaterialsNames.INFANTRY_MINE: 1,
                },
                TimeDuration(seconds=25).time,
            ),
            # Tank Mine
            (
                {
                    MaterialsNames.HEAVY_EXPLOSIVE_POWDER: 2,
                    MaterialsNames.CONSTRUCTION_MATERIALS: 2,
                    MaterialsNames.POWER: 4,
                },
                {
                    MaterialsNames.TANK_MINE: 1,
                },
                TimeDuration(seconds=25).time,
            ),
        ]
    }
}