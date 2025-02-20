import typing
from enum import Enum, auto, EnumMeta


class EnumValue(EnumMeta):
    def __getattribute__(cls, name):
        """
        Allows to use the value as the default class
        :param name: attribute to use
        :return: value of name
        """
        value = super().__getattribute__(name)
        if isinstance(value, cls):
            value = value.value
        return value


class DamageTypes(EnumValue):
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
    CONFIG_DIR = 'guilds_config_files'


class DiscordIdType(Enum):
    USER = auto()
    ROLE = auto()


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


class InterfaceType(Enum):
    """
    Enum of possible interfaces types as name and list of associated table & column as value
    """
    REGISTER_VIEW: typing.ClassVar = []
    STOCKPILE_VIEW: typing.ClassVar = []
    TODOLIST_VIEW: typing.ClassVar = [('GroupsTodolistsAccess', 'TodolistId'), ('GroupsTodolistsTasks', 'TodolistId')]
    FACILITY_VIEW: typing.ClassVar = []


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


class FoxholeOfficialNames(EnumValue):
    AMMO_0_44MM = '.44'
    AMMO_7_62MM = '7.62mm'
    AMMO_7_92MM = '7.92mm'
    AMMO_8MM = '8mm'
    AMMO_9MM = '9mm'
    AMMO_12_7MM = '12.7mm'
    AMMO_20MM = '20mm'
    AMMO_30MM = '30mm'
    AMMO_40MM = '40mm'
    AMMO_68MM = '68mm'
    AMMO_75MM = '75mm'
    AMMO_94_5MM = '94.5mm'
    AMMO_120MM = '120mm'
    AMMO_150MM = '150mm'
    AMMO_250MM = '250mm'
    AMMO_300MM = '300mm'
    HARPA = 'A3 Harpa Fragmentation Grenade'
    BUCKSHOT = 'Buckshot'
    INFANTRY_MINE = "Crow's Foot Mine"
    TANK_MINE = 'Abisme AT-99'
    SEA_MINE = 'E680-S Rudder Lock'
    SEA_MINE_ALIAS = 'Sea Mine'
    GARRISON_HOUSE = 'Garrisoned House'
    SAFE_HOUSE = 'Safe House'
    TOWN_BASE = 'Town Base'
    RELIC_BASE = 'Relic Base'
    RIFLE_PILLBOX = 'Rifle Pillbox'
    MG_PILLBOX = 'Machine Gun Pillbox'
    AT_PILLBOX = 'Anti-Tank Pillbox'
    BOMASTONE = 'Bomastone Grenade'
    MORTAR_SHELL = 'Mortar Shell'
    MORTAR_SHRAPNEL_SHELL = 'Shrapnel Mortar Shell'
    MORTAR_FLARE_SHELL = 'Flare Mortar Shell'
    MORTAR_INCENDIARY_SHELL = 'Incendiary Mortar Shell'
    GAS_GRENADE = 'Green Ash Grenade'
    MAMMON = 'Mammon 91-b'
    RPG = 'RPG'
    TREMOLA_GRENADE = 'Tremola Grenade GPb-1'
    DEPTH_CHARGE = 'Model-7 “Evie”'
    DEPTH_CHARGE_ALIAS = 'Depth Charge'
    TORPEDO = 'Moray Torpedo'
    TORPEDO_ALIAS = 'Torpedo'
    SATCHEL = 'Alligator Charge'
    HAVOC_CHARGE = 'Havoc Charge'
    HYDRA = "Hydra's Whisper"
    AP_RPG = 'AP⧸RPG'
    ARC_RPG = 'ARC⧸RPG'
    IGNIFIST = 'Ignifist 30'
    STICKY_BOMB = 'Anti-Tank Sticky Bomb'
    VARSI = 'B2 Varsi Anti-Tank Grenade'
    FLASK = 'BF5 White Ash Flask Grenade'
    FLAMETHROWER_AMMO = 'Flamethrower Ammo'
    MOLTEN_WIND_AMMO = "“Molten Wind” v.II Ammo"
    FLAME_AMMO = 'Flame Ammo'
    WILLOWS_BANE_AMMO = "Willow's Bane Ammo"
    HIGH_EXPLOSIVE_ROCKET = '3C-High Explosive Rocket'
    FIRE_ROCKET = '4C-Fire Rocket'
    BAYONET = 'Buckhorn CCQ-18'
    SWORD = 'Eleos Infantry Dagger'
    CLUB = 'Falias Raiding Club'
    FISTS = 'Fists'
