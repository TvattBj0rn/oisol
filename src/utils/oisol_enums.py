from enum import Enum, auto


class DamageTypes(Enum):
    LIGHT_KINETIC = 'Light Kinetic'
    HEAVY_KINETIC = 'Heavy Kinetic'
    ANTI_TANK_KINETIC = 'Anti-Tank Kinetic'
    ANTI_TANK_KINETIC_STRUCTURE = 'Anti-Tank Kinetic Structure'
    SHRAPNEL = 'Shrapnel'
    FLARE = 'Flare'
    POISONOUS_GAS = 'Poisonous Gas'
    EXPLOSIVE = 'Explosive'
    HIGH_EXPLOSIVE = 'High Explosive'
    DEMOLITION = 'Demolition'
    ARMOUR_PIERCING = 'Armour Piercing'
    ANTI_TANK_EXPLOSIVE = 'Anti-Tank Explosive'
    INCENDIARY = 'Incendiary'
    INCENDIARY_HIGH_EXPLOSIVE = 'Incendiary High Explosive'
    MELEE = 'Melee'


class DataFilesPath(Enum):
    REGISTER = 'register.csv'
    STOCKPILES = 'stockpiles.csv'
    CONFIG = 'config.ini'


class EmbedIds(Enum):
    STOCKPILES_VIEW = 'Stockpiles Viewer'
    REGISTER_VIEW = 'Register Viewer'


class Faction(Enum):
    WARDEN = 0x245682
    COLONIAL = 0x516C4B
    NEUTRAL = 0xffffff


class FoxholeBuildings(Enum):
    STORAGE_DEPOT = '<:storagedepotw:1130918748648394822>'
    SEAPORT = '<:seaportw:1130918734769442868>'
    SEAPORT_WARDEN = '<:seaport_warden:1272594645809107097>'
    SEAPORT_COLONIAL = '<:seaport_colonial:1272594646920331265>'
    SEAPORT_NEUTRAL = '<:seaport_neutral:1077298856196313158>'
    STORAGE_DEPOT_WARDEN = '<:storage_depot_warden:1272594650284167208>'
    STORAGE_DEPOT_COLONIAL = '<:storage_depot_colonial:1272594648757436457>'
    STORAGE_DEPOT_NEUTRAL = '<:storage_depot_neutral:1077298889490694204>'


class Language(Enum):
    FR = auto()
    EN = auto()
    DE = auto()
    ES = auto()


class Modules(Enum):
    CONFIG = auto()
    REGISTER = auto()
    STOCKPILE = auto()
    TODOLIST = auto()
    WIKI = auto()


class PriorityType(Enum):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'

class Shard(Enum):
    ABLE = 'https://war-service-live.foxholeservices.com/api'
    BAKER = 'https://war-service-live-2.foxholeservices.com/api'
    CHARLIE = 'https://war-service-live-3.foxholeservices.com/api'
    DEVBRANCH = 'https://war-service-dev.foxholeservices.com/api'
