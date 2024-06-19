from enum import Enum, auto


class Language(Enum):
    FR = auto()
    EN = auto()
    DE = auto()
    ES = auto()


class Faction(Enum):
    WARDEN = 0x245682
    COLONIAL = 0x516C4B
    NEUTRAL = 0xffffff


class DataFilesPath(Enum):
    REGISTER = 'register.csv'
    STOCKPILES = 'stockpiles.csv'
    CONFIG = 'config.ini'


class EmbedIds(Enum):
    STOCKPILES_VIEW = 'Stockpiles Viewer'
    REGISTER_VIEW = 'Register Viewer'


class FoxholeBuildings(Enum):
    STORAGE_DEPOT = '<:storagedepotw:1130918748648394822>'
    SEAPORT = '<:seaportw:1130918734769442868>'


class PriorityType(Enum):
    HAUTE = 'high'
    MOYENNE = 'medium'
    BASSE = 'low'
