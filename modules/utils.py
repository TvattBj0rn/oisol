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
    ('Model-7 “Evie”', 'https://foxhole.wiki.gg/wiki/Depth_Charge')
]
