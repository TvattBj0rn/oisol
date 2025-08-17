from enum import Enum, EnumMeta, auto


class EnumValue(EnumMeta):
    def __getattribute__(cls, name: str):
        """
        Allows to use the value as the default class
        :param name: attribute to use
        :return: value of name
        """
        value = super().__getattribute__(name)
        if isinstance(value, cls):
            value = value.value
        return value


class CacheKeys(EnumValue):
    WORLD_SPAWNS_STATUS = 'world_spawn_status'


class DataFilesPath(Enum):
    CONFIG_DIR = 'guilds_config_files'


class DiscordIdType(Enum):
    USER = auto()
    ROLE = auto()


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


class InterfaceType(Enum):
    """
    Enum of possible interfaces types as name and list of associated table & column as value
    """
    MULTISERVER_STOCKPILE_VIEW = []
    REGISTER_VIEW = []
    STOCKPILE_VIEW = []
    TODOLIST_VIEW = [('GroupsInterfacesAccess', 'InterfaceId'), ('GroupsTodolistsTasks', 'TodolistId')]


class InterfacesTypes(Enum):
    """
    Enum of possible interfaces types as name and list of associated table & column as value
    """
    MULTISERVER_STOCKPILE = 'MULTISERVER_STOCKPILE_VIEW'
    REGISTER = 'REGISTER_VIEW'
    STOCKPILE = 'STOCKPILE_VIEW'
    TODOLIST = 'TODOLIST_VIEW'


class PriorityType(Enum):
    HIGH = '🟥'
    MEDIUM = '🟨'
    LOW = '🟩'


class Shard(Enum):
    ABLE = 'https://war-service-live.foxholeservices.com/api'
    BAKER = 'https://war-service-live-2.foxholeservices.com/api'
    CHARLIE = 'https://war-service-live-3.foxholeservices.com/api'
    DEVBRANCH = 'https://war-service-dev.foxholeservices.com/api'


class MapIcon(Enum):
    FORWARD_BASE_1 = 8
    HOSPITAL = 11
    GARAGE = 12
    REFINERY = 17
    SHIPYARD = 18
    ENGINEERING_CENTER = 19
    SALVAGE_FIELD = 20
    COMPONENT_FIELD = 21
    FUEL_FIELD = 22
    SULFUR_FIELD = 23
    WORLD_MAP_TENT = 24
    TRAVEL_TENT = 25
    TRAINING_AREA = 26
    KEEP = 27
    OBSERVATION_TOWER = 28
    FORT = 29
    TROOP_SHIP = 30
    SULFUR_MINE = 32
    STORAGE_DEPOT = 33
    FACTORY = 34
    GARRISON_STATION = 35
    ROCKET_SITE = 37
    SALVAGE_MINE = 38
    CONSTRUCTION_YARD = 39
    COMPONENT_MINE = 40
    RELIC_BASE_1 = 45
    MPF = 51
    SEAPORT = 52
    COASTAL_GUN = 53
    SOUL_FACTORY = 54
    TOWN_BASE_1 = 56
    TOWN_BASE_2 = 57 # For the town bases, the integer refers to the tier of the town base, not its type
    TOWN_BASE_3 = 58
    STORM_CANON = 59
    INTEL_CENTER = 60
    COAL_FIELD = 61
    OIL_FIELD = 62
    ROCKET_TARGET = 70
    ROCKET_GROUND_ZERO = 71
    ROCKET_SITE_WITH_ROCKET = 72
    FACILITY_MINE_OIL_RIG = 75
    WEATHER_STATION = 83
    MORTAR_HOUSE = 84


class WikiTables(Enum):
    ARMAMENT = 'armament'
    DAMAGE_TYPES = 'damagetypes'
    ICON_DATA = 'icondata'
    ITEM_DATA = 'itemdata'
    MAPS = 'maps'
    PRODUCTION = 'production'
    PRODUCTION_SHIPPABLE = 'productionshippable'
    PRODUCTION_VEHICLE = 'productionvehicle'
    STRUCTURES = 'structures'
    VEHICLES = 'vehicles'
    VEHICLE_CLASS = 'VehicleClass'


class WorldSpawnTypes(Enum):
    RELIC_SMALL = 'Relic Base (Small)'
    RELIC_MEDIUM = 'Relic Base (Medium)'
    RELIC_LARGE = 'Relic Base (Large)'
    TOWN_BASE_POST_OFFICE = 'Post Office'
    TOWN_BASE_SCHOOL = 'School'
    TOWN_BASE_CENTER = 'Town Center'
