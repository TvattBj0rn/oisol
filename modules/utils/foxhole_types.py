from enum import Enum

FACTION_COLORS = {
    'Warden': 0x245682,
    'Colonial': 0x516C4B,
    'Both': 0xffffff
}

class StockpileTypes(Enum):
    # STORAGE_DEPOT = '<:storagedepot:1077298889490694204>' # Neutral color
    # SEAPORT = '<:seaport:1077298856196313158>' # Neutral color
    REGION = '<:region:1130915923704946758>'
    STORAGE_DEPOT = '<:storagedepotw:1130918748648394822>'
    SEAPORT = '<:seaportw:1130918734769442868>'