from dataclasses import dataclass
from enum import Enum, auto, EnumMeta


@dataclass
class NameEmojiPair:
    display_name: str
    emoji: str | None = None
    aliases: list[str] | None = None

    def __post_init__(self) -> None:
        """
        Ensure proper data is displayed on the interfaces
        """
        if self.emoji is None:
            self.emoji = self.display_name

    def __getitem__(self, display_name: str) -> str:
        """
        Allows dict like access to retrieve the emoji from display name
        :param display_name:
        :return: emoji attribute if the given name has the same value as the display_name attribute, given_name otherwise
        """
        if display_name == self.display_name or (self.aliases is not None and display_name in self.aliases):
            return self.emoji
        return display_name


@dataclass
class TimeDuration:
    """
    Class to store time as seconds
    """
    seconds: int = 0
    minutes: int = 0
    hours: int = 0
    days: int = 0
    time : int = 0

    def __post_init__(self):
        self.time = self.seconds + self.minutes * 60 + self.hours * 3600 + self.days * 86400


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
    EN = auto()
    FR = auto()


class InterfaceType(Enum):
    """
    Enum of possible interfaces types as name and list of associated table & column as value
    """
    REGISTER_VIEW = []
    STOCKPILE_VIEW = []
    TODOLIST_VIEW = [('GroupsTodolistsAccess', 'TodolistId'), ('GroupsTodolistsTasks', 'TodolistId')]
    FACILITY_VIEW = []


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

class EntitiesNames(EnumMeta):
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


class ResourcesNames(EntitiesNames):
    CONSTRUCTION_MATERIALS = NameEmojiPair('Construction Materials', '<:cmat:1239353162616279122>')
    EXPLOSIVE_POWDER = NameEmojiPair('Explosive Powder', '<:emat:1327687090590449818>')
    HEAVY_EXPLOSIVE_POWDER = NameEmojiPair('Heavy Explosive Powder', '<:hemat:1327688754617647184>')
    POWER = NameEmojiPair('MW of power', '<:mw_of_power:1327439074184794185>')
    ASSEMBLY_MATERIAL_I = NameEmojiPair('Assembly Materials I', '<:asmat1:1239353117120659557>')
    ASSEMBLY_MATERIAL_II = NameEmojiPair('Assembly Materials II', '<:asmat2:1239353144484302953>')
    ASSEMBLY_MATERIAL_III = NameEmojiPair('Assembly Materials III', '<:asmat3:1239353124653760584>')
    ASSEMBLY_MATERIALS_IV = NameEmojiPair('Assembly Materials IV', '<:asmat4:1239353135772995584>')
    ASSEMBLY_MATERIAL_V = NameEmojiPair('Assembly Materials V', '<:asmat5:1239353106404474951>')
    FLAME_AMMO = NameEmojiPair('Flame Ammo', '<:flame_ammo:1317941665016844392>')
    SEA_MINE = NameEmojiPair('Sea Mine', '<:sea_mine:1244048778063773716>', ['E680-S Rudder Lock'])
    INFANTRY_MINE = NameEmojiPair("Crow's Foot Mine")
    TANK_MINE = NameEmojiPair('Abisme AT-99', '<:landmine:1088831369762848850>')
    THERMAL_SHIELDING = NameEmojiPair('Thermal Shielding', '<:thermal_shielding:1251473216111640586>')

class AmmunitionNames(EntitiesNames):
    BUCKSHOT = NameEmojiPair('', '')
    MM_44 = NameEmojiPair('', '')
    MM_7_62 = NameEmojiPair('', '')
    MM_7_92 = NameEmojiPair('', '')
    MM_8 = NameEmojiPair('', '')
    MM_9 = NameEmojiPair('', '')
    MM_12_7 = NameEmojiPair('', '')
    MM_250 = NameEmojiPair('250mm', '<:250mm:1239630880289329262>')


if __name__ == '__main__':
    print(ResourcesNames.CONSTRUCTION_MATERIALS.display_name)
    print(TimeDuration(minutes=30).time)
    # print(NameEmojiPair('Explosive Powder', 'test')['Explosive Powder'])

