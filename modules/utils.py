from enum import Enum


class Language(Enum):
    FR = 'french'
    EN = 'english'
    DE = 'german'
    ES = 'spanish'


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


def safeguarded_nickname(nickname: str) -> str:
    """
    Function required as discord does not allow for nicknames longer than 32 characters.
    :param nickname: wanted name
    :return: nickname equal or shortened to 32 chars
    """
    return nickname[:32 - len(nickname)] if len(nickname) > 32 else nickname


MODULES_CSV_KEYS = {
    'stockpiles': ['region', 'subregion', 'code', 'name', 'type'],
    'register': ['member', 'timer'],
    'todolist': ['content', 'priority'],
}

EMOTES_CUSTOM_ID = {
    '🇦': 'TodoButtonA',
    '🇧': 'TodoButtonB',
    '🇨': 'TodoButtonC',
    '🇩': 'TodoButtonD',
    '🇪': 'TodoButtonE',
    '🇫': 'TodoButtonF',
    '🇬': 'TodoButtonG',
    '🇭': 'TodoButtonH',
    '🇮': 'TodoButtonI',
    '🇯': 'TodoButtonJ',
    '🇰': 'TodoButtonK',
    '🇱': 'TodoButtonL',
    '🇲': 'TodoButtonM',
    '🇳': 'TodoButtonN',
    '🇴': 'TodoButtonO',
    '🇵': 'TodoButtonP',
    '🇶': 'TodoButtonQ',
    '🇷': 'TodoButtonR',
    '🇸': 'TodoButtonS',
    '🇹': 'TodoButtonT',
    '🇺': 'TodoButtonU',
    '🇻': 'TodoButtonV',
    '🇼': 'TodoButtonW',
    '🇽': 'TodoButtonX',
    '🇾': 'TodoButtonY',
    '🇿': 'TodoButtonZ'
}


REGIONS = {
    'Acrithia': ['Patridia', 'Nereid Kepp', 'The Brimehold', 'Legion Ranch', 'Camp Omicron', 'Heir Apparent', 'Thetus Ring', 'Swordfort'],
    "Allod's Bight": ['The Stone Plank', "Mercy's Wail", 'The Turncoat', 'Belaying Trace', 'Homesick', 'Rumhold', 'Scurvyshire'],
    'Ash Fields': ['Cometa', 'The Calamity', 'Ashtown', 'Sootflow', 'The Ashfort', 'Camp Omega', 'Electi'],
    'Basin Sionnach': ['Cuttail Station', 'Stoic', 'Lamplight', 'The Den', 'Bassinhome', 'Sess'],
    "Callahan's Passage": ['Cragstown', 'White Chapel', 'The Procession', 'The Latch', 'Overlook Hill', 'Crumbling Passage', 'Crumbling Post', 'Scáth Passing', 'Lochan Berth', 'Solas Gorge'],
    "Callum's Cape": ['Naofa', 'Scouts Jest', 'Ire', 'Lookout', 'Holdout', 'Camp Hollow', "Callum's Keep"],
    'Clanshead Valley': ['Fallen Crown', 'Fort Windham', 'The King', 'Sweetholt', 'Fort Esterwild', 'The Pike', 'Fort Ealar'],
    'Deadlands': ['The Salt Farms', 'Brine Glen', 'The Salt March', "Callahan's Gate", "Callahan's Boot", "Iron's End", 'The Spine', 'Liberation Point', "Sun's Hollow", 'The Pits', 'Abandoned Ward'],
    'Endless Shore': ['Iron Junction', 'The Overland', 'Woodbind', 'Tuatha Watchpost', 'Evil Eye', 'Dannan Ridge', 'Vulpine Watch', 'Wellchurch', 'Brackish Point', 'Saltbrook Channel', 'Enduring Wake', 'The Old Jack Tar'],
    'Farranac Coast': ['Victa', 'Pleading Wharf', "Macha's Keening", 'Mara', 'Scythe', 'The Jade Cove', 'Scarp of Ambrose', 'Luxta Homestead', 'The Bone Haft', 'The Spearhead', 'Terra'],
    "Fisherman's Row": ['Arcadia', 'Fort Ember', 'The Satyr Stone', "Hangmen's Court", 'The Tree Sisters', 'Eidolo', 'Peripti Landing', 'Black Well', 'Oceanwatch', 'Partisan Island'],
    'Godcrofts': ['Anchor Beach', 'Blackwatch', 'Protos', 'The Axehead', 'Skodio', 'Promithiens', 'Isawa', 'The Fleece Road'],
    'Great March': ['Violethome', 'Leto', 'Camo Senti', "Myrmidon's Stay", 'Remnant Villa', 'Lionsfort', 'Dendro Field', "Sitaria", 'The Swan'],
    'Howl County': ['Hungry Wolf', 'Slipgate Outpost', 'Great Warden Dam', 'Fort Red', 'Sickelshire', 'Little Lamb', 'Teller Farm', 'Fort Rider'],
    'Kalokai': ["Night's Regret", 'Sourtooth', 'Sweetearth', 'Camp Tau', 'Hallow', 'Baccae Ridge', 'Lost Greensward'],
    'Loch Mór': ['Market Road', 'Tomb of the First', "Mercy's Wish", 'Westmarch', "Moon's Copse", 'The Roilfort', 'Feirmor'],
    'Marban Hollow': ['Lockheed', 'Oster Wall', 'Mox', 'Checkpoint Bua', "Maiden's Veil", 'The Spitrocks', 'Sanctum'],
    "Morgen's Crossing": ['Eversus', 'Allsight', "Bastard's Block", 'Quietus', 'Lividus', 'Warmonger Bay'],
    'Nevish Line': ['Blinding Stones', 'The Scrying Belt', 'Unruly', 'Mistle Shrine', 'Grief Mother', 'Princefal', 'Blackcoat Way', 'Tomb Father'],
    'Origin': ['Finis', 'Arise', 'Initium', 'Dormio', 'World Star', 'Teichotima'],
    'Reaching Trail': ['Limestone Holdfast', 'Dwyerstown', 'Brodytown', 'Elksford', 'Ice Ranch', 'Nightchurch', 'Harpy', 'Reprieve', "Fort Mac Conaill's", 'The Ark', 'Mousetrap'],
    'Red River': ['Camp Upsilon', 'Penance', 'Fort Matchwood', 'Climb', 'Judicium', 'Victoria Hill', 'Cannonsmoke', 'Minos'],
    'Schackeld Chasm': ['Savages', 'The Grave of Erastos', 'The Beli Toll', 'Firstmarch', 'The Vanguard', 'Limewood Holdfast', 'Gorgon Grove', 'Reflection', 'Silk Farm', "Simo's Run"],
    'Speaking Woods': ['Hush', 'Inari Base', 'Tine', 'Sotto Bank', 'Fort Blather', 'Stem', 'The Filament', 'Wound'],
    'Stonecradle': ['The Dais', 'The Reach', 'Trammel Pool', 'Fading Lights', 'The Cord', 'Buckler Sound', "World's End", "The Heir's Knife", 'The Long Fast'],
    'Tempest Island': ['Isle of Psyche', 'The Gale', "Liar's Heaven", 'The Iris', 'Surge Gate', 'The Rush', 'Reef', 'Lost Airchal', 'Alchimio Estate'],
    'Terminus': ['Therizó', 'Bloody Palm', 'Winding Bolas', 'Thunderbolt', "Warlord's Stead", 'Cerberus Wake'],
    'The Drowned Vale': ['Loggerhead', "Wisp's Warning", 'The Wash', 'Eastmarch', 'Vessel', 'Splinter Pens', 'The Baths', 'Coaldrifter Stead', 'Bootnap', 'Singing Serpents', 'The Saltcaps'],
    'The Fingers': ['Titancall', 'The Old Captain', 'Fort Barley', 'Second Man', 'The Routed', 'The Tusk', "Headsman's Villa", 'Plankhouse'],
    'The Heartlands': ['Deeplaw Post', 'The Breach', 'Barrony Ranch', 'The Plough', 'Greenfield Orchard', 'Fort Providence', 'The Blemish', 'Barronswall', 'Oleander Homestead', 'Proexí'],
    'The Linn of Mercy': ['The Long Whine', 'Rotdust', 'Lathair', 'Outwich Ranch', 'Fort Duncan', 'The Prairie Bazaar', 'The First Coin', 'The Last Grove', 'The Crimson Gardens', 'Hardline', 'Ulster Falls'],
    'The Moors': ['Reaching River', 'The Spade', 'Headstone', "Gravekeeper's Holdfast", 'The Cut', 'The Wind Hills', 'MacConmara Barrows', 'Wiccwalk', "Morrighan's Grave", "Luch's Workshop", 'Borderlane', 'Reaching River', 'Ogmaran'],
    'The Oarbreaker Isles': ['Gold', 'Reliqua', 'The Ides', 'Posterus', 'Skelter Course', 'The Conclave', "Lion's Head", 'Integrum', 'Base Akri'],
    'Umbral Wildwood': ['The Foundry', 'Golden Root Ranch', 'Thunderfoot', 'Sentry', "Atropos' Fate", "Hermit's Rest", "Lachesis' Tally", 'Amethyst', "Clotho's Refuge", 'Vagrant Bastion', 'Stray'],
    'Viper Pit': ["Serenity's Blight", 'Flech Crossing', 'Earl Crowley', 'Molworth', 'Blackthroat', 'The Friars', 'Fort Viêr', 'Fleck Crossing', 'Kirknell'],
    'Weathered Expanse': ['The Weathering Halls', 'Port of Rime', 'Wightwalk', 'Huntsfort', 'Shattered Advance', 'Frostmarch', "Crow's Nest", 'Necropolis', 'Foxcatcher'],
    'Westgate': ['Sanctuary', 'The Gallows', 'Holdfast', "Rancher's Fast", 'Kingstown', "Lord's Mouth", 'Lost Partition', 'Westgate Keep', 'Longstone', "Zeus' Demise", 'Wyattwick']
}


REGIONS_STOCKPILES = {
    'Acrithia': [('Legion Ranch', FoxholeBuildings.STORAGE_DEPOT.value), ('Patridia', FoxholeBuildings.SEAPORT.value), ('Thetus Ring', FoxholeBuildings.STORAGE_DEPOT.value)],
    "Allod's Bight": [("Mercy's Wail", FoxholeBuildings.SEAPORT.value), ('Scurvyshire', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Ash Fields': [('Ashtown', FoxholeBuildings.SEAPORT.value), ('Electi', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Basin Sionnach': [('Cuttail Station', FoxholeBuildings.SEAPORT.value), ('Sess', FoxholeBuildings.STORAGE_DEPOT.value), ('The Den', FoxholeBuildings.STORAGE_DEPOT.value)],
    "Callahan's Passage": [('Lochan Berth', FoxholeBuildings.SEAPORT.value), ('Solas Gorge', FoxholeBuildings.STORAGE_DEPOT.value)],
    "Callum's Cape": [("Callum's Keep", FoxholeBuildings.SEAPORT.value), ('Holdout', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Clanshead Valley': [('The King', FoxholeBuildings.SEAPORT.value), ('The Pike', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Deadlands': [('Abandoned Ward', FoxholeBuildings.STORAGE_DEPOT.value), ('Brine Glen', FoxholeBuildings.STORAGE_DEPOT.value), ("Callahan's Gate", FoxholeBuildings.STORAGE_DEPOT.value), ('The Salt Farms', FoxholeBuildings.STORAGE_DEPOT.value), ('The Spine', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Endless Shore': [('Brackish Point', FoxholeBuildings.STORAGE_DEPOT.value), ('Iron Junction', FoxholeBuildings.STORAGE_DEPOT.value), ('Saltbrook Channel', FoxholeBuildings.SEAPORT.value)],
    'Farranac Coast': [('Mara', FoxholeBuildings.STORAGE_DEPOT.value), ('The Jade Cove', FoxholeBuildings.SEAPORT.value), ('Victa', FoxholeBuildings.STORAGE_DEPOT.value)],
    "Fisherman's Row": [('Black Well', FoxholeBuildings.STORAGE_DEPOT.value), ('Eidolo', FoxholeBuildings.SEAPORT.value), ("Hangmen's Court", FoxholeBuildings.STORAGE_DEPOT.value), ('Partisan Island', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Godcrofts': [('Blackwatch', FoxholeBuildings.STORAGE_DEPOT.value), ('Skodio', FoxholeBuildings.STORAGE_DEPOT.value), ('The Axehead', FoxholeBuildings.SEAPORT.value)],
    'Great March': [("Myrmidon's Stay", FoxholeBuildings.STORAGE_DEPOT.value), ('Sitaria', FoxholeBuildings.STORAGE_DEPOT.value), ('Violethome', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Howl County': [('Great Warden Dam', FoxholeBuildings.SEAPORT.value), ('Hungry Wolf', FoxholeBuildings.STORAGE_DEPOT.value), ('Little Lamb', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Kalokai': [('Baccae Ridge', FoxholeBuildings.SEAPORT.value), ('Hallow', FoxholeBuildings.STORAGE_DEPOT.value), ('Sweetearth', FoxholeBuildings.STORAGE_DEPOT.value)],
    "King's Cage": [('Gibbet Fields', FoxholeBuildings.STORAGE_DEPOT.value), ('The Manacle', FoxholeBuildings.SEAPORT.value)],
    'Loch Mór': [('Feirmor', FoxholeBuildings.SEAPORT.value), ("Mercy's Wish", FoxholeBuildings.STORAGE_DEPOT.value)],
    'Marban Hollow': [('Lockheed', FoxholeBuildings.STORAGE_DEPOT.value), ("Maiden's Veil", FoxholeBuildings.SEAPORT.value)],
    "Morgen's Crossing": [('Allsight', FoxholeBuildings.STORAGE_DEPOT.value), ('Lividus', FoxholeBuildings.STORAGE_DEPOT.value), ('Quietus', FoxholeBuildings.SEAPORT.value)],
    'Nevish Line': [('Blackcoat Way', FoxholeBuildings.STORAGE_DEPOT.value), ('Mistle Shrine', FoxholeBuildings.STORAGE_DEPOT.value), ('The Scrying Belt', FoxholeBuildings.SEAPORT.value)],
    'Origin': [('Finis', FoxholeBuildings.STORAGE_DEPOT.value), ('Initium', FoxholeBuildings.SEAPORT.value), ('Teichotima', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Reaching Trail': [('Brodytown', FoxholeBuildings.STORAGE_DEPOT.value), ('Nightchurch', FoxholeBuildings.STORAGE_DEPOT.value), ('Reprieve', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Red River': [('Cannonsmoke', FoxholeBuildings.SEAPORT.value), ('Judicium', FoxholeBuildings.STORAGE_DEPOT.value), ('Penance', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Sableport': [('Barronhome', FoxholeBuildings.STORAGE_DEPOT.value), ('Cinderwick', FoxholeBuildings.STORAGE_DEPOT.value), ("Light's End", FoxholeBuildings.SEAPORT.value)],
    'Schackeld Chasm': [('Savages', FoxholeBuildings.STORAGE_DEPOT.value), ('Silk Farm', FoxholeBuildings.SEAPORT.value), ('The Grave of Erastos', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Speaking Woods': [('Sotto Bank', FoxholeBuildings.STORAGE_DEPOT.value), ('The Filament', FoxholeBuildings.STORAGE_DEPOT.value), ('Tine', FoxholeBuildings.SEAPORT.value)],
    'Stonecradle': [('Buckler Sound', FoxholeBuildings.SEAPORT.value), ('Fading Lights', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Tempest Island': [('Alchimio Estate', FoxholeBuildings.STORAGE_DEPOT.value), ('Isle of Psyche', FoxholeBuildings.STORAGE_DEPOT.value), ("Liar's Heaven", FoxholeBuildings.SEAPORT.value)],
    'Terminus': [('Therizó', FoxholeBuildings.STORAGE_DEPOT.value), ("Warlord's Stead", FoxholeBuildings.SEAPORT.value)],
    'The Drowned Vale': [('Loggerhead', FoxholeBuildings.STORAGE_DEPOT.value), ('The Baths', FoxholeBuildings.SEAPORT.value)],
    'The Fingers': [("Headsman's Villa", FoxholeBuildings.STORAGE_DEPOT.value), ('The Old Captain', FoxholeBuildings.SEAPORT.value), ('The Routed', FoxholeBuildings.STORAGE_DEPOT.value)],
    'The Heartlands': [('Greenfield Orchard', FoxholeBuildings.STORAGE_DEPOT.value), ('The Blemish', FoxholeBuildings.STORAGE_DEPOT.value)],
    'The Linn of Mercy': [('The Prairie Bazaar', FoxholeBuildings.STORAGE_DEPOT.value), ('Ulster Falls', FoxholeBuildings.SEAPORT.value)],
    'The Moors': [("Morrighan's Grave", FoxholeBuildings.STORAGE_DEPOT.value), ('Ogmaran', FoxholeBuildings.SEAPORT.value)],
    'The Oarbreaker Isles': [('Integrum', FoxholeBuildings.STORAGE_DEPOT.value), ('Skelter Course', FoxholeBuildings.SEAPORT.value), ('The Ides', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Umbral Wildwood': [("Hermit's Rest", FoxholeBuildings.STORAGE_DEPOT.value), ('Thunderfoot', FoxholeBuildings.SEAPORT.value)],
    'Viper Pit': [('Earl Crowley', FoxholeBuildings.STORAGE_DEPOT.value), ('Kirknell', FoxholeBuildings.SEAPORT.value)],
    'Weathered Expanse': [("Crow's Nest", FoxholeBuildings.STORAGE_DEPOT.value), ('Foxcatcher', FoxholeBuildings.STORAGE_DEPOT.value), ('Port of Rime', FoxholeBuildings.SEAPORT.value)],
    'Westgate': [('Kingstown', FoxholeBuildings.STORAGE_DEPOT.value), ('Longstone', FoxholeBuildings.SEAPORT.value), ('The Gallows', FoxholeBuildings.STORAGE_DEPOT.value)]
}

REGIONS_NAMES_API = [
    'HomeRegionC',
    'HomeRegionW',
    'AcrithiaHex',
    'AllodsBightHex',
    'AshFieldsHex',
    'BasinSionnachHex',
    'CallahansPassageHex',
    'CallumsCapeHex',
    'ClansheadValleyHex',
    'DeadlandsHex',
    'DrownedValeHex',
    'EndlessShoreHex',
    'FarranacCoastHex',
    'FishermansRowHex',
    'GodcroftsHex',
    'GreatMarchHex',
    'HeartlandsHex',
    'HowlCountyHex',
    'KalokaiHex',
    'KingsCageHex',
    'LinnMercyHex',
    'LochMorHex',
    'MarbanHollow',
    'MooringCountyHex',
    'MorgensCrossingHex',
    'NevishLineHex',
    'OarbreakerHex',
    'OriginHex',
    'ReachingTrailHex',
    'RedRiverHex',
    'SableportHex',
    'ShackledChasmHex',
    'SpeakingWoodsHex',
    'StonecradleHex',
    'TempestIslandHex',
    'TerminusHex',
    'TheFingersHex',
    'UmbralWildwoodHex',
    'ViperPitHex',
    'WeatheredExpanseHex',
    'WestgateHex'
]
