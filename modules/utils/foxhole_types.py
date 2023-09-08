from enum import Enum


FACTION_COLORS = {
    'Warden': 0x245682,
    'Colonial': 0x516C4B,
    'Both': 0xffffff
}


class StockpileTypes(Enum):
    REGION = '<:region:1130915923704946758>'
    STORAGE_DEPOT = '<:storagedepotw:1130918748648394822>'
    SEAPORT = '<:seaportw:1130918734769442868>'