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


EMOJIS_FROM_DICT = {
    'Light Kinetic': '<:light_kinetic:1239343508725174355>',
    'Heavy Kinetic': '<:heavy_kinetic:1239343499787112490>',
    'Anti-Tank Kinetic': '<:AT_kinetic:1239343491138588722>',
    'Anti-Tank Explosive': '<:AT_explosive:1239343415854891071>',
    'Explosive': '<:explosive:1239343451447758878>',
    'High Explosive': '<:high_explosive:1239343441025175583>',
    'Armour Piercing': '<:AP:1239343423807553547>',
    'Demolition': '<:demolition:1239343432367870035>',
    'Shrapnel': '<:shrapnel:1239343483286716417>',
    'Incendiary High Explosive': '<:incendiary:1239343406854049824>',
    'Tracks': '<:tracked:1239349968767291454>',
    'Fuel Tank': '<:fuel_leak:1239349986471313499>',
    'Turret': '<:turret:1239349978170921060>',
    'Steel Construction Materials': '<:scmat:1239353153694994533>',
    'Assembly Materials I': '<:asmat1:1239353117120659557>',
    'Assembly Materials II': '<:asmat2:1239353144484302953>',
    'Assembly Materials III': '<:asmat3:1239353124653760584>',
    'Assembly Materials IV': '<:asmat4:1239353135772995584>',
    'Assembly Materials V': '<:asmat5:1239353106404474951>',
    'Refined Materials': '<:rmat:1239353730172715048>',
    'Basic Materials': '<:bmat:1239353181474127943>',
    'Processed Construction Materials': '<:pcmat:1239353173488042005>',
    'LegendLargeShips': '<:large_ship:1239361716777914479>',
    'LegendFacilities': '<:facility:1239361717922828371>',
    'LegendMedical': '<:medical:1239361720288284693>',
    'LegendStructure': '<:intel:1239361723429949461>',
    'LegendArtillery': '<:arty:1239361721324539986>',
    'LegendDefense': '<:defense:1239361722700271727>',
    'LegendOutpost': '<:outpost:1239361719084515329>'
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
    'Acrithia': ['Camp Omicron', 'Heir Apparent', 'Legion Ranch', 'Nereid Keep', 'Patridia', 'Swordfort', 'The Brinehold', 'Thetus Ring'],
    'Allods Bight': ['Belaying Trace', 'Homesick', "Mercy's Wail", 'Rumhold', 'Scurvyshire', 'The Stone Plank', 'The Turncoat'],
    'Ash Fields': ['Ashtown', 'Camp Omega', 'Cometa', 'Electi', 'Sootflow', 'The Ashfort', 'The Calamity'],
    'Basin Sionnach': ['Basinhome', 'Cuttail Station', 'Lamplight', 'Sess', 'Stoic', 'The Den'],
    'Callahans Passage': ['Cragstown', 'Crumbling Post', 'Lochan Berth', 'Overlook Hill', 'Scáth Passing', 'Solas Gorge', 'The Crumbling Passage', 'The Latch', 'The Procession', 'White Chapel'],
    'Callums Cape': ["Callum's Keep", 'Camp Hollow', 'Holdout', 'Ire', 'Lookout', 'Naofa', 'Scouts Jest'],
    'Clahstra': ['Bewailing Fort', 'East Narthex', 'The Treasury', 'The Vault', 'Third Chapter', 'Transept', 'Watchful Nave', 'Weephome'],
    'Clanshead Valley': ['Fallen Crown', 'Fort Ealar', 'Fort Esterwild', 'Fort Windham', 'Sweetholt', 'The King', 'The Pike'],
    'Deadlands': ['Abandoned Ward', 'Brine Glen', "Callahan's Boot", "Callahan's Gate", "Iron's End", 'Liberation Point', "Sun's Hollow", 'The Pits', 'The Salt Farms', 'The Salt March', 'The Spine'],
    'Drowned Vale': ['Bootnap', 'Coaldrifter Stead', 'Eastmarch', 'Loggerhead', 'Singing Serpents', 'Splinter Pens', 'The Baths', 'The Saltcaps', 'The Wash', 'Vessel', "Wisp's Warning"],
    'Endless Shore': ['Brackish Point', 'Enduring Wake', 'Iron Junction', 'Saltbrook Channel', 'Sídhe Fall', 'The Old Jack Tar', 'The Overland', 'Tuatha Watchpost', 'Wellchurch', 'Woodbind'],
    'Farranac Coast': ['Huskhollow', "Macha's Keening", 'Mara', 'Pleading Wharf', 'Scarp of Ambrose', 'Scythe', 'Terra', 'The Bone Haft', 'The Jade Cove', 'Transient Valley', 'Victa'],
    'Fishermans Row': ['Arcadia', 'Black Well', 'Dankana Post', 'Eidolo', 'Fort Ember', "Hangman's Court", 'Oceanwatch', 'Peripti Landing', 'The Satyr Stone'],
    'Godcrofts': ['Argosa', 'Exile', 'Fleecewatch', 'Isawa', 'Lipsia', 'Protos', 'Saegio', 'The Axehead', 'Ursa Base'],
    'Great March': ['Camp Senti', 'Dendró Field', 'Leto', 'Lionsfort', "Myrmidon's Stay", 'Remnant Villa', 'Sitaria', 'The Swan', 'Violethome'],
    'Heartlands': ['Barronswall', 'Barrony Ranch', 'Deeplaw Post', 'Fort Providence', 'Greenfield Orchard', 'Oleander Homestead', 'Proexí', 'The Blemish', 'The Breach', 'The Plough'],
    'Howl County': ['Fort Red', 'Fort Rider', 'Great Warden Dam', 'Hungry Wolf', 'Little Lamb', 'Sickleshire', 'Slipgate Outpost', 'Teller Farm'],
    'Kalokai': ['Baccae Ridge', 'Camp Tau', 'Hallow', 'Lost Greensward', "Night's Regret", 'Sourtooth', 'Sweethearth'],
    'Kings Cage': ['Den of Knaves', 'Eastknife', 'Gibbet Fields', 'Scarlethold', 'Slipchain', 'Southblade', 'The Bailie', 'The Manacle'],
    'Linn Mercy': ['Fort Duncan', 'Hardline', 'Lathair', 'Outwich Ranch', 'Rotdust', 'The Crimson Gardens', 'The First Coin', 'The Last Grove', 'The Long Whine', 'The Prairie Bazaar', 'Ulster Falls'],
    'Loch Mor': ['Feirmor', 'Market Road', "Mercy's Wish", "Moon's Copse", 'The Roilfort', 'Tomb of the First', 'Westmarch'],
    'Marban Hollow': ['Checkpoint Bua', 'Lockheed', "Maiden's Veil", 'Mox', 'Oster Wall', 'Sanctum', 'The Spitrocks'],
    'Morgens Crossing': ['Allsight', "Bastard's Block", "Callum's Descent", 'Eversus', 'Lividus', 'Quietus'],
    'Nevish Line': ['Blackcoat Way', 'Blinding Stones', 'Grief Mother', 'Mistle Shrine', 'Princefal', 'The Scrying Belt', 'Tomb Father', 'Unruly'],
    'Oarbreaker': ['Fort Fogwood', 'Gold', 'Grisly Refuge', 'Integrum', 'Partisan Island', 'Posterus', 'Silver', 'The Conclave', 'The Dirk'],
    'Origin': ['Arise', 'Dormio', 'Finis', 'Initium', 'Teichotima', 'The Steel Road', 'World Star'],
    'Reaching Trail': ['Brodytown', 'Dwyerstown', 'Elksford', 'Fort Mac Conaill', 'Harpy', 'Ice Ranch', 'Limestone Holdfast', 'Mousetrap', 'Nightchurch', 'Reprieve', 'The Ark'],
    'Reavers Pass': ['Breakwater', 'Clay Coffer', 'Fort Rictus', 'Keelhaul', 'Scuttletown', 'The Bilge', 'Thimble Base'],
    'Red River': ['Camp Upsilon', 'Cannonsmoke', 'Climb', 'Fort Matchwood', 'Judicium', 'Minos', 'Penance', 'Victoria Hill'],
    'Sableport': ['Barronhome', 'Cinderwick', "Light's End", 'Talonsfort', 'The Pendant', "The Robin's Nest", 'The Whetstone'],
    'Shackled Chasm': ['Firstmarch', 'Gorgon Grove', 'Limewood Holdfast', 'Reflection', 'Savages', 'Silk Farms', "Simo's Run", 'The Bell Toll', 'The Grave of Erastos', 'The Vanguard'],
    'Speaking Woods': ['Fort Blather', 'Hush', 'Inari Base', 'Sotto Bank', 'Stem', 'The Filament', 'Tine', 'Wound'],
    'Stema Landing': ['Acies Overlook', 'Alchimio Estate', 'Base Ferveret', 'Base Sagitta', 'The Flair', 'The Spearhead', 'The Wane', 'Ustio', 'Verge Wing'],
    'Stlican Shelf': ['Briar', 'Cavilltown', 'Fort Hoarfrost', 'Port of Rime', 'The Old Mourn', 'The South Wind', 'Thornhold', 'Vulpine Watch'],
    'Stonecradle': ['Buckler Sound', 'Fading Lights', 'The Cord', 'The Dais', "The Heir's Knife", 'The Long Fast', 'The Reach', 'Trammel Pool', "World's End"],
    'Tempest Island': ['Blackwatch', 'Isle of Psyche', "Liar's Haven", 'Plana Fada', 'Reef', 'Surge Gate', 'The Gale', 'The Iris', 'The Rush'],
    'Terminus': ['Bloody Palm Fort', 'Cerberus Wake', 'Therizó', 'Thunderbolt', "Warlord's Stead", 'Winding Bolas'],
    'The Fingers': ["Captain's Dread", 'Fort Barley', "Headsman's Villa", 'Plankhouse', 'Second Man', 'Tethys Base', 'The Old Captain', 'The Tusk', 'Titancall'],
    'The Moors': ['Borderlane', "Gravekeeper's Holdfast", 'Headstone', "Luch's Workshop", 'MacConmara Barrows', "Morrighan's Grave", 'Ogmaran', 'Reaching River', 'The Cut', 'The Spade', 'The Wind Hills', 'Wiccwalk'],
    'Umbral Wildwood': ['Amethyst', "Atropos' Fate", "Clotho's Refuge", 'GoldenRoot Ranch', "Hermit's Rest", "Lachesis' Tally ", 'Sentry', 'Stray', 'The Foundry', 'Thunderfoot', 'Vagrant Bastion'],
    'Viper Pit': ['Blackthroat', 'Earl Crowley', 'Fleck Crossing', 'Fort Viper', 'Kirknell', 'Moltworth', "Serenity's Blight", 'The Friars'],
    'Weathered Expanse': ["Crow's Nest", 'Foxcatcher', 'Frostmarch', 'Huntsfort', 'Necropolis', 'Shattered Advance', 'Spirit Watch', 'The Weathering Halls', 'Wightwalk'],
    'Westgate': ['Holdfast', 'Kingstone', 'Longstone', "Lord's Mouth", 'Lost Partition', "Rancher's Fast", 'The Gallows', 'Westgate Keep', 'Wyattwick', "Zeus' Demise"]
}


REGIONS_STOCKPILES = {
    'Acrithia': [('Legion Ranch', FoxholeBuildings.STORAGE_DEPOT.value), ('Thetus Ring', FoxholeBuildings.STORAGE_DEPOT.value), ('Patridia', FoxholeBuildings.SEAPORT.value)],
    'Allods Bight': [('Scurvyshire', FoxholeBuildings.STORAGE_DEPOT.value), ("Mercy's Wail", FoxholeBuildings.SEAPORT.value)],
    'Ash Fields': [('Electi', FoxholeBuildings.STORAGE_DEPOT.value), ('Ash Town', FoxholeBuildings.SEAPORT.value)],
    'Basin Sionnach': [('Sess', FoxholeBuildings.STORAGE_DEPOT.value), ('The Den', FoxholeBuildings.STORAGE_DEPOT.value), ('Cutail Station', FoxholeBuildings.SEAPORT.value)],
    'Callahans Passage': [('Solas Gorge', FoxholeBuildings.STORAGE_DEPOT.value), ('Lochan Berth', FoxholeBuildings.SEAPORT.value)],
    'Callums Cape': [('Holdout', FoxholeBuildings.STORAGE_DEPOT.value), ("Callum's Keep", FoxholeBuildings.SEAPORT.value)],
    'Clahstra': [('East Narthex', FoxholeBuildings.STORAGE_DEPOT.value), ('Third Chapter', FoxholeBuildings.STORAGE_DEPOT.value), ('The Treasury', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Clanshead Valley': [('The Pike', FoxholeBuildings.STORAGE_DEPOT.value), ('The King', FoxholeBuildings.SEAPORT.value)],
    'Deadlands': [('Abandoned Ward', FoxholeBuildings.STORAGE_DEPOT.value), ('Brine Glen', FoxholeBuildings.STORAGE_DEPOT.value), ("Callahan's Gate", FoxholeBuildings.STORAGE_DEPOT.value), ('The Salt Farms', FoxholeBuildings.STORAGE_DEPOT.value), ('The Spine', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Drowned Vale': [('Loggerhead', FoxholeBuildings.STORAGE_DEPOT.value), ('The Baths', FoxholeBuildings.SEAPORT.value)],
    'Endless Shore': [('Brackish Point', FoxholeBuildings.STORAGE_DEPOT.value), ('Iron Junction', FoxholeBuildings.STORAGE_DEPOT.value), ('Tuatha Watchpost', FoxholeBuildings.STORAGE_DEPOT.value), ('Saltbrook Channel', FoxholeBuildings.SEAPORT.value)],
    'Farranac Coast': [('Mara', FoxholeBuildings.STORAGE_DEPOT.value), ('The Bone Haft', FoxholeBuildings.STORAGE_DEPOT.value), ('Victa', FoxholeBuildings.STORAGE_DEPOT.value), ('Jade Cove', FoxholeBuildings.SEAPORT.value)],
    'Fishermans Row': [('Arcadia', FoxholeBuildings.STORAGE_DEPOT.value), ('Black Well', FoxholeBuildings.STORAGE_DEPOT.value), ('Eidolo', FoxholeBuildings.SEAPORT.value)],
    'Godcrofts': [('Isawa', FoxholeBuildings.SEAPORT.value), ('The Axehead', FoxholeBuildings.SEAPORT.value)],
    'Great March': [('Sitaria', FoxholeBuildings.STORAGE_DEPOT.value), ('Violethome', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Heartlands': [('Greenfield Orchard', FoxholeBuildings.STORAGE_DEPOT.value), ('The Blemish', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Howl County': [('Hungry Wolf', FoxholeBuildings.STORAGE_DEPOT.value), ('Little Lamb', FoxholeBuildings.STORAGE_DEPOT.value), ('Great Warden Dam', FoxholeBuildings.SEAPORT.value)],
    'Kalokai': [('Hallow', FoxholeBuildings.STORAGE_DEPOT.value), ('Sweethearth', FoxholeBuildings.STORAGE_DEPOT.value), ('Baccae Ridge', FoxholeBuildings.SEAPORT.value)],
    'Kings Cage': [('Gibbet Fields', FoxholeBuildings.STORAGE_DEPOT.value), ('The Manacle', FoxholeBuildings.SEAPORT.value)],
    'Linn Mercy': [('The Prarie Bazaar', FoxholeBuildings.STORAGE_DEPOT.value), ('Ulster Falls', FoxholeBuildings.SEAPORT.value)],
    'Loch Mor': [("Mercy's Wish", FoxholeBuildings.STORAGE_DEPOT.value), ('Feirmor', FoxholeBuildings.SEAPORT.value)],
    'Marban Hollow': [('Lockheed', FoxholeBuildings.STORAGE_DEPOT.value), ("Maiden's Veil", FoxholeBuildings.SEAPORT.value)],
    'Morgens Crossing': [('Allsight', FoxholeBuildings.STORAGE_DEPOT.value), ('Lividus', FoxholeBuildings.STORAGE_DEPOT.value), ('Quietus', FoxholeBuildings.SEAPORT.value)],
    'Nevish Line': [('Blackcoat Way', FoxholeBuildings.STORAGE_DEPOT.value), ('Mistle Shrine', FoxholeBuildings.STORAGE_DEPOT.value), ('The Scrying Belt', FoxholeBuildings.SEAPORT.value)],
    'Oarbreaker Isles': [('Integrum', FoxholeBuildings.SEAPORT.value), ('The Conclave', FoxholeBuildings.SEAPORT.value)],
    'Origin': [('Finis', FoxholeBuildings.STORAGE_DEPOT.value), ('Teichotima', FoxholeBuildings.STORAGE_DEPOT.value), ('Initium', FoxholeBuildings.SEAPORT.value)],
    'Reaching Trail': [('Brodytown', FoxholeBuildings.STORAGE_DEPOT.value), ('Reprieve', FoxholeBuildings.STORAGE_DEPOT.value)],
    'Reavers Pass': [('Breakwater', FoxholeBuildings.STORAGE_DEPOT.value), ('Scuttletown', FoxholeBuildings.STORAGE_DEPOT.value), ('Keelhaul', FoxholeBuildings.SEAPORT.value)],
    'Red River': [('Judicium', FoxholeBuildings.STORAGE_DEPOT.value), ('Penance', FoxholeBuildings.STORAGE_DEPOT.value), ('Cannonsmoke', FoxholeBuildings.SEAPORT.value)],
    'Sableport': [('Barronhome', FoxholeBuildings.STORAGE_DEPOT.value), ('Cinderwick', FoxholeBuildings.STORAGE_DEPOT.value), ("Light's End", FoxholeBuildings.SEAPORT.value)],
    'Shackled Chasm': [('Savages', FoxholeBuildings.STORAGE_DEPOT.value), ('Silk Farms', FoxholeBuildings.SEAPORT.value)],
    'Speaking Woods': [('Sotto Bank', FoxholeBuildings.STORAGE_DEPOT.value), ('The Filament', FoxholeBuildings.STORAGE_DEPOT.value), ('Tine', FoxholeBuildings.SEAPORT.value)],
    'Stema Landing': [('Alchimio Estate', FoxholeBuildings.SEAPORT.value), ('The Spearhead', FoxholeBuildings.SEAPORT.value)],
    'Stlican Shelf': [('Cavilltown', FoxholeBuildings.STORAGE_DEPOT.value), ('Vulpine Watch', FoxholeBuildings.STORAGE_DEPOT.value), ('Port of Rime', FoxholeBuildings.SEAPORT.value)],
    'Stonecradle': [('Fading Lights', FoxholeBuildings.STORAGE_DEPOT.value), ('Buckler Sound', FoxholeBuildings.SEAPORT.value)],
    'Tempest Island': [("Liar's Heaven", FoxholeBuildings.STORAGE_DEPOT.value), ('The Rush', FoxholeBuildings.STORAGE_DEPOT.value), ('The Iris', FoxholeBuildings.SEAPORT.value)],
    'Terminus': [("Warlord's Stead", FoxholeBuildings.STORAGE_DEPOT.value), ('Therizó', FoxholeBuildings.SEAPORT.value)],
    'The Fingers': [("Headman's Villa", FoxholeBuildings.SEAPORT.value), ('The Old Captain', FoxholeBuildings.SEAPORT.value)],
    'The Moors': [("Morrighan's Grave", FoxholeBuildings.STORAGE_DEPOT.value), ('Ogmaran', FoxholeBuildings.SEAPORT.value)],
    'Umbral Wildwood': [("Hermit's Rest", FoxholeBuildings.STORAGE_DEPOT.value), ('Thunderfoot', FoxholeBuildings.SEAPORT.value)],
    'Viper Pit': [('Earl Crowley', FoxholeBuildings.STORAGE_DEPOT.value), ('Kirknell', FoxholeBuildings.SEAPORT.value)],
    'Weathered Expanse': [("Crow's Nest", FoxholeBuildings.STORAGE_DEPOT.value), ('Foxcatcher', FoxholeBuildings.STORAGE_DEPOT.value), ('The Weathering Halls', FoxholeBuildings.SEAPORT.value)],
    'Westgate': [('Kingstone', FoxholeBuildings.STORAGE_DEPOT.value), ('The Gallow', FoxholeBuildings.STORAGE_DEPOT.value), ('Longstone', FoxholeBuildings.SEAPORT.value)]
}


# TODO: end goal: if I search for 'rifle warden', it should returns an ordered list by search validity

ALL_WIKI_ENTRIES = [
    {
        'name': "Argenti r.II Rifle",
        'url': "https://foxhole.wiki.gg/wiki/Argenti_r.II_Rifle",
        'keywords': 'argenti rifle colonial',
    },
    {
        'name': "Blakerow 871",
        'url': "https://foxhole.wiki.gg/wiki/Blakerow_871keywords",
        'keywords': 'blakerow 871 rifle warden'
    },
    {
        'name': "Catena rt.IV Auto-Rifle",
        'url': "https://foxhole.wiki.gg/wiki/Catena_rt.IV_Auto-Rifle",
        'keywords': 'catena auto rifle colonial'
    },
    {
        'name': "Fuscina pi.I",
        'url': "https://foxhole.wiki.gg/wiki/Fuscina_pi.I",
        'keywords': 'fuscina fusina fucina rifle colonial'
    },
    {
        'name': "No.2 Loughcaster",
        'url': "https://foxhole.wiki.gg/wiki/No.2_Loughcaster",
        'keywords': 'loughcaster rifle warden'
    },
    {
        'name': "No.2B Hawthorne",
        'url': "https://foxhole.wiki.gg/wiki/No.2B_Hawthorne",
        'keywords': 'hawthorne smallcaster rifle warden'
    },
    {
        'name': "Sampo Auto-Rifle 77",
        'url': "https://foxhole.wiki.gg/wiki/Sampo_Auto-Rifle_77",
        'keywords': 'sampo auto rifle 77 warden'
    },
    {
        'name': "The Hangman 757",
        'url': "https://foxhole.wiki.gg/wiki/The_Hangman_757",
        'keywords': 'the hangman 757 heavy rifle warden'
    },
    {
        'name': "Volta r.I Repeater",
        'url': "https://foxhole.wiki.gg/wiki/Volta_r.I_Repeater",
        'keywords': 'volta repeater heavy rifle colonial'
    },
    {
        'name': "Clancy Cinder M3",
        'url': "https://foxhole.wiki.gg/wiki/Clancy_Cinder_M3",
        'keywords': 'clancy cinder m3 long rifle warden'
    },
    {
        'name': "KRR2-790 Omen",
        'url': "https://foxhole.wiki.gg/wiki/KRR2-790_Omen",
        'keywords': 'krr2 790 omen long rifle colonial'
    },
    {
        'name': "Clancy-Raca M4",
        'url': "https://foxhole.wiki.gg/wiki/Clancy-Raca_M4",
        'keywords': 'clancy raca sniper rifle warden'
    },
    {
        'name': "KRR3-792 Auger",
        'url': "https://foxhole.wiki.gg/wiki/KRR3-792_Auger",
        'keywords': 'krr3 792 auger sniper rifle colonial'
    },
    {
        'name': "“Lionclaw” mc.VIII",
        'url': "https://foxhole.wiki.gg/wiki/%E2%80%9CLionclaw%E2%80%9D_mc.VIII",
        'keywords': 'lionclaw submachine gun colonial'
    },
    {
        'name': "“The Pitch Gun” mc.V",
        'url': "https://foxhole.wiki.gg/wiki/%E2%80%9CThe_Pitch_Gun%E2%80%9D_mc.V",
        'keywords': 'pitch gun submachine gun colonial'
    },
    {
        'name': "Fiddler Submachine Gun Model 868",
        'url': "https://foxhole.wiki.gg/wiki/Fiddler_Submachine_Gun_Model_868",
        'keywords': 'fiddler submachine gun warden'
    },
    {
        'name': "No.1 “The Liar” Submachine Gun",
        'url': "https://foxhole.wiki.gg/wiki/No.1_%E2%80%9CThe_Liar%E2%80%9D_Submachine_Gun",
        'keywords': 'the liar submachine gun warden'
    },
    {
        'name': "“Dusk” ce.III",
        'url': "https://foxhole.wiki.gg/wiki/%E2%80%9CDusk%E2%80%9D_ce.III",
        'keywords': 'dusk assault rifle colonial'
    },
    {
        'name': "Aalto Storm Rifle 24",
        'url': "https://foxhole.wiki.gg/wiki/Aalto_Storm_Rifle_24",
        'keywords': 'aalto storm rifle assault rifle warden'
    },
    {
        'name': "Booker Storm Rifle Model 838",
        'url': "https://foxhole.wiki.gg/wiki/Booker_Storm_Rifle_Model_838",
        'keywords': 'booker storm rifle model 838 assault rifle warden'
    },
    {
        'name': "Brasa Shotgun",
        'url': "https://foxhole.wiki.gg/wiki/Shotgun",
        'keywords': 'brasa shotgun colonial warden'
    },
    {
        'name': "Ahti Model 2",
        'url': "https://foxhole.wiki.gg/wiki/Ahti_Model_2",
        'keywords': 'ahti ati model 2 pistol warden'
    },
    {
        'name': "Cascadier 873",
        'url': "https://foxhole.wiki.gg/wiki/Cascadier_873",
        'keywords': 'cascadier 873 pistol warden'
    },
    {
        'name': "Ferro 879",
        'url': "https://foxhole.wiki.gg/wiki/Ferro_879",
        'keywords': 'ferro 879 pistol colonial'
    },
    {
        'name': "Cometa T2-9",
        'url': "https://foxhole.wiki.gg/wiki/Revolver",
        'keywords': 'cometa t2 9 revolver colonial warden'
    },
    {
        'name': "Catara mo.II",
        'url': "https://foxhole.wiki.gg/wiki/Light_Machine_Gun",
        'keywords': 'catara mo ii light machine gun lmg colonial'
    },
    {
        'name': "KRN886-127 Gast Machine Gun",
        'url': "https://foxhole.wiki.gg/wiki/KRN886-127_Gast_Machine_Gun",
        'keywords': 'krn886 127 gast machine gun mg colonial'
    },
    {
        'name': "Malone MK.2",
        'url': "https://foxhole.wiki.gg/wiki/Malone_MK.2",
        'keywords': 'malone mk 2 machine gun mg warden'
    },
    {
        'name': "20 Neville Anti-Tank Rifle",
        'url': "https://foxhole.wiki.gg/wiki/Anti-Tank_Rifle",
        'keywords': '20 neville anti tank rifle atr warden'
    },
    {
        'name': "“Typhon” ra.XII",
        'url': "https://foxhole.wiki.gg/wiki/Mounted_Anti-Tank_Rifle",
        'keywords': 'typhon ra xii mounted anti tank rifle atr colonial'
    },
    {
        'name': "Lamentum mm.IV",
        'url': "https://foxhole.wiki.gg/wiki/Lamentum_mm.IV",
        'keywords': 'lamentum mm iv mounted machine gun mg colonial'
    },
    {
        'name': "Malone Ratcatcher MK.1",
        'url': "https://foxhole.wiki.gg/wiki/Malone_Ratcatcher_MK.1",
        'keywords': 'malone ratcatcher mk 1 mounted machine gun mg warden'
    },
    {
        'name': "Daucus isg.III",
        'url': "https://foxhole.wiki.gg/wiki/Mounted_Infantry_Support_Gun",
        'keywords': 'daucus isg iii mounted infantry support gun colonial'
    },
    {
        'name': "“Molten Wind” v.II Flame Torch",
        'url': "https://foxhole.wiki.gg/wiki/%E2%80%9CMolten_Wind%E2%80%9D_v.II_Flame_Torch",
        'keywords': 'molten wind v ii flame torch flamethrower flame thrower colonial'
    },
    {
        'name': "Willow's Bane Model 845",
        'url': "https://foxhole.wiki.gg/wiki/Willow%27s_Bane_Model_845",
        'keywords': 'willow s bane model 845 flamethrower flame thrower warden'
    },
    {
        'name': "A3 Harpa Fragmentation Grenade",
        'url': "https://foxhole.wiki.gg/wiki/A3_Harpa_Fragmentation_Grenade",
        'keywords': 'a3 harpa fragmentation grenade warden'
    },
    {
        'name': "Bomastone Grenade",
        'url': "https://foxhole.wiki.gg/wiki/Bomastone_Grenade",
        'keywords': 'bomastone grenade colonial'
    },
    {
        'name': "Mammon 91-b",
        'url': "https://foxhole.wiki.gg/wiki/Mammon_91-b",
        'keywords': 'mamon mammon 91 b he grenade colonial warden'
    },
    {
        'name': "Tremola Grenade GPb-1",
        'url': "https://foxhole.wiki.gg/wiki/Tremola_Grenade_GPb-1",
        'keywords': 'tremola grenade gpb 1 he colonial warden'
    },
    {
        'name': "Green Ash Grenade",
        'url': "https://foxhole.wiki.gg/wiki/Gas_Grenade",
        'keywords': 'green ash grenade gas colonial warden'
    },
    {
        'name': "Anti-Tank Sticky Bomb",
        'url': "https://foxhole.wiki.gg/wiki/Anti-Tank_Sticky_Bomb",
        'keywords': 'anti tank sticky bomb colonial warden'
    },
    {
        'name': "BF5 White Ash Flask Grenade",
        'url': "https://foxhole.wiki.gg/wiki/Anti-Tank_Grenade",
        'keywords': 'bf5 white ash flask anti tank grenade warden'
    },
    {
        'name': "PT-815 Smoke Grenade",
        'url': "https://foxhole.wiki.gg/wiki/Smoke_Grenade",
        'keywords': 'pt 815 smoke grenade colonial warden'
    },
    {
        'name': "Alligator Charge",
        'url': "https://foxhole.wiki.gg/wiki/Alligator_Charge",
        'keywords': 'alligator aligator explosive charge warden'
    },
    {
        'name': "Hydra's Whisper",
        'url': "https://foxhole.wiki.gg/wiki/Hydra%27s_Whisper",
        'keywords': 'hydra s whisper explosive charge colonial'
    },
    {
        'name': "Abisme AT-99",
        'url': "https://foxhole.wiki.gg/wiki/Abisme_AT-99",
        'keywords': 'abisme at 99 anti tank mine colonial warden'
    },
    {
        'name': "Havoc Charge",
        'url': "https://foxhole.wiki.gg/wiki/Havoc_Charge",
        'keywords': 'havoc explosive charge colonial warden'
    },
    {
        'name': "E680-S Rudder Lock",
        'url': "https://foxhole.wiki.gg/wiki/Sea_Mine",
        'keywords': 'e680 rudder lock sea mine colonial warden'
    },
    {
        'name': "KLG901-2 Lunaire F",
        'url': "https://foxhole.wiki.gg/wiki/KLG901-2_Lunaire_F",
        'keywords': 'klg901 2 lunaire f launcher colonial'
    },
    {
        'name': "The Ospreay",
        'url': "https://foxhole.wiki.gg/wiki/The_Ospreay",
        'keywords': 'the ospreay grenade launcher warden'
    },
    {
        'name': "Cutler Launcher 4",
        'url': "https://foxhole.wiki.gg/wiki/RPG_Launcher",
        'keywords': 'cutler rpg launcher 4 warden'
    },
    {
        'name': "Bane 45",
        'url': "https://foxhole.wiki.gg/wiki/Bane_45",
        'keywords': 'bane 45 at anti tank rpg launcher colonial'
    },
    {
        'name': "Bonesaw MK.3",
        'url': "https://foxhole.wiki.gg/wiki/Bonesaw_MK.3",
        'keywords': 'bonesaw mk 3 arc rpg launcher warden'
    },
    {
        'name': "Ignifist 30",
        'url': "https://foxhole.wiki.gg/wiki/Ignifist_30",
        'keywords': 'ignifist 30 at rpg launcher colonial'
    },
    {
        'name': "Venom c.II 35",
        'url': "https://foxhole.wiki.gg/wiki/Venom_c.II_35",
        'keywords': 'venom c ii 35 at rpg launcher colonial'
    },
    {
        'name': "Cremari Mortar",
        'url': "https://foxhole.wiki.gg/wiki/Mortar",
        'keywords': 'cremari mortar colonial warden'
    },
    {
        'name': "Cutler Foebreaker",
        'url': "https://foxhole.wiki.gg/wiki/Mounted_RPG_Launcher",
        'keywords': 'cutler foebreaker mounted rpg launcher warden'
    },
    {
        'name': "Mounted Bonesaw MK.3",
        'url': "https://foxhole.wiki.gg/wiki/Mounted_Anti-Tank_RPG",
        'keywords': 'mounted bonesaw mk 3 arc rpg launcher warden'
    },
    {
        'name': "Mounted Fissura gd.I",
        'url': "https://foxhole.wiki.gg/wiki/Mounted_Grenade_Launcher",
        'keywords': 'mounted fissura gd i grenade launcher colonial'
    },
    {
        'name': "Buckhorn CCQ-18 Bayonet",
        'url': "https://foxhole.wiki.gg/wiki/Bayonet",
        'keywords': 'buckhorn ccq 18 bayonet colonial warden'
    },
    {
        'name': "Fists",
        'url': "https://foxhole.wiki.gg/wiki/Fists",
        'keywords': 'fists colonial warden'
    },
    {
        'name': "9mm",
        'url': "https://foxhole.wiki.gg/wiki/9mm",
        'keywords': '9mm magazine'
    },
    {
        'name': "8mm",
        'url': "https://foxhole.wiki.gg/wiki/8mm",
        'keywords': '8mm magazine'
    },
    {
        'name': "7.92mm",
        'url': "https://foxhole.wiki.gg/wiki/7.92mm",
        'keywords': '7 92mm magazine'
    },
    {
        'name': "7.62mm",
        'url': "https://foxhole.wiki.gg/wiki/7.62mm",
        'keywords': '7 62mm magazine'
    },
    {
        'name': ".44",
        'url': "https://foxhole.wiki.gg/wiki/.44",
        'keywords': '44 magazine'
    },
    {
        'name': "Buckshot",
        'url': "https://foxhole.wiki.gg/wiki/Buckshot",
        'keywords': 'buckshot shotgun ammo'
    },
    {
        'name': "Flame Ammo",
        'url': "https://foxhole.wiki.gg/wiki/Flame_Ammo",
        'keywords': 'flame ammo'
    },
    {
        'name': "12.7mm",
        'url': "https://foxhole.wiki.gg/wiki/12.7mm",
        'keywords': '12 7mm magazine'
    },
    {
        'name': "20mm",
        'url': "https://foxhole.wiki.gg/wiki/20mm",
        'keywords': '20mm magazine'
    },
    {
        'name': "30mm",
        'url': "https://foxhole.wiki.gg/wiki/30mm",
        'keywords': '30mm shell'
    },
    {
        'name': "40mm",
        'url': "https://foxhole.wiki.gg/wiki/40mm",
        'keywords': '40mm shell'
    },
    {
        'name': "68mm",
        'url': "https://foxhole.wiki.gg/wiki/68mm",
        'keywords': '68mm shell'
    },
    {
        'name': "75mm",
        'url': "https://foxhole.wiki.gg/wiki/75mm",
        'keywords': '75mm shell'
    },
    {
        'name': "94.5mm",
        'url': "https://foxhole.wiki.gg/wiki/94.5mm",
        'keywords': '94 5mmm shell'
    },
    {
        'name': "Flare Mortar Shell",
        'url': "https://foxhole.wiki.gg/wiki/Flare_Mortar_Shell",
        'keywords': 'flare mortar shell'
    },
    {
        'name': "Shrapnel Mortar Shell",
        'url': "https://foxhole.wiki.gg/wiki/Shrapnel_Mortar_Shell",
        'keywords': 'shrapnel mortar shell'
    },
    {
        'name': "Mortar Shell",
        'url': "https://foxhole.wiki.gg/wiki/Mortar_Shell",
        'keywords': 'mortar shell'
    },
    {
        'name': "4C-Fire Rocket",
        'url': "https://foxhole.wiki.gg/wiki/4C-Fire_Rocket",
        'keywords': '4c fire rocket'
    },
    {
        'name': "3C-High Explosive Rocket",
        'url': "https://foxhole.wiki.gg/wiki/3C-High_Explosive_Rocket",
        'keywords': '3c high explosive fire rocket'
    },
    {
        'name': "120mm",
        'url': "https://foxhole.wiki.gg/wiki/120mm",
        'keywords': '120mm shell'
    },
    {
        'name': "150mm",
        'url': "https://foxhole.wiki.gg/wiki/150mm",
        'keywords': '150mm shell'
    },
    {
        'name': "300mm",
        'url': "https://foxhole.wiki.gg/wiki/300mm",
        'keywords': '300mm shell'
    },
    {
        'name': "RPG",
        'url': "https://foxhole.wiki.gg/wiki/RPG",
        'keywords': 'rpg shell'
    },
    {
        'name': "AP⧸RPG",
        'url': "https://foxhole.wiki.gg/wiki/AP%E2%A7%B8RPG",
        'keywords': 'ap rpg shell'
    },
    {
        'name': "ARC⧸RPG",
        'url': "https://foxhole.wiki.gg/wiki/ARC%E2%A7%B8RPG",
        'keywords': 'arc rpg shell'
    },
    {
        'name': "250mm",
        'url': "https://foxhole.wiki.gg/wiki/250mm",
        'keywords': '250mm shell'
    },
    {
        'name': "“Molten Wind” v.II Ammo",
        'url': "https://foxhole.wiki.gg/wiki/%E2%80%9CMolten_Wind%E2%80%9D_v.II_Ammo",
        'keywords': 'molen wind v ii flame ammo'
    },
    {
        'name': "Willow's Bane Ammo",
        'url': "https://foxhole.wiki.gg/wiki/Willow%27s_Bane_Ammo",
        'keywords': 'willow s bane flame ammo'
    },
    {
        'name': "Moray Torpedo",
        'url': "https://foxhole.wiki.gg/wiki/Torpedo",
        'keywords': 'moray torpedo'
    },
    {
        'name': "Model-7 “Evie”",
        'url': "https://foxhole.wiki.gg/wiki/Depth_Charge",
        'keywords': 'model 7 evie depth charge'
    },
    {
        'name': "T3 “Xiphos”",
        'url': "https://foxhole.wiki.gg/wiki/T3_%E2%80%9CXiphos%E2%80%9D",
        'keywords': 't3 xiphos armored car ac colonial'
    },
    {
        'name': "T5 “Percutio”",
        'url': "https://foxhole.wiki.gg/wiki/T5_%E2%80%9CPercutio%E2%80%9D",
        'keywords': 't5 percutio armored car atac colonial'
    },
    {
        'name': "T8 “Gemini”",
        'url': "https://foxhole.wiki.gg/wiki/T8_%E2%80%9CGemini%E2%80%9D",
        'keywords': 't8 gemini armored car ac colonial'
    },
    {
        'name': "O'Brien V.110",
        'url': "https://foxhole.wiki.gg/wiki/O%27Brien_V.110",
        'keywords': 'obrien v 110 armored car ac warden'
    },
    {
        'name': "O'Brien V.113 Gravekeeper",
        'url': "https://foxhole.wiki.gg/wiki/O%27Brien_V.113_Gravekeeper",
        'keywords': 'obrien v 113 gravekeeper amored car ac bonewagon bonecar warden'
    },
    {
        'name': "O'Brien V.121 Highlander",
        'url': "https://foxhole.wiki.gg/wiki/O%27Brien_V.121_Highlander",
        'keywords': 'obrien v 121 highlander amored car tac warden'
    },
    {
        'name': "O'Brien V.130 Wild Jack",
        'url': "https://foxhole.wiki.gg/wiki/O%27Brien_V.130_Wild_Jack",
        'keywords': 'obrien v 130 wildjack armored car flame ac warden'
    },
    {
        'name': "O'Brien V.190 Knave",
        'url': "https://foxhole.wiki.gg/wiki/O%27Brien_V.190_Knave",
        'keywords': 'obrien v 190 knave armored car gac glac warden'
    },
    {
        'name': "O'Brien V.101 Freeman",
        'url': "https://foxhole.wiki.gg/wiki/O%27Brien_V.101_Freeman",
        'keywords': 'obrien v 101 freeman armored car hac warden'
    },
    {
        'name': "T12 “Actaeon” Tankette",
        'url': "https://foxhole.wiki.gg/wiki/T12_%E2%80%9CActaeon%E2%80%9D_Tankette",
        'keywords': 't12 actaeon tankette colonial'
    },
    {
        'name': "T13 “Deioneus” Rocket Battery",
        'url': "https://foxhole.wiki.gg/wiki/T13_%E2%80%9CDeioneus%E2%80%9D_Rocket_Battery",
        'keywords': 't13 deioneus rocket battery tankette colonial'
    },
    {
        'name': "T14 “Vesta” Tankette",
        'url': "https://foxhole.wiki.gg/wiki/T14_%E2%80%9CVesta%E2%80%9D_Tankette",
        'keywords': 't14 vesta flame tankette colonial'
    },
    {
        'name': "T20 “Ixion” Tankette",
        'url': "https://foxhole.wiki.gg/wiki/T20_%E2%80%9CIxion%E2%80%9D_Tankette",
        'keywords': 't20 ixion 30mm tankette colonial'
    },
    {
        'name': "AB-8 “Acheron”",
        'url': "https://foxhole.wiki.gg/wiki/AB-8_%E2%80%9CAcheron%E2%80%9D",
        'keywords': 'ab8 acheron apc colonial'
    },
    {
        'name': "AB-11 “Doru”",
        'url': "https://foxhole.wiki.gg/wiki/AB-11_%E2%80%9CDoru%E2%80%9D",
        'keywords': 'ab11 doru apc 12 7mm colonial'
    },
    {
        'name': "Mulloy LPC",
        'url': "https://foxhole.wiki.gg/wiki/Mulloy_LPC",
        'keywords': 'mulloy lpc apc warden'
    },
    {
        'name': "HH-a “Javelin”",
        'url': "https://foxhole.wiki.gg/wiki/HH-a_%E2%80%9CJavelin%E2%80%9D",
        'keywords': 'hha javelin halftrack ht colonial'
    },
    {
        'name': "HH-b “Hoplite”",
        'url': "https://foxhole.wiki.gg/wiki/HH-b_%E2%80%9CHoplite%E2%80%9D",
        'keywords': 'hhb hoplite halftrack ht colonial'
    },
    {
        'name': "HH-d “Peltast”",
        'url': "https://foxhole.wiki.gg/wiki/HH-d_%E2%80%9CPeltast%E2%80%9D",
        'keywords': 'hhd peltast mortart halftrack mht colonial'
    },
    {
        'name': "Niska Mk. I Gun Motor Carriage",
        'url': "https://foxhole.wiki.gg/wiki/Niska_Mk._I_Gun_Motor_Carriage",
        'keywords': 'niska mk i gun motor carriage halftrack ht warden'
    },
    {
        'name': "Niska Mk. II Blinder",
        'url': "https://foxhole.wiki.gg/wiki/Niska_Mk._II_Blinder",
        'keywords': 'niska mk ii blinder 68mm halftrack atht warden'
    },
    {
        'name': "Niska Mk. III Scar Twin",
        'url': "https://foxhole.wiki.gg/wiki/Niska_Mk._III_Scar_Twin",
        'keywords': 'niska mk iii scar twin halftrack ht warden'
    },
    {
        'name': "Niska-Rycker Mk. IX Skycaller",
        'url': "https://foxhole.wiki.gg/wiki/Niska-Rycker_Mk._IX_Skycaller",
        'keywords': 'niska rycker mk  ix skycaller rocket halftrack ht warden'
    },
    {
        'name': "Swallowtail 988/127-2",
        'url': "https://foxhole.wiki.gg/wiki/Swallowtail_988/127-2",
        'keywords': 'swallotail 988 field machine gun fmg warden'
    },
    {
        'name': "G40 “Sagittarii”",
        'url': "https://foxhole.wiki.gg/wiki/G40_%E2%80%9CSagittarii%E2%80%9D",
        'keywords': 'g40 sagittarii field machine gun fmg colonial'
    },
    {
        'name': "Duncan's Coin 20mm",
        'url': "https://foxhole.wiki.gg/wiki/Duncan%27s_Coin_20mm",
        'keywords': 'duncans coin 20mm field anti tank fatr warden'
    },
    {
        'name': "GA6 “Cestus”",
        'url': "https://foxhole.wiki.gg/wiki/GA6_%E2%80%9CCestus%E2%80%9D",
        'keywords': 'ga6 cestus field anti tank fatr colonial'
    },
    {
        'name': "120-68 “Koronides” Field Gun",
        'url': "https://foxhole.wiki.gg/wiki/Field_Artillery",
        'keywords': '120 68 koronides field gun field artillery arty colonial'
    },
    {
        'name': "Balfour Wolfhound 40mm",
        'url': "https://foxhole.wiki.gg/wiki/Field_Cannon",
        'keywords': 'balfour wolfhound 40mm field cannon pushgun warden'
    },
    {
        'name': "Rycker 4/3-F Wasp Nest",
        'url': "https://foxhole.wiki.gg/wiki/Field_Launcher",
        'keywords': 'rycker 1 3 f wasp nest field rocket launcher warden'
    },
    {
        'name': "Collins Cannon 68mm",
        'url': "https://foxhole.wiki.gg/wiki/Collins_Cannon_68mm",
        'keywords': 'collins cnanon 68mm fat field anti tank warden'
    },
    {
        'name': "AA-2 Battering Ram",
        'url': "https://foxhole.wiki.gg/wiki/AA-2_Battering_Ram",
        'keywords': 'aa 2 battering ram fat field anti tank colonial'
    },
    {
        'name': "Balfour Falconer 250mm",
        'url': "https://foxhole.wiki.gg/wiki/Field_Mortar",
        'keywords': 'barlfour falconer fm baby ballista 250mm pushgun warden'
    },
    {
        'name': "Balfour Rampart 68mm",
        'url': "https://foxhole.wiki.gg/wiki/Heavy_Field_Cannon",
        'keywords': 'balfourt rampart 68mm hv68 hvfat pushgun warden'
    },
    {
        'name': "40-45 “Smelter” Heavy Field Gun",
        'url': "https://foxhole.wiki.gg/wiki/Heavy_Field_Gun",
        'keywords': '40 45 smelter heavy field gun hv40 pushgun colonial'
    },
    {
        'name': "Balfour Stockade 75mm",
        'url': "https://foxhole.wiki.gg/wiki/Balfour_Stockade_75mm",
        'keywords': 'balfour stockade 75mm large field gun pushgun warden'
    },
    {
        'name': "945g “Stygian Bolt”",
        'url': "https://foxhole.wiki.gg/wiki/945g_%E2%80%9CStygian_Bolt%E2%80%9D",
        'keywords': '945g stygian bolt large field gun pushgun colonial'
    },
    {
        'name': "King Spire Mk. I",
        'url': "https://foxhole.wiki.gg/wiki/King_Spire_Mk._I",
        'keywords': 'king spire mk i scout tank mgst warden'
    },
    {
        'name': "King Gallant Mk. II",
        'url': "https://foxhole.wiki.gg/wiki/King_Gallant_Mk._II",
        'keywords': 'king gallant mk ii 30mm scout tank warden'
    },
    {
        'name': "King Jester - Mk. I-1",
        'url': "https://foxhole.wiki.gg/wiki/King_Jester_-_Mk._I-1",
        'keywords': 'king jester mk i 1 rocket scout tank warden'
    },
    {
        'name': "H-5 “Hatchet”",
        'url': "https://foxhole.wiki.gg/wiki/H-5_%E2%80%9CHatchet%E2%80%9D",
        'keywords': 'h5 hatchet light tank lt colonial'
    },
    {
        'name': "H-10 “Pelekys”",
        'url': "https://foxhole.wiki.gg/wiki/H-10_%E2%80%9CPelekys%E2%80%9D",
        'keywords': 'h10 pelekys light tank destroyer ltd colonial'
    },
    {
        'name': "H-19 “Vulcan”",
        'url': "https://foxhole.wiki.gg/wiki/H-19_%E2%80%9CVulcan%E2%80%9D",
        'keywords': 'h19 vulcan flame light tank lt colonial'
    },
    {
        'name': "H-8 “Kranesca”",
        'url': "https://foxhole.wiki.gg/wiki/H-8_%E2%80%9CKranesca%E2%80%9D",
        'keywords': 'h8 kranesca kranny light tank lt colonial'
    },
    {
        'name': "Devitt Mk. III",
        'url': "https://foxhole.wiki.gg/wiki/Devitt_Mk._III",
        'keywords': 'devit mkiii light tank lt warden'
    },
    {
        'name': "Devitt Ironhide Mk. IV",
        'url': "https://foxhole.wiki.gg/wiki/Devitt_Ironhide_Mk._IV",
        'keywords': 'devit ironhide mkiv light tank lt warden'
    },
    {
        'name': "Devitt-Caine Mk. IV MMR",
        'url': "https://foxhole.wiki.gg/wiki/Devitt-Caine_Mk._IV_MMR",
        'keywords': 'devitt caine mkiv mmr mortar light tank mlt warden'
    },
    {
        'name': "85K-b “Falchion”",
        'url': "https://foxhole.wiki.gg/wiki/85K-b_%E2%80%9CFalchion%E2%80%9D",
        'keywords': '85kb falchion assault tank mpt colonial'
    },
    {
        'name': "85K-a “Spatha”",
        'url': "https://foxhole.wiki.gg/wiki/85K-a_%E2%80%9CSpatha%E2%80%9D",
        'keywords': '85ka spatha spatah spata spahta assault tank colonial'
    },
    {
        'name': "85V-g “Talos”",
        'url': "https://foxhole.wiki.gg/wiki/85V-g_%E2%80%9CTalos%E2%80%9D",
        'keywords': '85vg talos assault 75mm tank colonial'
    },
    {
        'name': "86K-a “Bardiche”",
        'url': "https://foxhole.wiki.gg/wiki/86K-a_%E2%80%9CBardiche%E2%80%9D",
        'keywords': '86ka bardiche assault tank colonial'
    },
    {
        'name': "86K-c “Ranseur”",
        'url': "https://foxhole.wiki.gg/wiki/86K-c_%E2%80%9CRanseur%E2%80%9D",
        'keywords': '86kc ranseur quadiche assault rpg tank colonial'
    },
    {
        'name': "Silverhand - Mk. IV",
        'url': "https://foxhole.wiki.gg/wiki/Silverhand_-_Mk._IV",
        'keywords': 'silverhand mkiv svh assault tank warden'
    },
    {
        'name': "Silverhand Chieftain - Mk. VI",
        'url': "https://foxhole.wiki.gg/wiki/Silverhand_Chieftain_-_Mk._VI",
        'keywords': 'silverhand chieftain mkvi assault tank warden'
    },
    {
        'name': "Silverhand Lordscar - Mk. X",
        'url': "https://foxhole.wiki.gg/wiki/Silverhand_Lordscar_-_Mk._X",
        'keywords': 'silverhand lordscar mkix std assault tank destroyer warden'
    },
    {
        'name': "Gallagher Outlaw Mk. II",
        'url': "https://foxhole.wiki.gg/wiki/Gallagher_Outlaw_Mk._II",
        'keywords': 'gallagher outlaw mkii cruiser tank warden'
    },
    {
        'name': "Gallagher Highwayman Mk. III",
        'url': "https://foxhole.wiki.gg/wiki/Gallagher_Highwayman_Mk._III",
        'keywords': 'gallagher highwayman mkiii hwm cruiser tank warden'
    },
    {
        'name': "Gallagher Thornfall Mk. VI",
        'url': "https://foxhole.wiki.gg/wiki/Gallagher_Thornfall_Mk._VI",
        'keywords': 'gallagher thornfall mkiv bonelaw cruiser tank warden'
    },
    {
        'name': "HC-2 “Scorpion”",
        'url': "https://foxhole.wiki.gg/wiki/Light_Infantry_Tank",
        'keywords': 'hc2 scorpion light infantry support tank ist colonial'
    },
    {
        'name': "HC-7 “Ballista”",
        'url': "https://foxhole.wiki.gg/wiki/Siege_Tank",
        'keywords': 'hc7 ballista siege tank colonial'
    },
    {
        'name': "Noble Widow MK. XIV",
        'url': "https://foxhole.wiki.gg/wiki/Noble_Widow_MK._XIV",
        'keywords': 'noble widow mkxiv heavy tank destroyer htd warden'
    },
    {
        'name': "Noble Firebrand Mk. XVII",
        'url': "https://foxhole.wiki.gg/wiki/Noble_Firebrand_Mk._XVII",
        'keywords': 'noblle firebrand mkvii heavy flame destroyer tank warden'
    },
    {
        'name': "Flood Juggernaut Mk. VII",
        'url': "https://foxhole.wiki.gg/wiki/Flood_Juggernaut_Mk._VII",
        'keywords': 'flood juggernaut mkvii flame battle tank bt warden'
    },
    {
        'name': "Flood Mk. I",
        'url': "https://foxhole.wiki.gg/wiki/Flood_Mk._I",
        'keywords': 'flood mki battle tank bt warden'
    },
    {
        'name': "Flood Mk. IX Stain",
        'url': "https://foxhole.wiki.gg/wiki/Flood_Mk._IX_Stain",
        'keywords': 'flood mkix stain battle tank spg warden'
    },
    {
        'name': "Lance-25 “Hasta”",
        'url': "https://foxhole.wiki.gg/wiki/Lance-25_%E2%80%9CHasta%E2%80%9D",
        'keywords': 'lance25 hasta battle tank destroyer btd colonial'
    },
    {
        'name': "Lance-36",
        'url': "https://foxhole.wiki.gg/wiki/Lance-36",
        'keywords': 'lance36 battle tank bt colonial'
    },
    {
        'name': "Lance-46 “Sarissa”",
        'url': "https://foxhole.wiki.gg/wiki/Lance-46_%E2%80%9CSarissa%E2%80%9D",
        'keywords': 'lance46 sarissa battle tank spg colonial'
    },
    {
        'name': "Cullen Predator Mk. III",
        'url': "https://foxhole.wiki.gg/wiki/Cullen_Predator_Mk._III",
        'keywords': 'cullen predator mkiii super tank warden'
    },
    {
        'name': "O-75b “Ares”",
        'url': "https://foxhole.wiki.gg/wiki/O-75b_%E2%80%9CAres%E2%80%9D",
        'keywords': '075b ares super tank colonial'
    },
    {
        'name': "Dunne Fuelrunner 2d",
        'url': "https://foxhole.wiki.gg/wiki/Dunne_Fuelrunner_2d",
        'keywords': 'dunnel fuelrunner 2d fuel tanker warden'
    },
    {
        'name': "RR-3 “Stolon” Tanker",
        'url': "https://foxhole.wiki.gg/wiki/RR-3_%E2%80%9CStolon%E2%80%9D_Tanker",
        'keywords': 'rr3 stolon fuel tanker colonial'
    },
    {
        'name': "R-1 Hauler",
        'url': "https://foxhole.wiki.gg/wiki/R-1_Hauler",
        'keywords': 'r1 hauler truck colonial'
    },
    {
        'name': "R-17 “Retiarius” Skirmisher",
        'url': "https://foxhole.wiki.gg/wiki/R-17_%E2%80%9CRetiarius%E2%80%9D_Skirmisher",
        'keywords': 'r17 retiarius skirmisher katyusha truck colonial'
    },
    {
        'name': "R-5b “Sisyphus” Hauler",
        'url': "https://foxhole.wiki.gg/wiki/R-5b_%E2%80%9CSisyphus%E2%80%9D_Hauler",
        'keywords': 'r5b sisyphus hauler truck colonial'
    },
    {
        'name': "R-9 “Speartip” Escort",
        'url': "https://foxhole.wiki.gg/wiki/R-9_%E2%80%9CSpeartip%E2%80%9D_Escort",
        'keywords': 'r9 speartip escort truck colonial'
    },
    {
        'name': "R-5 “Atlas” Hauler",
        'url': "https://foxhole.wiki.gg/wiki/R-5_%E2%80%9CAtlas%E2%80%9D_Hauler",
        'keywords': 'r5 atlas hauler truck colonial'
    },
    {
        'name': "Dunne Loadlugger 3c",
        'url': "https://foxhole.wiki.gg/wiki/Dunne_Loadlugger_3c",
        'keywords': 'dunne loadlugger 3c truck warden'
    },
    {
        'name': "Dunne Transport",
        'url': "https://foxhole.wiki.gg/wiki/Dunne_Transport",
        'keywords': 'dunne transport truck warden'
    },
    {
        'name': "Dunne Landrunner 12c",
        'url': "https://foxhole.wiki.gg/wiki/Dunne_Landrunner_12c",
        'keywords': 'dunne landrunner 12c truck warden'
    },
    {
        'name': "Dunne Leatherback 2a",
        'url': "https://foxhole.wiki.gg/wiki/Dunne_Leatherback_2a",
        'keywords': 'dunner leatherback 2a truck warden'
    },
    {
        'name': "BMS - Class 2 Mobile Auto-Crane",
        'url': "https://foxhole.wiki.gg/wiki/Crane",
        'keywords': 'bms class 2 mobile auto crane colonial warden'
    },
    {
        'name': "BMS - Universal Assembly Rig",
        'url': "https://foxhole.wiki.gg/wiki/Construction_Vehicle",
        'keywords': 'bms universal assembly rig construction vehicle cv colonial warden'
    },
    {
        'name': "BMS - Fabricator",
        'url': "https://foxhole.wiki.gg/wiki/Advanced_Construction_Vehicle",
        'keywords': 'bms fabricator advanced construction vehicle acv colonial warden'
    },
    {
        'name': "BMS - Packmule Flatbed",
        'url': "https://foxhole.wiki.gg/wiki/Flatbed_Truck",
        'keywords': 'bms packmule flatbed truck colonial warden'
    },
    {
        'name': "BMS - Scrap Hauler",
        'url': "https://foxhole.wiki.gg/wiki/Harvester",
        'keywords': 'bms scrap hauler harvester colonial warden'
    },
    {
        'name': "Rooster - Junkwagon",
        'url': "https://foxhole.wiki.gg/wiki/Rooster_-_Junkwagon",
        'keywords': 'rooster junkwagon trailer colonial warden'
    },
    {
        'name': "Rooster - Lamploader",
        'url': "https://foxhole.wiki.gg/wiki/Rooster_-_Lamploader",
        'keywords': 'rooster lamploader trailer colonial warden'
    },
    {
        'name': "Rooster - Tumblebox",
        'url': "https://foxhole.wiki.gg/wiki/Rooster_-_Tumblebox",
        'keywords': 'rooster tumblebox trailer colonial warden'
    },
    {
        'name': "Dunne Dousing Engine 3r",
        'url': "https://foxhole.wiki.gg/wiki/Dunne_Dousing_Engine_3r",
        'keywords': 'dunne dousing engine 3r firetruck engine warden'
    },
    {
        'name': "R-12b - “Salva” Flame Truck",
        'url': "https://foxhole.wiki.gg/wiki/R-12b_-_%E2%80%9CSalva%E2%80%9D_Flame_Truck",
        'keywords': 'r12b salva flame truck firetruck engine colonial'
    },
    {
        'name': "Dunne Caravaner 2f",
        'url': "https://foxhole.wiki.gg/wiki/Dunne_Caravaner_2f",
        'keywords': 'dunne caravaner 2f bus warden'
    },
    {
        'name': "R-15 - “Chariot”",
        'url': "https://foxhole.wiki.gg/wiki/R-15_-_%E2%80%9CChariot%E2%80%9D",
        'keywords': 'r15 chariot bus colonial'
    },
    {
        'name': "Dunne Responder 3e",
        'url': "https://foxhole.wiki.gg/wiki/Dunne_Responder_3e",
        'keywords': 'dunner responder 3e ambulance warden'
    },
    {
        'name': "R-12 - “Salus” Ambulance",
        'url': "https://foxhole.wiki.gg/wiki/R-12_-_%E2%80%9CSalus%E2%80%9D_Ambulance",
        'keywords': 'r12 salus ambulance colonial'
    },
    {
        'name': "Cnute Cliffwrest",
        'url': "https://foxhole.wiki.gg/wiki/Cnute_Cliffwrest",
        'keywords': 'cnute cliffwrest heavy duty truck warden'
    },
    {
        'name': "AU-A150 Taurine Rigger",
        'url': "https://foxhole.wiki.gg/wiki/AU-A150_Taurine_Rigger",
        'keywords': 'aua150 taurine rigger heavy duty truck colonial'
    },
    {
        'name': "Blumfield LK205",
        'url': "https://foxhole.wiki.gg/wiki/Bicycle",
        'keywords': 'blumfield lk205 bycyle colonial warden'
    },
    {
        'name': "03MM “Caster”",
        'url': "https://foxhole.wiki.gg/wiki/03MM_%E2%80%9CCaster%E2%80%9D",
        'keywords': '03mm caster motorcycle bike colonial'
    },
    {
        'name': "00MS “Stinger”",
        'url': "https://foxhole.wiki.gg/wiki/00MS_%E2%80%9CStinger%E2%80%9D",
        'keywords': '00ms stinger motorcycle mg bike colonial'
    },
    {
        'name': "Kivela Power Wheel 80-1",
        'url': "https://foxhole.wiki.gg/wiki/Kivela_Power_Wheel_80-1",
        'keywords': 'kivela power wheel 801 motorcycle bike warden'
    },
    {
        'name': "UV-05a “Argonaut”",
        'url': "https://foxhole.wiki.gg/wiki/UV-05a_%E2%80%9CArgonaut%E2%80%9D",
        'keywords': 'uv05a argonaut light utility vehicle luv colonial'
    },
    {
        'name': "UV-24 “Icarus”",
        'url': "https://foxhole.wiki.gg/wiki/UV-24_%E2%80%9CIcarus%E2%80%9D",
        'keywords': 'uv24 icarus rpg jeep light utility vehicle luv colonial'
    },
    {
        'name': "UV-5c “Odyssey”",
        'url': "https://foxhole.wiki.gg/wiki/UV-5c_%E2%80%9COdyssey%E2%80%9D",
        'keywords': 'uv5c odyssey light utility vehicle luv colonial'
    },
    {
        'name': "Drummond 100a",
        'url': "https://foxhole.wiki.gg/wiki/Drummond_100a",
        'keywords': 'drummond 100a light utility vehicle luv warden'
    },
    {
        'name': "Drummond Loscann 55c",
        'url': "https://foxhole.wiki.gg/wiki/Drummond_Loscann_55c",
        'keywords': 'drummond loscann 55c amphibious light utility vehicle aluv duck car warden'
    },
    {
        'name': "Drummond Spitfire 100d",
        'url': "https://foxhole.wiki.gg/wiki/Drummond_Spitfire_100d",
        'keywords': 'drummond spitfire 100d light utility vehicle luv warden'
    },
    {
        'name': "MacConmara Shorerunner",
        'url': "https://foxhole.wiki.gg/wiki/MacConmara_Shorerunner",
        'keywords': 'macconmara shorerunner landing ship warden'
    },
    {
        'name': "Interceptor PA-12",
        'url': "https://foxhole.wiki.gg/wiki/Interceptor_PA-12",
        'keywords': 'interceptor pa12 landing ship colonial'
    },
    {
        'name': "BMS - Aquatipper",
        'url': "https://foxhole.wiki.gg/wiki/Barge",
        'keywords': 'bms aquatipper barge colonial warden'
    },
    {
        'name': "BMS - Ironship",
        'url': "https://foxhole.wiki.gg/wiki/Freighter",
        'keywords': 'mbs ironship freighter colonial warden'
    },
    {
        'name': "74b-1 Ronan Gunship",
        'url': "https://foxhole.wiki.gg/wiki/74b-1_Ronan_Gunship",
        'keywords': '74b1 ronan gunship gunboat warden'
    },
    {
        'name': "Type C - “Charon”",
        'url': "https://foxhole.wiki.gg/wiki/Type_C_-_%E2%80%9CCharon%E2%80%9D",
        'keywords': 'type c charon gunboat colonial'
    },
    {
        'name': "Nakki",
        'url': "https://foxhole.wiki.gg/wiki/Nakki",
        'keywords': 'nakki submarine warden'
    },
    {
        'name': "AC-b “Trident”",
        'url': "https://foxhole.wiki.gg/wiki/AC-b_%E2%80%9CTrident%E2%80%9D",
        'keywords': 'acb trident submarine colonial'
    },
    {
        'name': "Blacksteele",
        'url': "https://foxhole.wiki.gg/wiki/Blacksteele",
        'keywords': 'blacksteele light frigate warden'
    },
    {
        'name': "Conqueror",
        'url': "https://foxhole.wiki.gg/wiki/Conqueror",
        'keywords': 'conqueror destroyer colonial'
    },
    {
        'name': "BMS - Longhook",
        'url': "https://foxhole.wiki.gg/wiki/Base_Ship",
        'keywords': 'bms longhook base ship colonial warden'
    },
    {
        'name': "BMS - Bluefin",
        'url': "https://foxhole.wiki.gg/wiki/Storage_Ship",
        'keywords': 'bms bluefin storage ship colonial warden'
    },
    {
        'name': "Callahan (Battleship)",
        'url': "https://foxhole.wiki.gg/wiki/Callahan_(Battleship)",
        'keywords': 'callahan battleship warden'
    },
    {
        'name': "Titan",
        'url': "https://foxhole.wiki.gg/wiki/Titan",
        'keywords': 'titan battleship colonial'
    },
    {
        'name': "BMS - Grouper",
        'url': "https://foxhole.wiki.gg/wiki/Motorboat",
        'keywords': 'bms grouper motorboat colonial warden'
    },
    {
        'name': "BMS Railtruck",
        'url': "https://foxhole.wiki.gg/wiki/Small_Container_Car",
        'keywords': 'bms railtruck small container car'
    },
    {
        'name': "BMS Linerunner",
        'url': "https://foxhole.wiki.gg/wiki/Small_Flatbed_Car",
        'keywords': 'bms linerunner small flatbed car'
    },
    {
        'name': "BMS Tinderbox",
        'url': "https://foxhole.wiki.gg/wiki/Small_Liquid_Container_Car",
        'keywords': 'bms tinderbox small liquid container car'
    },
    {
        'name': "BMS Mineseeker",
        'url': "https://foxhole.wiki.gg/wiki/Small_Train_Locomotive",
        'keywords': 'bms mineseeker small train locomotive'
    },
    {
        'name': "BMS Rockhold",
        'url': "https://foxhole.wiki.gg/wiki/Container_Car",
        'keywords': 'bms rockhold large train container car'
    },
    {
        'name': "BMS Roadhouse",
        'url': "https://foxhole.wiki.gg/wiki/Caboose",
        'keywords': 'bms roadhouse large train caboose'
    },
    {
        'name': "BMS Longrider",
        'url': "https://foxhole.wiki.gg/wiki/Flatbed_Car",
        'keywords': 'bms longrider large train flatbed car'
    },
    {
        'name': "BMS Holdout",
        'url': "https://foxhole.wiki.gg/wiki/Infantry_Car",
        'keywords': 'bms holdout large train infantry car'
    },
    {
        'name': "BMS Black Bolt",
        'url': "https://foxhole.wiki.gg/wiki/Locomotive",
        'keywords': 'bms black bolt large train locomotive'
    },
    {
        'name': "O'Brien Warsmith v.215",
        'url': "https://foxhole.wiki.gg/wiki/O%27Brien_Warsmith_v.215",
        'keywords': 'obrien warsmith v215 combat car warden'
    },
    {
        'name': "Aegis Steelbreaker K5a",
        'url': "https://foxhole.wiki.gg/wiki/Aegis_Steelbreaker_K5a",
        'keywords': 'aegis steelbreaker k5a combat car colonial'
    },
    {
        'name': "Tempest Cannon RA-2",
        'url': "https://foxhole.wiki.gg/wiki/Long-Range_Artillery_Car",
        'keywords': 'tempest cannon ra2 long range artillery car rsc colonial warden'
    },
    {
        'name': "BMS - Overseer Sky-Hauler",
        'url': "https://foxhole.wiki.gg/wiki/Large_Crane",
        'keywords': 'bms overseer skyhauler large crane'
    },
    {
        'name': "Heavy Infantry Carrier",
        'url': "https://foxhole.wiki.gg/wiki/Heavy_Infantry_Carrier",
        'keywords': 'heavy infantry carrier relic vehicle'
    },
    {
        'name': "Armoured Fighting Tractor",
        'url': "https://foxhole.wiki.gg/wiki/Armoured_Fighting_Tractor",
        'keywords': 'armoured amored fighting tractor relic vehicle'
    },
    {
        'name': "PL-1 “Phalanx”",
        'url': "https://foxhole.wiki.gg/wiki/Relic_Assault_Tank",
        'keywords': 'pl1 phalanx relic assault tank vehicle'
    },
    {
        'name': "Storm Tank",
        'url': "https://foxhole.wiki.gg/wiki/Storm_Tank",
        'keywords': 'storm tank relic vehicle'
    },
    {
        'name': "Staff Car",
        'url': "https://foxhole.wiki.gg/wiki/Staff_Car",
        'keywords': 'staff car relic vehicle'
    },
    {
        'name': "Repurposed Truck",
        'url': "https://foxhole.wiki.gg/wiki/Repurposed_Truck",
        'keywords': 'repurposed truck relic vehicle'
    },
    {
        'name': "Herne QMW 1a Scourge Hunter",
        'url': "https://foxhole.wiki.gg/wiki/Herne_QMW_1a_Scourge_Hunter",
        'keywords': 'herne qmw 1a scourge hunter mecha'
    },
    {
        'name': "Centurion MV-2",
        'url': "https://foxhole.wiki.gg/wiki/Centurion_MV-2",
        'keywords': 'centurion mv2 mecha'
    },
    {
        'name': "Border Base",
        'url': "https://foxhole.wiki.gg/wiki/Border_Base",
        'keywords': 'border base'
    },
    {
        'name': "Relic Base",
        'url': "https://foxhole.wiki.gg/wiki/Relic_Base",
        'keywords': 'relic base'
    },
    {
        'name': "Town Base (Tier 1)",
        'url': "https://foxhole.wiki.gg/wiki/Town_Base#Tier_1-0",
        'keywords': 'townbase'
    },
    {
        'name': "Town Base (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Town_Base#Tier_2-0",
        'keywords': 'townbase'
    },
    {
        'name': "Town Base (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Town_Base#Tier_3-0",
        'keywords': 'townbase'
    },
    {
        'name': "Bunker Base (Tier 1)",
        'url': "https://foxhole.wiki.gg/wiki/Bunker_Base#Tier_1-0",
        'keywords': 'bunker base'
    },
    {
        'name': "Bunker Base (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Bunker_Base#Tier_2-0",
        'keywords': 'bunker base'
    },
    {
        'name': "Bunker Base (Tier 3)",
        'url': " https://foxhole.wiki.gg/wiki/Bunker_Base#Tier_3-0",
        'keywords': 'bunker base'
    },
    {
        'name': "Encampment",
        'url': "https://foxhole.wiki.gg/wiki/Encampment",
        'keywords': 'encampment'
    },
    {
        'name': "Keep",
        'url': "https://foxhole.wiki.gg/wiki/Keep",
        'keywords': 'keep'
    },
    {
        'name': "Safe House (Tier 1)",
        'url': "https://foxhole.wiki.gg/wiki/Safe_House#Tier_1-0",
        'keywords': 'safe House'
    },
    {
        'name': "Safe House (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Safe_House#Tier_2-0",
        'keywords': 'safe House'
    },
    {
        'name': "Safe House (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Safe_House#Tier_3-0",
        'keywords': 'safe House'
    },
    {
        'name': "Seaport",
        'url': "https://foxhole.wiki.gg/wiki/Seaport",
        'keywords': 'seaport'
    },
    {
        'name': "Storage Depot",
        'url': "https://foxhole.wiki.gg/wiki/Storage_Depot",
        'keywords': 'storage depot'
    },
    {
        'name': "Liquid Container",
        'url': "https://foxhole.wiki.gg/wiki/Liquid_Container",
        'keywords': 'liquid container'
    },
    {
        'name': "Liquid Transfer Station",
        'url': "https://foxhole.wiki.gg/wiki/Liquid_Transfer_Station",
        'keywords': 'liquid transfer station'
    },
    {
        'name': "Material Pallet",
        'url': "https://foxhole.wiki.gg/wiki/Material_Pallet",
        'keywords': 'material pallet'
    },
    {
        'name': "Material Transfer Station",
        'url': "https://foxhole.wiki.gg/wiki/Material_Transfer_Station",
        'keywords': 'material transfer station'
    },
    {
        'name': "Resource Container",
        'url': "https://foxhole.wiki.gg/wiki/Resource_Container",
        'keywords': 'resource container'
    },
    {
        'name': "Resource Transfer Station",
        'url': "https://foxhole.wiki.gg/wiki/Resource_Transfer_Station",
        'keywords': 'resource transfer station'
    },
    {
        'name': "Shippable Crate",
        'url': "https://foxhole.wiki.gg/wiki/Shippable_Crate",
        'keywords': 'shippable crate'
    },
    {
        'name': "Shipping Container",
        'url': "https://foxhole.wiki.gg/wiki/Shipping_Container",
        'keywords': 'shipping container'
    },
    {
        'name': "Storage Box",
        'url': "https://foxhole.wiki.gg/wiki/Storage_Box",
        'keywords': 'storage boxe'
    },
    {
        'name': "Storage Room (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Storage_Room#Tier_2-0",
        'keywords': 'storage room bunker'
    },
    {
        'name': "Storage Room (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Storage_Room#Tier_3-0",
        'keywords': 'storage roombunker'
    },
    {
        'name': "Coastal Gun",
        'url': "https://foxhole.wiki.gg/wiki/Coastal_Gun",
        'keywords': 'coastal gun'
    },
    {
        'name': "Garrisoned House",
        'url': "https://foxhole.wiki.gg/wiki/Garrisoned_House",
        'keywords': 'garrisoned ghouse'
    },
    {
        'name': "Observation Tower",
        'url': "https://foxhole.wiki.gg/wiki/Observation_Tower",
        'keywords': 'observation tower'
    },
    {
        'name': "Anti-Tank Pillbox",
        'url': "https://foxhole.wiki.gg/wiki/Anti-Tank_Pillbox",
        'keywords': 'anti tank at pillboxe'
    },
    {
        'name': "AT Gun Garrison (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/AT_Gun_Garrison#Tier_2-0",
        'keywords': 'at gun garrison bunker'
    },
    {
        'name': "AT Gun Garrison (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/AT_Gun_Garrison#Tier_3-0",
        'keywords': 'at gun garrison bunker'
    },
    {
        'name': "Howitzer Garrison",
        'url': "https://foxhole.wiki.gg/wiki/Howitzer_Garrison",
        'keywords': 'howitzer garrison bunker'
    },
    {
        'name': "Machine Gun Garrison (Tier 1)",
        'url': "https://foxhole.wiki.gg/wiki/Machine_Gun_Garrison#Tier_1-0",
        'keywords': 'machine gun mg garrison bunker'
    },
    {
        'name': "Machine Gun Garrison (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Machine_Gun_Garrison#Tier_2-0",
        'keywords': 'machine gun mg garrison bunker'
    },
    {
        'name': "Machine Gun Garrison (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Machine_Gun_Garrison#Tier_3-0",
        'keywords': 'machine gun mg garrison bunker'
    },
    {
        'name': "Machine Gun Pillbox",
        'url': "https://foxhole.wiki.gg/wiki/Machine_Gun_Pillbox",
        'keywords': 'machine gun mg pillbox'
    },
    {
        'name': "Observation Bunker (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Observation_Bunker#Tier_2-0",
        'keywords': 'observation bunker'
    },
    {
        'name': "Observation Bunker (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Observation_Bunker#Tier_3-0",
        'keywords': 'observation bunker'
    },
    {
        'name': "Rifle Garrison (Tier 1)",
        'url': "https://foxhole.wiki.gg/wiki/Rifle_Garrison#Tier_1-0",
        'keywords': 'rifle garrison bunker'
    },
    {
        'name': "Rifle Garrison (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Rifle_Garrison#Tier_2-0",
        'keywords': 'rifle garrison bunker'
    },
    {
        'name': "Rifle Garrison (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Rifle_Garrison#Tier_3-0",
        'keywords': 'rifle garrison bunker'
    },
    {
        'name': "Rifle Pillbox",
        'url': "https://foxhole.wiki.gg/wiki/Rifle_Pillbox",
        'keywords': 'rifle pillbox'
    },
    {
        'name': "Watch Tower",
        'url': "https://foxhole.wiki.gg/wiki/Watch_Tower",
        'keywords': 'watch tower wt'
    },
    {
        'name': "Emplacement House",
        'url': "https://foxhole.wiki.gg/wiki/Emplacement_House",
        'keywords': 'emplacement mortar mhouse'
    },
    {
        'name': "50-500 “Thunderbolt” Cannon",
        'url': "https://foxhole.wiki.gg/wiki/50-500_%E2%80%9CThunderbolt%E2%80%9D_Cannon",
        'keywords': '50500 thunderbolt cannon artillery arty 150mm colonial'
    },
    {
        'name': "DAE 1b-2 “Serra”",
        'url': "https://foxhole.wiki.gg/wiki/DAE_1b-2_%E2%80%9CSerra%E2%80%9D",
        'keywords': 'dae 1b2 serra emplaced machine gun emg colonial'
    },
    {
        'name': "DAE 1o-3 “Polybolos”",
        'url': "https://foxhole.wiki.gg/wiki/DAE_1o-3_%E2%80%9CPolybolos%E2%80%9D",
        'keywords': 'dae 1o3 polybolos emplaced at gun beat colonial'
    },
    {
        'name': "DAE 2a-1 “Ruptura”",
        'url': "https://foxhole.wiki.gg/wiki/DAE_2a-1_%E2%80%9CRuptura%E2%80%9D",
        'keywords': 'dae 2a1 ruptura colonial'
    },
    {
        'name': "DAE 3b-2 “Hades' Net”",
        'url': "https://foxhole.wiki.gg/wiki/DAE_3b-2_%E2%80%9CHades%27_Net%E2%80%9D",
        'keywords': 'dae 3b2 hades net emplaced rocket artillery colonial'
    },
    {
        'name': "Huber Exalt 150mm",
        'url': "https://foxhole.wiki.gg/wiki/Huber_Exalt_150mm",
        'keywords': 'hubert exalt artillery arty 150mm warden'
    },
    {
        'name': "Huber Lariat 120mm",
        'url': "https://foxhole.wiki.gg/wiki/Light_Artillery",
        'keywords': 'huber lariat artillery arty warden'
    },
    {
        'name': "Huber Starbreaker 94.5mm",
        'url': "https://foxhole.wiki.gg/wiki/Huber_Starbreaker_94.5mm",
        'keywords': 'huber starbreaker 945mm warden'
    },
    {
        'name': "Intelligence Center",
        'url': "https://foxhole.wiki.gg/wiki/Intelligence_Center",
        'keywords': 'intelligence center ic'
    },
    {
        'name': "Leary Shellbore 68mm",
        'url': "https://foxhole.wiki.gg/wiki/Leary_Shellbore_68mm",
        'keywords': 'leary shellbore 68mm emplaced at gun eat warden'
    },
    {
        'name': "Leary Snare Trap 127",
        'url': "https://foxhole.wiki.gg/wiki/Leary_Snare_Trap_127",
        'keywords': 'leary snare trap 127 emplaced machine gun emg warden'
    },
    {
        'name': "Storm Cannon",
        'url': "https://foxhole.wiki.gg/wiki/Storm_Cannon",
        'keywords': 'storm cannon sc'
    },
    {
        'name': "Barbed Wire",
        'url': "https://foxhole.wiki.gg/wiki/Barbed_Wire_(Structure)",
        'keywords': 'barbed wire'
    },
    {
        'name': "Barbed Wire Fence",
        'url': "https://foxhole.wiki.gg/wiki/Barbed_Wire_Fence",
        'keywords': 'barbed wire fence'
    },
    {
        'name': "Bunker (Tier 1)",
        'url': "https://foxhole.wiki.gg/wiki/Bunker#Tier_1-0",
        'keywords': 'bunker'
    },
    {
        'name': "Bunker (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Bunker#Tier_2-0",
        'keywords': 'bunker'
    },
    {
        'name': "Bunker (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Bunker#Tier_3-0",
        'keywords': 'bunker'
    },
    {
        'name': "Bunker Corner (Tier 1)",
        'url': "https://foxhole.wiki.gg/wiki/Bunker_Corner#Tier_1-0",
        'keywords': 'bunker corner'
    },
    {
        'name': "Bunker Corner (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Bunker_Corner#Tier_2-0",
        'keywords': 'bunker corner'
    },
    {
        'name': "Bunker Corner (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Bunker_Corner#Tier_3-0",
        'keywords': 'bunker corner'
    },
    {
        'name': "Bunker Ramp (Tier 1)",
        'url': "https://foxhole.wiki.gg/wiki/Bunker_Ramp#Tier_1-0",
        'keywords': 'bunker ramp'
    },
    {
        'name': "Bunker Ramp (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Bunker_Ramp#Tier_2-0",
        'keywords': 'bunker ramp'
    },
    {
        'name': "Bunker Ramp (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Bunker_Ramp#Tier_3-0",
        'keywords': 'bunker ramp'
    },
    {
        'name': "Dragon's Teeth",
        'url': "https://foxhole.wiki.gg/wiki/Dragon%27s_Teeth",
        'keywords': 'dragons teeth'
    },
    {
        'name': "Foxhole",
        'url': "https://foxhole.wiki.gg/wiki/Dug_Foxhole",
        'keywords': 'dug foxhole'
    },
    {
        'name': "Gate (Tier 1)",
        'url': "https://foxhole.wiki.gg/wiki/Gate#Tier_1-0",
        'keywords': 'gate'
    },
    {
        'name': "Gate (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Gate#Tier_2-0",
        'keywords': 'gate'
    },
    {
        'name': "Gate (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Gate#Tier_3-0",
        'keywords': 'gate'
    },
    {
        'name': "Sandbag Cover",
        'url': "https://foxhole.wiki.gg/wiki/Sandbag_Cover#Sandbag_Cover_(Tier_1)-0",
        'keywords': 'sandbags cover'
    },
    {
        'name': "Sandbag Wall",
        'url': "https://foxhole.wiki.gg/wiki/Sandbag_Cover#Sandbag_Wall_(Tier_2)-0",
        'keywords': 'sandbags wall'
    },
    {
        'name': "Tank Trap",
        'url': "https://foxhole.wiki.gg/wiki/Tank_Trap",
        'keywords': 'tank trap'
    },
    {
        'name': "Trench (Tier 1)",
        'url': "https://foxhole.wiki.gg/wiki/Trench#Tier_1-0",
        'keywords': 'trench'
    },
    {
        'name': "Trench (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Trench#Tier_2-0",
        'keywords': 'trench'
    },
    {
        'name': "Trench (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Trench#Tier_3-0",
        'keywords': 'trench'
    },
    {
        'name': "Trench Connector (Tier 1)",
        'url': "https://foxhole.wiki.gg/wiki/Trench_Connector#Tier_1-0",
        'keywords': 'trench connector'
    },
    {
        'name': "Trench Connector (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Trench_Connector#Tier_2-0",
        'keywords': 'trench connector'
    },
    {
        'name': "Trench Connector (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Trench_Connector#Tier_3-0",
        'keywords': 'trench connector'
    },
    {
        'name': "Trench Emplacement (Tier 1)",
        'url': "https://foxhole.wiki.gg/wiki/Trench_Emplacement#Tier_1-0",
        'keywords': 'trench emplacement pit'
    },
    {
        'name': "Trench Emplacement (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Trench_Emplacement#Tier_2-0",
        'keywords': 'trench emplacement pit'
    },
    {
        'name': "Trench Emplacement (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Trench_Emplacement#Tier_3-0",
        'keywords': 'trench emplacement pit'
    },
    {
        'name': "Wall (Tier 1)",
        'url': "https://foxhole.wiki.gg/wiki/Wall#Tier_1-0",
        'keywords': 'wall'
    },
    {
        'name': "Wall (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Wall#Tier_2-0",
        'keywords': 'wall'
    },
    {
        'name': "Wall (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Wall#Tier_3-0",
        'keywords': 'wall'
    },
    {
        'name': "Construction Yard",
        'url': "https://foxhole.wiki.gg/wiki/Construction_Yard",
        'keywords': 'construction yard'
    },
    {
        'name': "Engineering Center",
        'url': "https://foxhole.wiki.gg/wiki/Engineering_Center",
        'keywords': 'engineering center'
    },
    {
        'name': "Factory",
        'url': "https://foxhole.wiki.gg/wiki/Factory",
        'keywords': 'factory'
    },
    {
        'name': "Garage",
        'url': "https://foxhole.wiki.gg/wiki/Garage",
        'keywords': 'garage'
    },
    {
        'name': "Hospital",
        'url': "https://foxhole.wiki.gg/wiki/Hospital",
        'keywords': 'hospital'
    },
    {
        'name': "Mass Production Factory",
        'url': "https://foxhole.wiki.gg/wiki/Mass_Production_Factory",
        'keywords': 'mass production factory'
    },
    {
        'name': "Refinery",
        'url': "https://foxhole.wiki.gg/wiki/Refinery",
        'keywords': 'refinery'
    },
    {
        'name': "Shipyard",
        'url': "https://foxhole.wiki.gg/wiki/Shipyard",
        'keywords': 'shipyard'
    },
    {
        'name': "A0E-9 Rocket Platform",
        'url': "https://foxhole.wiki.gg/wiki/A0E-9_Rocket_Platform",
        'keywords': 'a0e9 rocket nuke platform'
    },
    {
        'name': "Ammunition Factory",
        'url': "https://foxhole.wiki.gg/wiki/Ammunition_Factory",
        'keywords': 'ammunition factory'
    },
    {
        'name': "Coal Refinery",
        'url': "https://foxhole.wiki.gg/wiki/Coal_Refinery",
        'keywords': 'coal refinery'
    },
    {
        'name': "Concrete Mixer",
        'url': "https://foxhole.wiki.gg/wiki/Concrete_Mixer",
        'keywords': 'concrete mixer'
    },
    {
        'name': "Diesel Power Plant",
        'url': "https://foxhole.wiki.gg/wiki/Diesel_Power_Plant",
        'keywords': 'diesel power plant'
    },
    {
        'name': "Dry Dock",
        'url': "https://foxhole.wiki.gg/wiki/Dry_Dock",
        'keywords': 'dry dock'
    },
    {
        'name': "Field Hospital",
        'url': "https://foxhole.wiki.gg/wiki/Field_Hospital",
        'keywords': 'field hospital'
    },
    {
        'name': "Field Modification Center",
        'url': "https://foxhole.wiki.gg/wiki/Field_Modification_Center",
        'keywords': 'field modification center'
    },
    {
        'name': "Large Assembly Station",
        'url': "https://foxhole.wiki.gg/wiki/Large_Assembly_Station",
        'keywords': 'large assembly station upgrade pad'
    },
    {
        'name': "Materials Factory",
        'url': "https://foxhole.wiki.gg/wiki/Materials_Factory",
        'keywords': 'materials factory'
    },
    {
        'name': "Metalworks Factory",
        'url': "https://foxhole.wiki.gg/wiki/Metalworks_Factory",
        'keywords': 'metalworks factory'
    },
    {
        'name': "Oil Refinery",
        'url': "https://foxhole.wiki.gg/wiki/Oil_Refinery",
        'keywords': 'oil refinery'
    },
    {
        'name': "Power Station",
        'url': "https://foxhole.wiki.gg/wiki/Power_Station",
        'keywords': 'power station'
    },
    {
        'name': "Small Assembly Station",
        'url': "https://foxhole.wiki.gg/wiki/Small_Assembly_Station",
        'keywords': 'small assembly station upgrade pad'
    },
    {
        'name': "Oil Field",
        'url': "https://foxhole.wiki.gg/wiki/Oil_Field",
        'keywords': 'oil field'
    },
    {
        'name': "Coal Field",
        'url': "https://foxhole.wiki.gg/wiki/Coal_Field",
        'keywords': 'coal field'
    },
    {
        'name': "Salvage Field",
        'url': "https://foxhole.wiki.gg/wiki/Salvage_Field",
        'keywords': 'salvage scrap field'
    },
    {
        'name': "Sulfur Field",
        'url': "https://foxhole.wiki.gg/wiki/Sulfur_Field",
        'keywords': 'sulfur field'
    },
    {
        'name': "Component Field",
        'url': "https://foxhole.wiki.gg/wiki/Component_Field",
        'keywords': 'component field'
    },
    {
        'name': "Salvage Mine",
        'url': "https://foxhole.wiki.gg/wiki/Salvage_Mine",
        'keywords': 'salvage scrap mine'
    },
    {
        'name': "Sulfur Mine",
        'url': "https://foxhole.wiki.gg/wiki/Sulfur_Mine",
        'keywords': 'sulfur mine'
    },
    {
        'name': "Component Mine",
        'url': "https://foxhole.wiki.gg/wiki/Component_Mine",
        'keywords': 'component mine'
    },
    {
        'name': "Offshore Platform",
        'url': "https://foxhole.wiki.gg/wiki/Offshore_Platform",
        'keywords': 'offshore platform'
    },
    {
        'name': "Oil Well",
        'url': "https://foxhole.wiki.gg/wiki/Oil_Well",
        'keywords': 'oil well'
    },
    {
        'name': "Stationary Harvester (Coal)",
        'url': "https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Coal)",
        'keywords': 'stationary harvester'
    },
    {
        'name': "Stationary Harvester (Components)",
        'url': "https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Components)",
        'keywords': 'stationary harvester'
    },
    {
        'name': "Stationary Harvester (Scrap)",
        'url': "https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Scrap)",
        'keywords': 'stationary harvester'
    },
    {
        'name': "Stationary Harvester (Sulfur)",
        'url': "https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Sulfur)",
        'keywords': 'stationary harvester'
    },
    {
        'name': "Water Pump",
        'url': "https://foxhole.wiki.gg/wiki/Water_Pump",
        'keywords': 'water pump'
    },
    {
        'name': "Wooden Bridge",
        'url': "https://foxhole.wiki.gg/wiki/Bridge#Wooden_Bridge-0",
        'keywords': 'wooden bridge'
    },
    {
        'name': "Stone Bridge",
        'url': "https://foxhole.wiki.gg/wiki/Bridge#Stone_Bridge-0",
        'keywords': 'stone bridge'
    },
    {
        'name': "Two Tier Bridge",
        'url': "https://foxhole.wiki.gg/wiki/Bridge#Two_Tier_Bridge-1",
        'keywords': 'two tier bridge'
    },
    {
        'name': "Double Bridge",
        'url': "https://foxhole.wiki.gg/wiki/Bridge#Double_Bridge-1",
        'keywords': 'double bridge'
    },
    {
        'name': "Long Bridge",
        'url': "https://foxhole.wiki.gg/wiki/Bridge#Long_Bridge-1",
        'keywords': 'long bridge'
    },
    {
        'name': "Train Bridge",
        'url': "https://foxhole.wiki.gg/wiki/Bridge#Train_Bridge-1",
        'keywords': 'train bridge'
    },
    {
        'name': "Field Bridge",
        'url': "https://foxhole.wiki.gg/wiki/Field_Bridge",
        'keywords': 'field bridge'
    },
    {
        'name': "Dock",
        'url': "https://foxhole.wiki.gg/wiki/Dock",
        'keywords': 'docks'
    },
    {
        'name': "Stationary Crane",
        'url': "https://foxhole.wiki.gg/wiki/Stationary_Crane",
        'keywords': 'stationnary crane'
    },
    {
        'name': "A0E-9 Rocket",
        'url': "https://foxhole.wiki.gg/wiki/A0E-9_Rocket",
        'keywords': 'a0e9 rocket nuke'
    },
    {
        'name': "BMS Foreman Stacker",
        'url': "https://foxhole.wiki.gg/wiki/Facility_Crane",
        'keywords': 'bms foreman stacker facilty crane'
    },
    {
        'name': "Catwalk Bridge",
        'url': "https://foxhole.wiki.gg/wiki/Catwalk_Bridge",
        'keywords': 'catwalk bridge'
    },
    {
        'name': "Catwalk Platform",
        'url': "https://foxhole.wiki.gg/wiki/Catwalk_Platform",
        'keywords': 'catwalk platform'
    },
    {
        'name': "Catwalk Stairs",
        'url': "https://foxhole.wiki.gg/wiki/Catwalk_Stairs",
        'keywords': 'catwalk stairs'
    },
    {
        'name': "Crane Railway Track",
        'url': "https://foxhole.wiki.gg/wiki/Crane_Railway_Track",
        'keywords': 'crane railway track'
    },
    {
        'name': "Deployed Listening Kit",
        'url': "https://foxhole.wiki.gg/wiki/Listening_Kit",
        'keywords': 'deployed listening kit lk'
    },
    {
        'name': "Deployed Tripod",
        'url': "https://foxhole.wiki.gg/wiki/Tripod",
        'keywords': 'deployed tripod'
    },
    {
        'name': "Engine Room (Tier 2)",
        'url': "https://foxhole.wiki.gg/wiki/Engine_Room#Tier_2-0",
        'keywords': 'engine room bunker'
    },
    {
        'name': "Engine Room (Tier 3)",
        'url': "https://foxhole.wiki.gg/wiki/Engine_Room#Tier_3-0",
        'keywords': 'engine room bunker'
    },
    {
        'name': "Fire Pit",
        'url': "https://foxhole.wiki.gg/wiki/Fire_Pit",
        'keywords': 'fire pit campfire'
    },
    {
        'name': "Foundation (1x1)",
        'url': "https://foxhole.wiki.gg/wiki/Foundation#1x1-0",
        'keywords': 'foundation'
    },
    {
        'name': "Concrete Foundation (1x1)",
        'url': "https://foxhole.wiki.gg/wiki/Foundation#1x1_Concrete-0",
        'keywords': 'concrete foundation'
    },
    {
        'name': "Foundation Corner (1x1)",
        'url': "https://foxhole.wiki.gg/wiki/Foundation#Corner_1x1-0",
        'keywords': 'foundation'
    },
    {
        'name': "Concrete Foundation Corner (1x1)",
        'url': "https://foxhole.wiki.gg/wiki/Foundation#Corner_1x1_Concrete-0",
        'keywords': 'concrete foundation'
    },
    {
        'name': "Foundation (1x2)",
        'url': "https://foxhole.wiki.gg/wiki/Foundation#1x2-0",
        'keywords': 'foundation'
    },
    {
        'name': "Concrete Foundation (1x2)",
        'url': "https://foxhole.wiki.gg/wiki/Foundation#1x2_Concrete-0",
        'keywords': 'concrete foundation'
    },
    {
        'name': "Foundation (2x2)",
        'url': "https://foxhole.wiki.gg/wiki/Foundation#2x2-0",
        'keywords': 'foundation'
    },
    {
        'name': "Concrete Foundation (2x2)",
        'url': "https://foxhole.wiki.gg/wiki/Foundation#2x2_Concrete-0",
        'keywords': 'concrete foundation'
    },
    {
        'name': "Fuel Silo",
        'url': "https://foxhole.wiki.gg/wiki/Fuel_Silo",
        'keywords': 'fuel silo'
    },
    {
        'name': "Maintenance Tunnel",
        'url': "https://foxhole.wiki.gg/wiki/Maintenance_Tunnel",
        'keywords': 'maintenance tunnel'
    },
    {
        'name': "Navy Pier",
        'url': "https://foxhole.wiki.gg/wiki/Navy_Pier",
        'keywords': 'navy pier'
    },
    {
        'name': "Pipeline",
        'url': "https://foxhole.wiki.gg/wiki/Pipeline",
        'keywords': 'pipeline'
    },
    {
        'name': "Pipeline (Overhead)",
        'url': "https://foxhole.wiki.gg/wiki/Pipeline_(Overhead)",
        'keywords': 'pipeline'
    },
    {
        'name': "Pipeline (Underground)",
        'url': "https://foxhole.wiki.gg/wiki/Pipeline_(Underground)",
        'keywords': 'pipeline'
    },
    {
        'name': "Pipeline Valve",
        'url': "https://foxhole.wiki.gg/wiki/Pipeline_Valve",
        'keywords': 'pipeline'
    },
    {
        'name': "Power Pole",
        'url': "https://foxhole.wiki.gg/wiki/Power_Pole",
        'keywords': 'power pole'
    },
    {
        'name': "Power Switch",
        'url': "https://foxhole.wiki.gg/wiki/Power_Switch",
        'keywords': 'power switch'
    },
    {
        'name': "Provisional Road",
        'url': "https://foxhole.wiki.gg/wiki/Provisional_Road",
        'keywords': 'provisional road'
    },
    {
        'name': "Railway Track",
        'url': "https://foxhole.wiki.gg/wiki/Railway_Track#Standard-0",
        'keywords': 'large railway track'
    },
    {
        'name': "Railway Track (Biarc)",
        'url': "https://foxhole.wiki.gg/wiki/Railway_Track#Biarc-0",
        'keywords': 'large railway track'
    },
    {
        'name': "Railway Track (Foundation)",
        'url': "https://foxhole.wiki.gg/wiki/Railway_Track#Foundation-0",
        'keywords': 'large railway track'
    },
    {
        'name': "Small Gauge Railway Track",
        'url': "https://foxhole.wiki.gg/wiki/Small_Gauge_Railway_Track#Standard-0",
        'keywords': 'small gauge railway track'
    },
    {
        'name': "Small Gauge Railway Track (Biarc)",
        'url': "https://foxhole.wiki.gg/wiki/Small_Gauge_Railway_Track#Biarc-0",
        'keywords': 'small gauge railway track'
    },
    {
        'name': "Small Gauge Railway Track (Foundation)",
        'url': "https://foxhole.wiki.gg/wiki/Small_Gauge_Railway_Track#Foundation-0",
        'keywords': 'small gauge railway track'
    },
]
