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

ALL_WIKI_ENTRIES = [
    ## RIFLES
    ('Argenti r.II Rifle', 'https://foxhole.wiki.gg/wiki/Argenti_r.II_Rifle'),
    ('Blakerow 871', 'https://foxhole.wiki.gg/wiki/Blakerow_871', 'blakerow'),
    ('Catena rt.IV Auto-Rifle', 'https://foxhole.wiki.gg/wiki/Catena_rt.IV_Auto-Rifle'),
    ('Fuscina pi.I', 'https://foxhole.wiki.gg/wiki/Fuscina_pi.I'),
    ('No.2 Loughcaster', 'https://foxhole.wiki.gg/wiki/No.2_Loughcaster'),
    ('No.2B Hawthorne', 'https://foxhole.wiki.gg/wiki/No.2B_Hawthorne'),
    ('Sampo Auto-Rifle 77', 'https://foxhole.wiki.gg/wiki/Sampo_Auto-Rifle_77'),
    ## HEAVY RIFLES
    ('The Hangman 757', 'https://foxhole.wiki.gg/wiki/The_Hangman_757'),
    ('Volta r.I Repeater', 'https://foxhole.wiki.gg/wiki/Volta_r.I_Repeater'),
    ## LONG RIFLES
    ('Clancy Cinder M3', 'https://foxhole.wiki.gg/wiki/Clancy_Cinder_M3'),
    ('KRR2-790 Omen', 'https://foxhole.wiki.gg/wiki/KRR2-790_Omen'),
    ## SNIPER RIFLES
    ('Clancy-Raca M4', 'https://foxhole.wiki.gg/wiki/Clancy-Raca_M4'),
    ('KRR3-792 Auger', 'https://foxhole.wiki.gg/wiki/KRR3-792_Auger'),
    ## SUBMACHINE GUNS
    ('“Lionclaw” mc.VIII', 'https://foxhole.wiki.gg/wiki/%E2%80%9CLionclaw%E2%80%9D_mc.VIII'),
    ('“The Pitch Gun” mc.V', 'https://foxhole.wiki.gg/wiki/%E2%80%9CThe_Pitch_Gun%E2%80%9D_mc.V'),
    ('Fiddler Submachine Gun Model 868', 'https://foxhole.wiki.gg/wiki/Fiddler_Submachine_Gun_Model_868'),
    ('No.1 “The Liar” Submachine Gun', 'https://foxhole.wiki.gg/wiki/No.1_%E2%80%9CThe_Liar%E2%80%9D_Submachine_Gun'),
    ## ASSAULT RIFLES
    ('“Dusk” ce.III', 'https://foxhole.wiki.gg/wiki/%E2%80%9CDusk%E2%80%9D_ce.III'),
    ('Aalto Storm Rifle 24', 'https://foxhole.wiki.gg/wiki/Aalto_Storm_Rifle_24'),
    ('Booker Storm Rifle Model 838', 'https://foxhole.wiki.gg/wiki/Booker_Storm_Rifle_Model_838'),
    ## SHOTGUN
    ('Brasa Shotgun', 'https://foxhole.wiki.gg/wiki/Shotgun'),
    ## PISTOLS
    ('Ahti Model 2', 'https://foxhole.wiki.gg/wiki/Ahti_Model_2'),
    ('Cascadier 873', 'https://foxhole.wiki.gg/wiki/Cascadier_873'),
    ('Ferro 879', 'https://foxhole.wiki.gg/wiki/Ferro_879'),
    ## REVOLVER
    ('Cometa T2-9', 'https://foxhole.wiki.gg/wiki/Revolver'),
    ## LIGHT MACHINE GUN
    ('Catara mo.II', 'https://foxhole.wiki.gg/wiki/Light_Machine_Gun'),
    ## MACHINE GUN
    ('KRN886-127 Gast Machine Gun', 'https://foxhole.wiki.gg/wiki/KRN886-127_Gast_Machine_Gun'),
    ('Malone MK.2', 'https://foxhole.wiki.gg/wiki/Malone_MK.2'),
    ## ATR
    ('20 Neville Anti-Tank Rifle', 'https://foxhole.wiki.gg/wiki/Anti-Tank_Rifle'),
    ## MOUNTED ATR
    ('“Typhon” ra.XII', 'https://foxhole.wiki.gg/wiki/Mounted_Anti-Tank_Rifle'),
    ## MOUNTED MACHINE GUN
    ('Lamentum mm.IV', 'https://foxhole.wiki.gg/wiki/Lamentum_mm.IV'),
    ('Malone Ratcatcher MK.1', 'https://foxhole.wiki.gg/wiki/Malone_Ratcatcher_MK.1'),
    ## ISG
    ('Daucus isg.III', 'https://foxhole.wiki.gg/wiki/Mounted_Infantry_Support_Gun'),
    ## LANCE-FLAMMES
    ('“Molten Wind” v.II Flame Torch', 'https://foxhole.wiki.gg/wiki/%E2%80%9CMolten_Wind%E2%80%9D_v.II_Flame_Torch'),
    ("Willow's Bane Model 845", 'https://foxhole.wiki.gg/wiki/Willow%27s_Bane_Model_845'),
    ## GRENADES
    ('A3 Harpa Fragmentation Grenade', 'https://foxhole.wiki.gg/wiki/A3_Harpa_Fragmentation_Grenade'),
    ('Bomastone Grenade', 'https://foxhole.wiki.gg/wiki/Bomastone_Grenade'),
    ## HE GRENADES
    ('Mammon 91-b', 'https://foxhole.wiki.gg/wiki/Mammon_91-b'),
    ('Tremola Grenade GPb-1', 'https://foxhole.wiki.gg/wiki/Tremola_Grenade_GPb-1'),
    ## GAS GRENADE
    ('Green Ash Grenade', 'https://foxhole.wiki.gg/wiki/Gas_Grenade'),
    ## AT STICKY BOMB
    ('Anti-Tank Sticky Bomb', 'https://foxhole.wiki.gg/wiki/Anti-Tank_Sticky_Bomb'),
    ## AT GRENADES
    ('BF5 White Ash Flask Grenade', 'https://foxhole.wiki.gg/wiki/Anti-Tank_Grenade'),
    ## SMOKE GRENADES
    ('PT-815 Smoke Grenade', 'https://foxhole.wiki.gg/wiki/Smoke_Grenade'),
    ## EXPLOSIVE CHARGES
    ('Alligator Charge', 'https://foxhole.wiki.gg/wiki/Alligator_Charge'),
    ("Hydra's Whisper", 'https://foxhole.wiki.gg/wiki/Hydra%27s_Whisper'),
    ('Abisme AT-99', 'https://foxhole.wiki.gg/wiki/Abisme_AT-99'),
    ('Havoc Charge', 'https://foxhole.wiki.gg/wiki/Havoc_Charge'),
    ('E680-S Rudder Lock', 'https://foxhole.wiki.gg/wiki/Sea_Mine'),
    ## GRENADES LAUNCHERS
    ('KLG901-2 Lunaire F', 'https://foxhole.wiki.gg/wiki/KLG901-2_Lunaire_F'),
    ('The Ospreay', 'https://foxhole.wiki.gg/wiki/The_Ospreay'),
    ## RPG LAUNCHER
    ('Cutler Launcher 4', 'https://foxhole.wiki.gg/wiki/RPG_Launcher'),
    ## AT RPG
    ('Bane 45', 'https://foxhole.wiki.gg/wiki/Bane_45'),
    ('Bonesaw MK.3', 'https://foxhole.wiki.gg/wiki/Bonesaw_MK.3'),
    ('Ignifist 30', 'https://foxhole.wiki.gg/wiki/Ignifist_30'),
    ('Venom c.II 35', 'https://foxhole.wiki.gg/wiki/Venom_c.II_35'),
    ## MORTAR
    ('Cremari Mortar', 'https://foxhole.wiki.gg/wiki/Mortar'),
    ## MOUNTED RPG LAUNCHER
    ('Cutler Foebreaker', 'https://foxhole.wiki.gg/wiki/Mounted_RPG_Launcher'),
    # MOUNTED AT RPG
    ('Mounted Bonesaw MK.3', 'https://foxhole.wiki.gg/wiki/Mounted_Anti-Tank_RPG'),
    ## MOUNTED GRENADE LAUNCHER
    ('Mounted Fissura gd.I', 'https://foxhole.wiki.gg/wiki/Mounted_Grenade_Launcher'),
    ## MELEE
    ('Buckhorn CCQ-18 Bayonet', 'https://foxhole.wiki.gg/wiki/Bayonet'),
    ('Fists', 'https://foxhole.wiki.gg/wiki/Fists'),
    ## MAGAZINES
    ('9mm', 'https://foxhole.wiki.gg/wiki/9mm'),
    ('8mm', 'https://foxhole.wiki.gg/wiki/8mm'),
    ('7.92mm', 'https://foxhole.wiki.gg/wiki/7.92mm'),
    ('7.62mm', 'https://foxhole.wiki.gg/wiki/7.62mm'),
    ('.44', 'https://foxhole.wiki.gg/wiki/.44'),
    ('Buckshot', 'https://foxhole.wiki.gg/wiki/Buckshot'),
    ('Flame Ammo', 'https://foxhole.wiki.gg/wiki/Flame_Ammo'),
    ('12.7mm', 'https://foxhole.wiki.gg/wiki/12.7mm'),
    ('20mm', 'https://foxhole.wiki.gg/wiki/20mm'),
    ## SHELLS
    ('30mm', 'https://foxhole.wiki.gg/wiki/30mm'),
    ('40mm', 'https://foxhole.wiki.gg/wiki/40mm'),
    ('68mm', 'https://foxhole.wiki.gg/wiki/68mm'),
    ('75mm', 'https://foxhole.wiki.gg/wiki/75mm'),
    ('94.5mm', 'https://foxhole.wiki.gg/wiki/94.5mm'),
    ## ARTY AMMO
    ('Flare Mortar Shell', 'https://foxhole.wiki.gg/wiki/Flare_Mortar_Shell'),
    ('Shrapnel Mortar Shell', 'https://foxhole.wiki.gg/wiki/Shrapnel_Mortar_Shell'),
    ('Mortar Shell', 'https://foxhole.wiki.gg/wiki/Mortar_Shell'),
    ('4C-Fire Rocket', 'https://foxhole.wiki.gg/wiki/4C-Fire_Rocket'),
    ('3C-High Explosive Rocket', 'https://foxhole.wiki.gg/wiki/3C-High_Explosive_Rocket'),
    ('120mm', 'https://foxhole.wiki.gg/wiki/120mm'),
    ('150mm', 'https://foxhole.wiki.gg/wiki/150mm'),
    ('300mm', 'https://foxhole.wiki.gg/wiki/300mm'),
    ## PROPELLED EXPLOSIVES
    ('RPG', 'https://foxhole.wiki.gg/wiki/RPG'),
    ('AP⧸RPG', 'https://foxhole.wiki.gg/wiki/AP%E2%A7%B8RPG'),
    ('ARC⧸RPG', 'https://foxhole.wiki.gg/wiki/ARC%E2%A7%B8RPG'),
    ('250mm', 'https://foxhole.wiki.gg/wiki/250mm'),
    ## FLAMETHROWER AMMO
    ('“Molten Wind” v.II Ammo', 'https://foxhole.wiki.gg/wiki/%E2%80%9CMolten_Wind%E2%80%9D_v.II_Ammo'),
    ("Willow's Bane Ammo", 'https://foxhole.wiki.gg/wiki/Willow%27s_Bane_Ammo'),
    ## TORPEDO / DEPTH CHARGES
    ('Moray Torpedo', 'https://foxhole.wiki.gg/wiki/Torpedo'),
    ('Model-7 “Evie”', 'https://foxhole.wiki.gg/wiki/Depth_Charge'),
    ## ARMORED CARS
    ('T3 “Xiphos”', 'https://foxhole.wiki.gg/wiki/T3_%E2%80%9CXiphos%E2%80%9D'),
    ('T5 “Percutio”', 'https://foxhole.wiki.gg/wiki/T5_%E2%80%9CPercutio%E2%80%9D'),
    ('T8 “Gemini”', 'https://foxhole.wiki.gg/wiki/T8_%E2%80%9CGemini%E2%80%9D'),
    ("O'Brien V.110", 'https://foxhole.wiki.gg/wiki/O%27Brien_V.110'),
    ("O'Brien V.113 Gravekeeper", 'https://foxhole.wiki.gg/wiki/O%27Brien_V.113_Gravekeeper'),
    ("O'Brien V.121 Highlander", 'https://foxhole.wiki.gg/wiki/O%27Brien_V.121_Highlander'),
    ("O'Brien V.130 Wild Jack", 'https://foxhole.wiki.gg/wiki/O%27Brien_V.130_Wild_Jack'),
    ("O'Brien V.190 Knave", 'https://foxhole.wiki.gg/wiki/O%27Brien_V.190_Knave'),
    ("O'Brien V.101 Freeman", 'https://foxhole.wiki.gg/wiki/O%27Brien_V.101_Freeman'),
    ## TANKETTE
    ('T12 “Actaeon” Tankette', 'https://foxhole.wiki.gg/wiki/T12_%E2%80%9CActaeon%E2%80%9D_Tankette'),
    ('T13 “Deioneus” Rocket Battery', 'https://foxhole.wiki.gg/wiki/T13_%E2%80%9CDeioneus%E2%80%9D_Rocket_Battery'),
    ('T14 “Vesta” Tankette', 'https://foxhole.wiki.gg/wiki/T14_%E2%80%9CVesta%E2%80%9D_Tankette'),
    ('T20 “Ixion” Tankette', 'https://foxhole.wiki.gg/wiki/T20_%E2%80%9CIxion%E2%80%9D_Tankette'),
    ## APCs
    ('AB-8 “Acheron”', 'https://foxhole.wiki.gg/wiki/AB-8_%E2%80%9CAcheron%E2%80%9D'),
    ('AB-11 “Doru”', 'https://foxhole.wiki.gg/wiki/AB-11_%E2%80%9CDoru%E2%80%9D'),
    ('Mulloy LPC', 'https://foxhole.wiki.gg/wiki/Mulloy_LPC'),
    ## HALF-TRACKS
    ('HH-a “Javelin”', 'https://foxhole.wiki.gg/wiki/HH-a_%E2%80%9CJavelin%E2%80%9D'),
    ('HH-b “Hoplite”', 'https://foxhole.wiki.gg/wiki/HH-b_%E2%80%9CHoplite%E2%80%9D'),
    ('HH-d “Peltast”', 'https://foxhole.wiki.gg/wiki/HH-d_%E2%80%9CPeltast%E2%80%9D'),
    ('Niska Mk. I Gun Motor Carriage', 'https://foxhole.wiki.gg/wiki/Niska_Mk._I_Gun_Motor_Carriage'),
    ('Niska Mk. II Blinder', 'https://foxhole.wiki.gg/wiki/Niska_Mk._II_Blinder'),
    ('Niska Mk. III Scar Twin', 'https://foxhole.wiki.gg/wiki/Niska_Mk._III_Scar_Twin'),
    ('Niska-Rycker Mk. IX Skycaller', 'https://foxhole.wiki.gg/wiki/Niska-Rycker_Mk._IX_Skycaller'),
    ## FMG
    ('Swallowtail 988/127-2', 'https://foxhole.wiki.gg/wiki/Swallowtail_988/127-2'),
    ('G40 “Sagittarii”', 'https://foxhole.wiki.gg/wiki/G40_%E2%80%9CSagittarii%E2%80%9D'),
    ## FIELD ATR
    ("Duncan's Coin 20mm", 'https://foxhole.wiki.gg/wiki/Duncan%27s_Coin_20mm'),
    ('GA6 “Cestus”', 'https://foxhole.wiki.gg/wiki/GA6_%E2%80%9CCestus%E2%80%9D'),
    ## FIELD ARTILLERY
    ('120-68 “Koronides” Field Gun', 'https://foxhole.wiki.gg/wiki/Field_Artillery'),
    ## FIELD CANNON
    ('Balfour Wolfhound 40mm', 'https://foxhole.wiki.gg/wiki/Field_Cannon'),
    ## FIELD LAUNCHER
    ('Rycker 4/3-F Wasp Nest', 'https://foxhole.wiki.gg/wiki/Field_Launcher'),
    ## FIELD AT GUN
    ('Collins Cannon 68mm', 'https://foxhole.wiki.gg/wiki/Collins_Cannon_68mm'),
    ('AA-2 Battering Ram', 'https://foxhole.wiki.gg/wiki/AA-2_Battering_Ram'),
    ## FIELD MORTAR
    ('Balfour Falconer 250mm', 'https://foxhole.wiki.gg/wiki/Field_Mortar'),
    ## HEAVY FIELD CANON
    ('Balfour Rampart 68mm', 'https://foxhole.wiki.gg/wiki/Heavy_Field_Cannon'),
    ## HEAVY FIELD GUN
    ('40-45 “Smelter” Heavy Field Gun', 'https://foxhole.wiki.gg/wiki/Heavy_Field_Gun'),
    ## LARGE FIELD GUN
    ('Balfour Stockade 75mm', 'https://foxhole.wiki.gg/wiki/Balfour_Stockade_75mm'),
    ('945g “Stygian Bolt”', 'https://foxhole.wiki.gg/wiki/945g_%E2%80%9CStygian_Bolt%E2%80%9D'),
    ## SCOUT TANK
    ('King Spire Mk. I', 'https://foxhole.wiki.gg/wiki/King_Spire_Mk._I'),
    ('King Gallant Mk. II', 'https://foxhole.wiki.gg/wiki/King_Gallant_Mk._II'),
    ('King Jester - Mk. I-1', 'https://foxhole.wiki.gg/wiki/King_Jester_-_Mk._I-1'),
    ## LIGHT TANK
    ('H-5 “Hatchet”', 'https://foxhole.wiki.gg/wiki/H-5_%E2%80%9CHatchet%E2%80%9D'),
    ('H-10 “Pelekys”', 'https://foxhole.wiki.gg/wiki/H-10_%E2%80%9CPelekys%E2%80%9D'),
    ('H-19 “Vulcan”', 'https://foxhole.wiki.gg/wiki/H-19_%E2%80%9CVulcan%E2%80%9D'),
    ('H-8 “Kranesca”', 'https://foxhole.wiki.gg/wiki/H-8_%E2%80%9CKranesca%E2%80%9D'),
    ('Devitt Mk. III', 'https://foxhole.wiki.gg/wiki/Devitt_Mk._III'),
    ('Devitt Ironhide Mk. IV', 'https://foxhole.wiki.gg/wiki/Devitt_Ironhide_Mk._IV'),
    ('Devitt-Caine Mk. IV MMR', 'https://foxhole.wiki.gg/wiki/Devitt-Caine_Mk._IV_MMR'),
    ## ASSAULT TANK
    ('85K-b “Falchion”', 'https://foxhole.wiki.gg/wiki/85K-b_%E2%80%9CFalchion%E2%80%9D'),
    ('85K-a “Spatha”', 'https://foxhole.wiki.gg/wiki/85K-a_%E2%80%9CSpatha%E2%80%9D'),
    ('85V-g “Talos”', 'https://foxhole.wiki.gg/wiki/85V-g_%E2%80%9CTalos%E2%80%9D'),
    ('86K-a “Bardiche”', 'https://foxhole.wiki.gg/wiki/86K-a_%E2%80%9CBardiche%E2%80%9D'),
    ('86K-c “Ranseur”', 'https://foxhole.wiki.gg/wiki/86K-c_%E2%80%9CRanseur%E2%80%9D'),
    ('Silverhand - Mk. IV', 'https://foxhole.wiki.gg/wiki/Silverhand_-_Mk._IV'),
    ('Silverhand Chieftain - Mk. VI', 'https://foxhole.wiki.gg/wiki/Silverhand_Chieftain_-_Mk._VI'),
    ('Silverhand Lordscar - Mk. X', 'https://foxhole.wiki.gg/wiki/Silverhand_Lordscar_-_Mk._X'),
    ('Gallagher Outlaw Mk. II', 'https://foxhole.wiki.gg/wiki/Gallagher_Outlaw_Mk._II'),
    ('Gallagher Highwayman Mk. III', 'https://foxhole.wiki.gg/wiki/Gallagher_Highwayman_Mk._III'),
    ('Gallagher Thornfall Mk. VI', 'https://foxhole.wiki.gg/wiki/Gallagher_Thornfall_Mk._VI'),
    ## LIGHT INFANTRY TANK
    ('HC-2 “Scorpion”', 'https://foxhole.wiki.gg/wiki/Light_Infantry_Tank'),
    ## SIEGE TANK
    ('HC-7 “Ballista”', 'https://foxhole.wiki.gg/wiki/Siege_Tank'),
    ## DESTROYER TANK
    ('Noble Widow MK. XIV', 'https://foxhole.wiki.gg/wiki/Noble_Widow_MK._XIV'),
    ('Noble Firebrand Mk. XVII', 'https://foxhole.wiki.gg/wiki/Noble_Firebrand_Mk._XVII'),
    ## BATTLE TANK
    ('Flood Juggernaut Mk. VII', 'https://foxhole.wiki.gg/wiki/Flood_Juggernaut_Mk._VII'),
    ('Flood Mk. I', 'https://foxhole.wiki.gg/wiki/Flood_Mk._I'),
    ('Flood Mk. IX Stain', 'https://foxhole.wiki.gg/wiki/Flood_Mk._IX_Stain'),
    ('Lance-25 “Hasta”', 'https://foxhole.wiki.gg/wiki/Lance-25_%E2%80%9CHasta%E2%80%9D'),
    ('Lance-36', 'https://foxhole.wiki.gg/wiki/Lance-36'),
    ('Lance-46 “Sarissa”', 'https://foxhole.wiki.gg/wiki/Lance-46_%E2%80%9CSarissa%E2%80%9D'),
    ## SUPER TANK
    ('Cullen Predator Mk. III', 'https://foxhole.wiki.gg/wiki/Cullen_Predator_Mk._III'),
    ('O-75b “Ares”', 'https://foxhole.wiki.gg/wiki/O-75b_%E2%80%9CAres%E2%80%9D'),
    ## FUEL TANKER
    ('Dunne Fuelrunner 2d', 'https://foxhole.wiki.gg/wiki/Dunne_Fuelrunner_2d'),
    ('RR-3 “Stolon” Tanker', 'https://foxhole.wiki.gg/wiki/RR-3_%E2%80%9CStolon%E2%80%9D_Tanker'),
    ## TRUCK
    ('R-1 Hauler', 'https://foxhole.wiki.gg/wiki/R-1_Hauler'),
    ('R-17 “Retiarius” Skirmisher', 'https://foxhole.wiki.gg/wiki/R-17_%E2%80%9CRetiarius%E2%80%9D_Skirmisher'),
    ('R-5b “Sisyphus” Hauler', 'https://foxhole.wiki.gg/wiki/R-5b_%E2%80%9CSisyphus%E2%80%9D_Hauler'),
    ('R-9 “Speartip” Escort', 'https://foxhole.wiki.gg/wiki/R-9_%E2%80%9CSpeartip%E2%80%9D_Escort'),
    ('R-5 “Atlas” Hauler', 'https://foxhole.wiki.gg/wiki/R-5_%E2%80%9CAtlas%E2%80%9D_Hauler'),
    ('Dunne Loadlugger 3c', 'https://foxhole.wiki.gg/wiki/Dunne_Loadlugger_3c'),
    ('Dunne Transport', 'https://foxhole.wiki.gg/wiki/Dunne_Transport'),
    ('Dunne Landrunner 12c', 'https://foxhole.wiki.gg/wiki/Dunne_Landrunner_12c'),
    ('Dunne Leatherback 2a', 'https://foxhole.wiki.gg/wiki/Dunne_Leatherback_2a'),
    ## UTILITY VEHICLE
    ('BMS - Class 2 Mobile Auto-Crane', 'https://foxhole.wiki.gg/wiki/Crane'),
    ('BMS - Universal Assembly Rig', 'https://foxhole.wiki.gg/wiki/Construction_Vehicle'),
    ('BMS - Fabricator', 'https://foxhole.wiki.gg/wiki/Advanced_Construction_Vehicle'),
    ('BMS - Packmule Flatbed', 'https://foxhole.wiki.gg/wiki/Flatbed_Truck'),
    ('BMS - Scrap Hauler', 'https://foxhole.wiki.gg/wiki/Harvester'),
    ## TRAILER
    ('Rooster - Junkwagon', 'https://foxhole.wiki.gg/wiki/Rooster_-_Junkwagon'),
    ('Rooster - Lamploader', 'https://foxhole.wiki.gg/wiki/Rooster_-_Lamploader'),
    ('Rooster - Tumblebox', 'https://foxhole.wiki.gg/wiki/Rooster_-_Tumblebox'),
    ## FIRE ENGINE
    ('Dunne Dousing Engine 3r', 'https://foxhole.wiki.gg/wiki/Dunne_Dousing_Engine_3r'),
    ('R-12b - “Salva” Flame Truck', 'https://foxhole.wiki.gg/wiki/R-12b_-_%E2%80%9CSalva%E2%80%9D_Flame_Truck'),
    ## BUS
    ('Dunne Caravaner 2f', 'https://foxhole.wiki.gg/wiki/Dunne_Caravaner_2f'),
    ('R-15 - “Chariot”', 'https://foxhole.wiki.gg/wiki/R-15_-_%E2%80%9CChariot%E2%80%9D'),
    ## AMBULANCE
    ('Dunne Responder 3e', 'https://foxhole.wiki.gg/wiki/Dunne_Responder_3e'),
    ('R-12 - “Salus” Ambulance', 'https://foxhole.wiki.gg/wiki/R-12_-_%E2%80%9CSalus%E2%80%9D_Ambulance'),
    ## HEAVY-DUTY TRUCK
    ('Cnute Cliffwrest', 'https://foxhole.wiki.gg/wiki/Cnute_Cliffwrest'),
    ('AU-A150 Taurine Rigger', 'https://foxhole.wiki.gg/wiki/AU-A150_Taurine_Rigger'),
    ## BYCYCLE
    ('Blumfield LK205', 'https://foxhole.wiki.gg/wiki/Bicycle'),
    ## MOTORCYCLE
    ('03MM “Caster”', 'https://foxhole.wiki.gg/wiki/03MM_%E2%80%9CCaster%E2%80%9D'),
    ('00MS “Stinger”', 'https://foxhole.wiki.gg/wiki/00MS_%E2%80%9CStinger%E2%80%9D'),
    ('Kivela Power Wheel 80-1', 'https://foxhole.wiki.gg/wiki/Kivela_Power_Wheel_80-1'),
    ## LIGHT UTILITY VEHICLE
    ('UV-05a “Argonaut”', 'https://foxhole.wiki.gg/wiki/UV-05a_%E2%80%9CArgonaut%E2%80%9D'),
    ('UV-24 “Icarus”', 'https://foxhole.wiki.gg/wiki/UV-24_%E2%80%9CIcarus%E2%80%9D'),
    ('UV-5c “Odyssey”', 'https://foxhole.wiki.gg/wiki/UV-5c_%E2%80%9COdyssey%E2%80%9D'),
    ('Drummond 100a', 'https://foxhole.wiki.gg/wiki/Drummond_100a'),
    ('Drummond Loscann 55c', 'https://foxhole.wiki.gg/wiki/Drummond_Loscann_55c'),
    ('Drummond Spitfire 100d', 'https://foxhole.wiki.gg/wiki/Drummond_Spitfire_100d'),
    ## LANDING SHIP
    ('MacConmara Shorerunner', 'https://foxhole.wiki.gg/wiki/MacConmara_Shorerunner'),
    ('Interceptor PA-12', 'https://foxhole.wiki.gg/wiki/Interceptor_PA-12'),
    ## BARGE
    ('BMS - Aquatipper', 'https://foxhole.wiki.gg/wiki/Barge'),
    ## FREIGHTER
    ('BMS - Ironship', 'https://foxhole.wiki.gg/wiki/Freighter'),
    ## GUNBOAT
    ('74b-1 Ronan Gunship', 'https://foxhole.wiki.gg/wiki/74b-1_Ronan_Gunship'),
    ('Type C - “Charon”', 'https://foxhole.wiki.gg/wiki/Type_C_-_%E2%80%9CCharon%E2%80%9D'),
    ## SUBMARINE
    ('Nakki', 'https://foxhole.wiki.gg/wiki/Nakki'),
    ('AC-b “Trident”', 'https://foxhole.wiki.gg/wiki/AC-b_%E2%80%9CTrident%E2%80%9D'),
    ## LIGHT FRIGATE
    ('Blacksteele', 'https://foxhole.wiki.gg/wiki/Blacksteele'),
    ## DESTROYER
    ('Conqueror', 'https://foxhole.wiki.gg/wiki/Conqueror'),
    ## BASE SHIP
    ('BMS - Longhook', 'https://foxhole.wiki.gg/wiki/Base_Ship'),
    ## STORAGE SHIP
    ('BMS - Bluefin', 'https://foxhole.wiki.gg/wiki/Storage_Ship'),
    ## BATTLESHIP
    ('Callahan (Battleship)', 'https://foxhole.wiki.gg/wiki/Callahan_(Battleship)'),
    ('Titan', 'https://foxhole.wiki.gg/wiki/Titan'),
    ## MOTORBOAT
    ('BMS - Grouper', 'https://foxhole.wiki.gg/wiki/Motorboat'),
    ## SMALL TRAIN
    ('BMS Railtruck', 'https://foxhole.wiki.gg/wiki/Small_Container_Car'),
    ('BMS Linerunner', 'https://foxhole.wiki.gg/wiki/Small_Flatbed_Car'),
    ('BMS Tinderbox', 'https://foxhole.wiki.gg/wiki/Small_Liquid_Container_Car'),
    ('BMS Mineseeker', 'https://foxhole.wiki.gg/wiki/Small_Train_Locomotive'),
    ## LARGE TRAIN
    ('BMS Rockhold', 'https://foxhole.wiki.gg/wiki/Container_Car'),
    ('BMS Roadhouse', 'https://foxhole.wiki.gg/wiki/Caboose'),
    ('BMS Longrider', 'https://foxhole.wiki.gg/wiki/Flatbed_Car'),
    ('BMS Holdout', 'https://foxhole.wiki.gg/wiki/Infantry_Car'),
    ('BMS Black Bolt', 'https://foxhole.wiki.gg/wiki/Locomotive'),
    ("O'Brien Warsmith v.215", 'https://foxhole.wiki.gg/wiki/O%27Brien_Warsmith_v.215'),
    ('Aegis Steelbreaker K5a', 'https://foxhole.wiki.gg/wiki/Aegis_Steelbreaker_K5a'),
    ('Tempest Cannon RA-2', 'https://foxhole.wiki.gg/wiki/Long-Range_Artillery_Car'),
    ## LARGE CRANE
    ('BMS - Overseer Sky-Hauler', 'https://foxhole.wiki.gg/wiki/Large_Crane'),
    ## RELIC VEHICLE
    ('Heavy Infantry Carrier', 'https://foxhole.wiki.gg/wiki/Heavy_Infantry_Carrier'),
    ('Armoured Fighting Tractor', 'https://foxhole.wiki.gg/wiki/Armoured_Fighting_Tractor'),
    ('PL-1 “Phalanx”', 'https://foxhole.wiki.gg/wiki/Relic_Assault_Tank'),
    ('Storm Tank', 'https://foxhole.wiki.gg/wiki/Storm_Tank'),
    ('Staff Car', 'https://foxhole.wiki.gg/wiki/Staff_Car'),
    ('Repurposed Truck', 'https://foxhole.wiki.gg/wiki/Repurposed_Truck'),
    ## MECH VEHICLE
    ('Herne QMW 1a Scourge Hunter', 'https://foxhole.wiki.gg/wiki/Herne_QMW_1a_Scourge_Hunter'),
    ('Centurion MV-2', 'https://foxhole.wiki.gg/wiki/Centurion_MV-2')
]
