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


# TODO: end goal: if I search for 'rifle warden', it should returns an ordered list by search validity

ALL_WIKI_ENTRIES = [
    ## RIFLES
    {'name': "Argenti r.II Rifle", 'url': 'https://foxhole.wiki.gg/wiki/Argenti_r.II_Rifle'},
    {'name': "Blakerow 871", 'url': 'https://foxhole.wiki.gg/wiki/Blakerow_871'},
    {'name': "Catena rt.IV Auto-Rifle", 'url': 'https://foxhole.wiki.gg/wiki/Catena_rt.IV_Auto-Rifle'},
    {'name': "Fuscina pi.I", 'url': 'https://foxhole.wiki.gg/wiki/Fuscina_pi.I'},
    {'name': "No.2 Loughcaster", 'url': 'https://foxhole.wiki.gg/wiki/No.2_Loughcaster'},
    {'name': "No.2B Hawthorne", 'url': 'https://foxhole.wiki.gg/wiki/No.2B_Hawthorne'},
    {'name': "Sampo Auto-Rifle 77", 'url': 'https://foxhole.wiki.gg/wiki/Sampo_Auto-Rifle_77'},
    ## HEAVY RIFLES
    {'name': "The Hangman 757", 'url': 'https://foxhole.wiki.gg/wiki/The_Hangman_757'},
    {'name': "Volta r.I Repeater", 'url': 'https://foxhole.wiki.gg/wiki/Volta_r.I_Repeater'},
    ## LONG RIFLES
    {'name': "Clancy Cinder M3", 'url': 'https://foxhole.wiki.gg/wiki/Clancy_Cinder_M3'},
    {'name': "KRR2-790 Omen", 'url': 'https://foxhole.wiki.gg/wiki/KRR2-790_Omen'},
    ## SNIPER RIFLES
    {'name': "Clancy-Raca M4", 'url': 'https://foxhole.wiki.gg/wiki/Clancy-Raca_M4'},
    {'name': "KRR3-792 Auger", 'url': 'https://foxhole.wiki.gg/wiki/KRR3-792_Auger'},
    ## SUBMACHINE GUN
    {'name': "“Lionclaw” mc.VIII", 'url': 'https://foxhole.wiki.gg/wiki/%E2%80%9CLionclaw%E2%80%9D_mc.VIII'},
    {'name': "“The Pitch Gun” mc.V", 'url': 'https://foxhole.wiki.gg/wiki/%E2%80%9CThe_Pitch_Gun%E2%80%9D_mc.V'},
    {'name': "Fiddler Submachine Gun Model 868", 'url': 'https://foxhole.wiki.gg/wiki/Fiddler_Submachine_Gun_Model_868'},
    {'name': "No.1 “The Liar” Submachine Gun", 'url': 'https://foxhole.wiki.gg/wiki/No.1_%E2%80%9CThe_Liar%E2%80%9D_Submachine_Gun'},
    ## ASSAULT RIFLES
    {'name': "“Dusk” ce.III", 'url': 'https://foxhole.wiki.gg/wiki/%E2%80%9CDusk%E2%80%9D_ce.III'},
    {'name': "Aalto Storm Rifle 24", 'url': 'https://foxhole.wiki.gg/wiki/Aalto_Storm_Rifle_24'},
    {'name': "Booker Storm Rifle Model 838", 'url': 'https://foxhole.wiki.gg/wiki/Booker_Storm_Rifle_Model_838'},
    ## SHOTGUN
    {'name': "Brasa Shotgun", 'url': 'https://foxhole.wiki.gg/wiki/Shotgun'},
    ## PISTOLS
    {'name': "Ahti Model 2", 'url': 'https://foxhole.wiki.gg/wiki/Ahti_Model_2'},
    {'name': "Cascadier 873", 'url': 'https://foxhole.wiki.gg/wiki/Cascadier_873'},
    {'name': "Ferro 879", 'url': 'https://foxhole.wiki.gg/wiki/Ferro_879'},
    ## REVOLVER
    {'name': "Cometa T2-9", 'url': 'https://foxhole.wiki.gg/wiki/Revolver'},
    ## LIGHT MACHINE GUN
    {'name': "Catara mo.II", 'url': 'https://foxhole.wiki.gg/wiki/Light_Machine_Gun'},
    ## HEAVY MACHINE GUN
    {'name': "KRN886-127 Gast Machine Gun", 'url': 'https://foxhole.wiki.gg/wiki/KRN886-127_Gast_Machine_Gun'},
    {'name': "Malone MK.2", 'url': 'https://foxhole.wiki.gg/wiki/Malone_MK.2'},
    ## ATR
    {'name': "20 Neville Anti-Tank Rifle", 'url': 'https://foxhole.wiki.gg/wiki/Anti-Tank_Rifle'},
    ## MOUNTED ATR
    {'name': "“Typhon” ra.XII", 'url': 'https://foxhole.wiki.gg/wiki/Mounted_Anti-Tank_Rifle'},
    ## MOUNTED MACHINE GUN
    {'name': "Lamentum mm.IV", 'url': 'https://foxhole.wiki.gg/wiki/Lamentum_mm.IV'},
    {'name': "Malone Ratcatcher MK.1", 'url': 'https://foxhole.wiki.gg/wiki/Malone_Ratcatcher_MK.1'},
    ## ISG
    {'name': "Daucus isg.III", 'url': 'https://foxhole.wiki.gg/wiki/Mounted_Infantry_Support_Gun'},
    ## FLAME THROWERS
    {'name': "“Molten Wind” v.II Flame Torch", 'url': 'https://foxhole.wiki.gg/wiki/%E2%80%9CMolten_Wind%E2%80%9D_v.II_Flame_Torch'},
    {'name': "Willow's Bane Model 845", 'url': 'https://foxhole.wiki.gg/wiki/Willow%27s_Bane_Model_845'},
    ## GRENADES
    {'name': "A3 Harpa Fragmentation Grenade", 'url': 'https://foxhole.wiki.gg/wiki/A3_Harpa_Fragmentation_Grenade'},
    {'name': "Bomastone Grenade", 'url': 'https://foxhole.wiki.gg/wiki/Bomastone_Grenade'},
    ## HE GRENADES
    {'name': "Mammon 91-b", 'url': 'https://foxhole.wiki.gg/wiki/Mammon_91-b'},
    {'name': "Tremola Grenade GPb-1", 'url': 'https://foxhole.wiki.gg/wiki/Tremola_Grenade_GPb-1'},
    ## GAS GRENADE
    {'name': "Green Ash Grenade", 'url': 'https://foxhole.wiki.gg/wiki/Gas_Grenade'},
    ## AT GRENADES
    {'name': "Anti-Tank Sticky Bomb", 'url': 'https://foxhole.wiki.gg/wiki/Anti-Tank_Sticky_Bomb'},
    {'name': "BF5 White Ash Flask Grenade", 'url': 'https://foxhole.wiki.gg/wiki/Anti-Tank_Grenade'},
    ## SMOKE GRENADES
    {'name': "PT-815 Smoke Grenade", 'url': 'https://foxhole.wiki.gg/wiki/Smoke_Grenade'},
    ## EXPLOSIVE CHARGES
    {'name': "Alligator Charge", 'url': 'https://foxhole.wiki.gg/wiki/Alligator_Charge'},
    {'name': "Hydra's Whisper", 'url': 'https://foxhole.wiki.gg/wiki/Hydra%27s_Whisper'},
    {'name': "Abisme AT-99", 'url': 'https://foxhole.wiki.gg/wiki/Abisme_AT-99'},
    {'name': "Havoc Charge", 'url': 'https://foxhole.wiki.gg/wiki/Havoc_Charge'},
    {'name': "E680-S Rudder Lock", 'url': 'https://foxhole.wiki.gg/wiki/Sea_Mine'},
    ## GRENADES LAUNCHERS
    {'name': "KLG901-2 Lunaire F", 'url': 'https://foxhole.wiki.gg/wiki/KLG901-2_Lunaire_F'},
    {'name': "The Ospreay", 'url': 'https://foxhole.wiki.gg/wiki/The_Ospreay'},
    ## RPG LAUNCHER
    {'name': "Cutler Launcher 4", 'url': 'https://foxhole.wiki.gg/wiki/RPG_Launcher'},
    ## AT RPG
    {'name': "Bane 45", 'url': 'https://foxhole.wiki.gg/wiki/Bane_45'},
    {'name': "Bonesaw MK.3", 'url': 'https://foxhole.wiki.gg/wiki/Bonesaw_MK.3'},
    {'name': "Ignifist 30", 'url': 'https://foxhole.wiki.gg/wiki/Ignifist_30'},
    {'name': "Venom c.II 35", 'url': 'https://foxhole.wiki.gg/wiki/Venom_c.II_35'},
    ## MORTAR
    {'name': "Cremari Mortar", 'url': 'https://foxhole.wiki.gg/wiki/Mortar'},
    ## MOUNTED RPG LAUNCHER
    {'name': "Cutler Foebreaker", 'url': 'https://foxhole.wiki.gg/wiki/Mounted_RPG_Launcher'},
    ## MOUNTED AT RPG
    {'name': "Mounted Bonesaw MK.3", 'url': 'https://foxhole.wiki.gg/wiki/Mounted_Anti-Tank_RPG'},
    ## MOUNTED GRENADE LAUNCHER
    {'name': "Mounted Fissura gd.I", 'url': 'https://foxhole.wiki.gg/wiki/Mounted_Grenade_Launcher'},
    ## MELEE
    {'name': "Buckhorn CCQ-18 Bayonet", 'url': 'https://foxhole.wiki.gg/wiki/Bayonet'},
    {'name': "Fists", 'url': 'https://foxhole.wiki.gg/wiki/Fists'},
    ## MAGAZINES
    {'name': "9mm", 'url': 'https://foxhole.wiki.gg/wiki/9mm'},
    {'name': "8mm", 'url': 'https://foxhole.wiki.gg/wiki/8mm'},
    {'name': "7.92mm", 'url': 'https://foxhole.wiki.gg/wiki/7.92mm'},
    {'name': "7.62mm", 'url': 'https://foxhole.wiki.gg/wiki/7.62mm'},
    {'name': ".44", 'url': 'https://foxhole.wiki.gg/wiki/.44'},
    {'name': "Buckshot", 'url': 'https://foxhole.wiki.gg/wiki/Buckshot'},
    {'name': "Flame Ammo", 'url': 'https://foxhole.wiki.gg/wiki/Flame_Ammo'},
    {'name': "12.7mm", 'url': 'https://foxhole.wiki.gg/wiki/12.7mm'},
    {'name': "20mm", 'url': 'https://foxhole.wiki.gg/wiki/20mm'},
    ## SHELLS
    {'name': "30mm", 'url': 'https://foxhole.wiki.gg/wiki/30mm'},
    {'name': "40mm", 'url': 'https://foxhole.wiki.gg/wiki/40mm'},
    {'name': "68mm", 'url': 'https://foxhole.wiki.gg/wiki/68mm'},
    {'name': "75mm", 'url': 'https://foxhole.wiki.gg/wiki/75mm'},
    {'name': "94.5mm", 'url': 'https://foxhole.wiki.gg/wiki/94.5mm'},
    ## ARTY AMMO
    {'name': "Flare Mortar Shell", 'url': 'https://foxhole.wiki.gg/wiki/Flare_Mortar_Shell'},
    {'name': "Shrapnel Mortar Shell", 'url': 'https://foxhole.wiki.gg/wiki/Shrapnel_Mortar_Shell'},
    {'name': "Mortar Shell", 'url': 'https://foxhole.wiki.gg/wiki/Mortar_Shell'},
    {'name': "4C-Fire Rocket", 'url': 'https://foxhole.wiki.gg/wiki/4C-Fire_Rocket'},
    {'name': "3C-High Explosive Rocket", 'url': 'https://foxhole.wiki.gg/wiki/3C-High_Explosive_Rocket'},
    {'name': "120mm", 'url': 'https://foxhole.wiki.gg/wiki/120mm'},
    {'name': "150mm", 'url': 'https://foxhole.wiki.gg/wiki/150mm'},
    {'name': "300mm", 'url': 'https://foxhole.wiki.gg/wiki/300mm'},
    {'name': "RPG", 'url': 'https://foxhole.wiki.gg/wiki/RPG'},
    ## PROPELLED EXPLOSIVES
    {'name': "AP⧸RPG", 'url': 'https://foxhole.wiki.gg/wiki/AP%E2%A7%B8RPG'},
    {'name': "ARC⧸RPG", 'url': 'https://foxhole.wiki.gg/wiki/ARC%E2%A7%B8RPG'},
    {'name': "250mm", 'url': 'https://foxhole.wiki.gg/wiki/250mm'},
    {'name': "“Molten Wind” v.II Ammo", 'url': 'https://foxhole.wiki.gg/wiki/%E2%80%9CMolten_Wind%E2%80%9D_v.II_Ammo'},
    ## FLAMETHROWER AMMO
    {'name': "Willow's Bane Ammo", 'url': 'https://foxhole.wiki.gg/wiki/Willow%27s_Bane_Ammo'},
    ## TORPEDO / DEPTH CHARGES
    {'name': "Moray Torpedo", 'url': 'https://foxhole.wiki.gg/wiki/Torpedo'},
    {'name': "Model-7 “Evie”", 'url': 'https://foxhole.wiki.gg/wiki/Depth_Charge'},
    ## ARMORED CARS
    {'name': "T3 “Xiphos”", 'url': 'https://foxhole.wiki.gg/wiki/T3_%E2%80%9CXiphos%E2%80%9D'},
    {'name': "T5 “Percutio”", 'url': 'https://foxhole.wiki.gg/wiki/T5_%E2%80%9CPercutio%E2%80%9D'},
    {'name': "T8 “Gemini”", 'url': 'https://foxhole.wiki.gg/wiki/T8_%E2%80%9CGemini%E2%80%9D'},
    {'name': "O'Brien V.110", 'url': 'https://foxhole.wiki.gg/wiki/O%27Brien_V.110'},
    {'name': "O'Brien V.113 Gravekeeper", 'url': 'https://foxhole.wiki.gg/wiki/O%27Brien_V.113_Gravekeeper'},
    {'name': "O'Brien V.121 Highlander", 'url': 'https://foxhole.wiki.gg/wiki/O%27Brien_V.121_Highlander'},
    {'name': "O'Brien V.130 Wild Jack", 'url': 'https://foxhole.wiki.gg/wiki/O%27Brien_V.130_Wild_Jack'},
    {'name': "O'Brien V.190 Knave", 'url': 'https://foxhole.wiki.gg/wiki/O%27Brien_V.190_Knave'},
    {'name': "O'Brien V.101 Freeman", 'url': 'https://foxhole.wiki.gg/wiki/O%27Brien_V.101_Freeman'},
    ## TANKETTE
    {'name': "T12 “Actaeon” Tankette", 'url': 'https://foxhole.wiki.gg/wiki/T12_%E2%80%9CActaeon%E2%80%9D_Tankette'},
    {'name': "T13 “Deioneus” Rocket Battery", 'url': 'https://foxhole.wiki.gg/wiki/T13_%E2%80%9CDeioneus%E2%80%9D_Rocket_Battery'},
    {'name': "T14 “Vesta” Tankette", 'url': 'https://foxhole.wiki.gg/wiki/T14_%E2%80%9CVesta%E2%80%9D_Tankette'},
    {'name': "T20 “Ixion” Tankette", 'url': 'https://foxhole.wiki.gg/wiki/T20_%E2%80%9CIxion%E2%80%9D_Tankette'},
    ## APCs
    {'name': "AB-8 “Acheron”", 'url': 'https://foxhole.wiki.gg/wiki/AB-8_%E2%80%9CAcheron%E2%80%9D'},
    {'name': "AB-11 “Doru”", 'url': 'https://foxhole.wiki.gg/wiki/AB-11_%E2%80%9CDoru%E2%80%9D'},
    {'name': "Mulloy LPC", 'url': 'https://foxhole.wiki.gg/wiki/Mulloy_LPC'},
    ## HALFTRACKS
    {'name': "HH-a “Javelin”", 'url': 'https://foxhole.wiki.gg/wiki/HH-a_%E2%80%9CJavelin%E2%80%9D'},
    {'name': "HH-b “Hoplite”", 'url': 'https://foxhole.wiki.gg/wiki/HH-b_%E2%80%9CHoplite%E2%80%9D'},
    {'name': "HH-d “Peltast”", 'url': 'https://foxhole.wiki.gg/wiki/HH-d_%E2%80%9CPeltast%E2%80%9D'},
    {'name': "Niska Mk. I Gun Motor Carriage", 'url': 'https://foxhole.wiki.gg/wiki/Niska_Mk._I_Gun_Motor_Carriage'},
    {'name': "Niska Mk. II Blinder", 'url': 'https://foxhole.wiki.gg/wiki/Niska_Mk._II_Blinder'},
    {'name': "Niska Mk. III Scar Twin", 'url': 'https://foxhole.wiki.gg/wiki/Niska_Mk._III_Scar_Twin'},
    {'name': "Niska-Rycker Mk. IX Skycaller", 'url': 'https://foxhole.wiki.gg/wiki/Niska-Rycker_Mk._IX_Skycaller'},
    ## FIELD MACHINE GUNS
    {'name': "Swallowtail 988/127-2", 'url': 'https://foxhole.wiki.gg/wiki/Swallowtail_988/127-2'},
    {'name': "G40 “Sagittarii”", 'url': 'https://foxhole.wiki.gg/wiki/G40_%E2%80%9CSagittarii%E2%80%9D'},
    ## FIELD ATR
    {'name': "Duncan's Coin 20mm", 'url': 'https://foxhole.wiki.gg/wiki/Duncan%27s_Coin_20mm'},
    {'name': "GA6 “Cestus”", 'url': 'https://foxhole.wiki.gg/wiki/GA6_%E2%80%9CCestus%E2%80%9D'},
    ## FIELD ARTY
    {'name': "120-68 “Koronides” Field Gun", 'url': 'https://foxhole.wiki.gg/wiki/Field_Artillery'},
    ## FIELD CANNON
    {'name': "Balfour Wolfhound 40mm", 'url': 'https://foxhole.wiki.gg/wiki/Field_Cannon'},
    ## FIELD ROCKET LAUNCHER
    {'name': "Rycker 4/3-F Wasp Nest", 'url': 'https://foxhole.wiki.gg/wiki/Field_Launcher'},
    ## FIELD AT GUN
    {'name': "Collins Cannon 68mm", 'url': 'https://foxhole.wiki.gg/wiki/Collins_Cannon_68mm'},
    {'name': "AA-2 Battering Ram", 'url': 'https://foxhole.wiki.gg/wiki/AA-2_Battering_Ram'},
    ## FIELD MORTAR
    {'name': "Balfour Falconer 250mm", 'url': 'https://foxhole.wiki.gg/wiki/Field_Mortar'},
    ## HEAVY FIELD CANON
    {'name': "Balfour Rampart 68mm", 'url': 'https://foxhole.wiki.gg/wiki/Heavy_Field_Cannon'},
    ## HEAVY FIELD GUN
    {'name': "40-45 “Smelter” Heavy Field Gun", 'url': 'https://foxhole.wiki.gg/wiki/Heavy_Field_Gun'},
    ## LARGE FIELD GUN
    {'name': "Balfour Stockade 75mm", 'url': 'https://foxhole.wiki.gg/wiki/Balfour_Stockade_75mm'},
    {'name': "945g “Stygian Bolt”", 'url': 'https://foxhole.wiki.gg/wiki/945g_%E2%80%9CStygian_Bolt%E2%80%9D'},
    ## SCOUT TANK
    {'name': "King Spire Mk. I", 'url': 'https://foxhole.wiki.gg/wiki/King_Spire_Mk._I'},
    {'name': "King Gallant Mk. II", 'url': 'https://foxhole.wiki.gg/wiki/King_Gallant_Mk._II'},
    {'name': "King Jester - Mk. I-1", 'url': 'https://foxhole.wiki.gg/wiki/King_Jester_-_Mk._I-1'},
    ## LIGHT TANK
    {'name': "H-5 “Hatchet”", 'url': 'https://foxhole.wiki.gg/wiki/H-5_%E2%80%9CHatchet%E2%80%9D'},
    {'name': "H-10 “Pelekys”", 'url': 'https://foxhole.wiki.gg/wiki/H-10_%E2%80%9CPelekys%E2%80%9D'},
    {'name': "H-19 “Vulcan”", 'url': 'https://foxhole.wiki.gg/wiki/H-19_%E2%80%9CVulcan%E2%80%9D'},
    {'name': "H-8 “Kranesca”", 'url': 'https://foxhole.wiki.gg/wiki/H-8_%E2%80%9CKranesca%E2%80%9D'},
    {'name': "Devitt Mk. III", 'url': 'https://foxhole.wiki.gg/wiki/Devitt_Mk._III'},
    {'name': "Devitt Ironhide Mk. IV", 'url': 'https://foxhole.wiki.gg/wiki/Devitt_Ironhide_Mk._IV'},
    {'name': "Devitt-Caine Mk. IV MMR", 'url': 'https://foxhole.wiki.gg/wiki/Devitt-Caine_Mk._IV_MMR'},
    ## ASSAULT TANK
    {'name': "85K-b “Falchion”", 'url': 'https://foxhole.wiki.gg/wiki/85K-b_%E2%80%9CFalchion%E2%80%9D'},
    {'name': "85K-a “Spatha”", 'url': 'https://foxhole.wiki.gg/wiki/85K-a_%E2%80%9CSpatha%E2%80%9D'},
    {'name': "85V-g “Talos”", 'url': 'https://foxhole.wiki.gg/wiki/85V-g_%E2%80%9CTalos%E2%80%9D'},
    {'name': "86K-a “Bardiche”", 'url': 'https://foxhole.wiki.gg/wiki/86K-a_%E2%80%9CBardiche%E2%80%9D'},
    {'name': "86K-c “Ranseur”", 'url': 'https://foxhole.wiki.gg/wiki/86K-c_%E2%80%9CRanseur%E2%80%9D'},
    {'name': "Silverhand - Mk. IV", 'url': 'https://foxhole.wiki.gg/wiki/Silverhand_-_Mk._IV'},
    {'name': "Silverhand Chieftain - Mk. VI", 'url': 'https://foxhole.wiki.gg/wiki/Silverhand_Chieftain_-_Mk._VI'},
    {'name': "Silverhand Lordscar - Mk. X", 'url': 'https://foxhole.wiki.gg/wiki/Silverhand_Lordscar_-_Mk._X'},
    ## CRUISER TANK
    {'name': "Gallagher Outlaw Mk. II", 'url': 'https://foxhole.wiki.gg/wiki/Gallagher_Outlaw_Mk._II'},
    {'name': "Gallagher Highwayman Mk. III", 'url': 'https://foxhole.wiki.gg/wiki/Gallagher_Highwayman_Mk._III'},
    {'name': "Gallagher Thornfall Mk. VI", 'url': 'https://foxhole.wiki.gg/wiki/Gallagher_Thornfall_Mk._VI'},
    ## INFANTRY SUPPORT TANK
    {'name': "HC-2 “Scorpion”", 'url': 'https://foxhole.wiki.gg/wiki/Light_Infantry_Tank'},
    ## SIEGE TANK
    {'name': "HC-7 “Ballista”", 'url': 'https://foxhole.wiki.gg/wiki/Siege_Tank'},
    ## DESTROYER TANK
    {'name': "Noble Widow MK. XIV", 'url': 'https://foxhole.wiki.gg/wiki/Noble_Widow_MK._XIV'},
    {'name': "Noble Firebrand Mk. XVII", 'url': 'https://foxhole.wiki.gg/wiki/Noble_Firebrand_Mk._XVII'},
    ## BATTLE TANK
    {'name': "Flood Juggernaut Mk. VII", 'url': 'https://foxhole.wiki.gg/wiki/Flood_Juggernaut_Mk._VII'},
    {'name': "Flood Mk. I", 'url': 'https://foxhole.wiki.gg/wiki/Flood_Mk._I'},
    {'name': "Flood Mk. IX Stain", 'url': 'https://foxhole.wiki.gg/wiki/Flood_Mk._IX_Stain'},
    {'name': "Lance-25 “Hasta”", 'url': 'https://foxhole.wiki.gg/wiki/Lance-25_%E2%80%9CHasta%E2%80%9D'},
    {'name': "Lance-36", 'url': 'https://foxhole.wiki.gg/wiki/Lance-36'},
    {'name': "Lance-46 “Sarissa”", 'url': 'https://foxhole.wiki.gg/wiki/Lance-46_%E2%80%9CSarissa%E2%80%9D'},
    ## SUPER TANK
    {'name': "Cullen Predator Mk. III", 'url': 'https://foxhole.wiki.gg/wiki/Cullen_Predator_Mk._III'},
    {'name': "O-75b “Ares”", 'url': 'https://foxhole.wiki.gg/wiki/O-75b_%E2%80%9CAres%E2%80%9D'},
    ## FUEL TANKER
    {'name': "Dunne Fuelrunner 2d", 'url': 'https://foxhole.wiki.gg/wiki/Dunne_Fuelrunner_2d'},
    {'name': "RR-3 “Stolon” Tanker", 'url': 'https://foxhole.wiki.gg/wiki/RR-3_%E2%80%9CStolon%E2%80%9D_Tanker'},
    ## TRUCK
    {'name': "R-1 Hauler", 'url': 'https://foxhole.wiki.gg/wiki/R-1_Hauler'},
    {'name': "R-17 “Retiarius” Skirmisher", 'url': 'https://foxhole.wiki.gg/wiki/R-17_%E2%80%9CRetiarius%E2%80%9D_Skirmisher'},
    {'name': "R-5b “Sisyphus” Hauler", 'url': 'https://foxhole.wiki.gg/wiki/R-5b_%E2%80%9CSisyphus%E2%80%9D_Hauler'},
    {'name': "R-9 “Speartip” Escort", 'url': 'https://foxhole.wiki.gg/wiki/R-9_%E2%80%9CSpeartip%E2%80%9D_Escort'},
    {'name': "R-5 “Atlas” Hauler", 'url': 'https://foxhole.wiki.gg/wiki/R-5_%E2%80%9CAtlas%E2%80%9D_Hauler'},
    {'name': "Dunne Loadlugger 3c", 'url': 'https://foxhole.wiki.gg/wiki/Dunne_Loadlugger_3c'},
    {'name': "Dunne Transport", 'url': 'https://foxhole.wiki.gg/wiki/Dunne_Transport'},
    {'name': "Dunne Landrunner 12c", 'url': 'https://foxhole.wiki.gg/wiki/Dunne_Landrunner_12c'},
    {'name': "Dunne Leatherback 2a", 'url': 'https://foxhole.wiki.gg/wiki/Dunne_Leatherback_2a'},
    ## UTILITY VEHICLE
    {'name': "BMS - Class 2 Mobile Auto-Crane", 'url': 'https://foxhole.wiki.gg/wiki/Crane'},
    {'name': "BMS - Universal Assembly Rig", 'url': 'https://foxhole.wiki.gg/wiki/Construction_Vehicle'},
    {'name': "BMS - Fabricator", 'url': 'https://foxhole.wiki.gg/wiki/Advanced_Construction_Vehicle'},
    {'name': "BMS - Packmule Flatbed", 'url': 'https://foxhole.wiki.gg/wiki/Flatbed_Truck'},
    {'name': "BMS - Scrap Hauler", 'url': 'https://foxhole.wiki.gg/wiki/Harvester'},
    ## TRAILER
    {'name': "Rooster - Junkwagon", 'url': 'https://foxhole.wiki.gg/wiki/Rooster_-_Junkwagon'},
    {'name': "Rooster - Lamploader", 'url': 'https://foxhole.wiki.gg/wiki/Rooster_-_Lamploader'},
    {'name': "Rooster - Tumblebox", 'url': 'https://foxhole.wiki.gg/wiki/Rooster_-_Tumblebox'},
    ## FIRETRUCK
    {'name': "Dunne Dousing Engine 3r", 'url': 'https://foxhole.wiki.gg/wiki/Dunne_Dousing_Engine_3r'},
    {'name': "R-12b - “Salva” Flame Truck", 'url': 'https://foxhole.wiki.gg/wiki/R-12b_-_%E2%80%9CSalva%E2%80%9D_Flame_Truck'},
    ## BUS
    {'name': "Dunne Caravaner 2f", 'url': 'https://foxhole.wiki.gg/wiki/Dunne_Caravaner_2f'},
    {'name': "R-15 - “Chariot”", 'url': 'https://foxhole.wiki.gg/wiki/R-15_-_%E2%80%9CChariot%E2%80%9D'},
    ## AMBULANCE
    {'name': "Dunne Responder 3e", 'url': 'https://foxhole.wiki.gg/wiki/Dunne_Responder_3e'},
    {'name': "R-12 - “Salus” Ambulance", 'url': 'https://foxhole.wiki.gg/wiki/R-12_-_%E2%80%9CSalus%E2%80%9D_Ambulance'},
    ## HEAVY TRUCKS
    {'name': "Cnute Cliffwrest", 'url': 'https://foxhole.wiki.gg/wiki/Cnute_Cliffwrest'},
    {'name': "AU-A150 Taurine Rigger", 'url': 'https://foxhole.wiki.gg/wiki/AU-A150_Taurine_Rigger'},
    ## BYCYCLE
    {'name': "Blumfield LK205", 'url': 'https://foxhole.wiki.gg/wiki/Bicycle'},
    ## MOTORCYCLE
    {'name': "03MM “Caster”", 'url': 'https://foxhole.wiki.gg/wiki/03MM_%E2%80%9CCaster%E2%80%9D'},
    {'name': "00MS “Stinger”", 'url': 'https://foxhole.wiki.gg/wiki/00MS_%E2%80%9CStinger%E2%80%9D'},
    {'name': "Kivela Power Wheel 80-1", 'url': 'https://foxhole.wiki.gg/wiki/Kivela_Power_Wheel_80-1'},
    ## LIGHT UTILITY VEHICLE
    {'name': "UV-05a “Argonaut”", 'url': 'https://foxhole.wiki.gg/wiki/UV-05a_%E2%80%9CArgonaut%E2%80%9D'},
    {'name': "UV-24 “Icarus”", 'url': 'https://foxhole.wiki.gg/wiki/UV-24_%E2%80%9CIcarus%E2%80%9D'},
    {'name': "UV-5c “Odyssey”", 'url': 'https://foxhole.wiki.gg/wiki/UV-5c_%E2%80%9COdyssey%E2%80%9D'},
    {'name': "Drummond 100a", 'url': 'https://foxhole.wiki.gg/wiki/Drummond_100a'},
    {'name': "Drummond Loscann 55c", 'url': 'https://foxhole.wiki.gg/wiki/Drummond_Loscann_55c'},
    {'name': "Drummond Spitfire 100d", 'url': 'https://foxhole.wiki.gg/wiki/Drummond_Spitfire_100d'},
    ## LANDING SHIP
    {'name': "MacConmara Shorerunner", 'url': 'https://foxhole.wiki.gg/wiki/MacConmara_Shorerunner'},
    {'name': "Interceptor PA-12", 'url': 'https://foxhole.wiki.gg/wiki/Interceptor_PA-12'},
    ## BARGE
    {'name': "BMS - Aquatipper", 'url': 'https://foxhole.wiki.gg/wiki/Barge'},
    ## FREIGHTER
    {'name': "BMS - Ironship", 'url': 'https://foxhole.wiki.gg/wiki/Freighter'},
    ## GUNBOAT
    {'name': "74b-1 Ronan Gunship", 'url': 'https://foxhole.wiki.gg/wiki/74b-1_Ronan_Gunship'},
    {'name': "Type C - “Charon”", 'url': 'https://foxhole.wiki.gg/wiki/Type_C_-_%E2%80%9CCharon%E2%80%9D'},
    ## SUBMARINE
    {'name': "Nakki", 'url': 'https://foxhole.wiki.gg/wiki/Nakki'},
    {'name': "AC-b “Trident”", 'url': 'https://foxhole.wiki.gg/wiki/AC-b_%E2%80%9CTrident%E2%80%9D'},
    ## FRIGATE
    {'name': "Blacksteele", 'url': 'https://foxhole.wiki.gg/wiki/Blacksteele'},
    ## DESTROYER
    {'name': "Conqueror", 'url': 'https://foxhole.wiki.gg/wiki/Conqueror'},
    ## BASE SHIP
    {'name': "BMS - Longhook", 'url': 'https://foxhole.wiki.gg/wiki/Base_Ship'},
    ## STORAGE SHIP
    {'name': "BMS - Bluefin", 'url': 'https://foxhole.wiki.gg/wiki/Storage_Ship'},
    ## BATTLESHIP
    {'name': "Callahan (Battleship)", 'url': 'https://foxhole.wiki.gg/wiki/Callahan_(Battleship)'},
    {'name': "Titan", 'url': 'https://foxhole.wiki.gg/wiki/Titan'},
    ## MOTORBOAT
    {'name': "BMS - Grouper", 'url': 'https://foxhole.wiki.gg/wiki/Motorboat'},
    ## SMALL TRAIN
    {'name': "BMS Railtruck", 'url': 'https://foxhole.wiki.gg/wiki/Small_Container_Car'},
    {'name': "BMS Linerunner", 'url': 'https://foxhole.wiki.gg/wiki/Small_Flatbed_Car'},
    {'name': "BMS Tinderbox", 'url': 'https://foxhole.wiki.gg/wiki/Small_Liquid_Container_Car'},
    {'name': "BMS Mineseeker", 'url': 'https://foxhole.wiki.gg/wiki/Small_Train_Locomotive'},
    ## LARGE TRAIN
    {'name': "BMS Rockhold", 'url': 'https://foxhole.wiki.gg/wiki/Container_Car'},
    {'name': "BMS Roadhouse", 'url': 'https://foxhole.wiki.gg/wiki/Caboose'},
    {'name': "BMS Longrider", 'url': 'https://foxhole.wiki.gg/wiki/Flatbed_Car'},
    {'name': "BMS Holdout", 'url': 'https://foxhole.wiki.gg/wiki/Infantry_Car'},
    {'name': "BMS Black Bolt", 'url': 'https://foxhole.wiki.gg/wiki/Locomotive'},
    {'name': "O'Brien Warsmith v.215", 'url': 'https://foxhole.wiki.gg/wiki/O%27Brien_Warsmith_v.215'},
    {'name': "Aegis Steelbreaker K5a", 'url': 'https://foxhole.wiki.gg/wiki/Aegis_Steelbreaker_K5a'},
    {'name': "Tempest Cannon RA-2", 'url': 'https://foxhole.wiki.gg/wiki/Long-Range_Artillery_Car'},
    ## LARGE CRANE
    {'name': "BMS - Overseer Sky-Hauler", 'url': 'https://foxhole.wiki.gg/wiki/Large_Crane'},
    ## RELIC VEHICLE
    {'name': "Heavy Infantry Carrier", 'url': 'https://foxhole.wiki.gg/wiki/Heavy_Infantry_Carrier'},
    {'name': "Armoured Fighting Tractor", 'url': 'https://foxhole.wiki.gg/wiki/Armoured_Fighting_Tractor'},
    {'name': "PL-1 “Phalanx”", 'url': 'https://foxhole.wiki.gg/wiki/Relic_Assault_Tank'},
    {'name': "Storm Tank", 'url': 'https://foxhole.wiki.gg/wiki/Storm_Tank'},
    {'name': "Staff Car", 'url': 'https://foxhole.wiki.gg/wiki/Staff_Car'},
    {'name': "Repurposed Truck", 'url': 'https://foxhole.wiki.gg/wiki/Repurposed_Truck'},
    ## MECH VEHICLE
    {'name': "Herne QMW 1a Scourge Hunter", 'url': 'https://foxhole.wiki.gg/wiki/Herne_QMW_1a_Scourge_Hunter'},
    {'name': "Centurion MV-2", 'url': 'https://foxhole.wiki.gg/wiki/Centurion_MV-2'},
    ## HOME BASE
    {'name': "Border Base", 'url': 'https://foxhole.wiki.gg/wiki/Border_Base'},
    {'name': "Relic Base", 'url': 'https://foxhole.wiki.gg/wiki/Relic_Base'},
    {'name': "Town Base (Tier 1)", 'url': 'https://foxhole.wiki.gg/wiki/Town_Base#Tier_1-0'},
    {'name': "Town Base (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Town_Base#Tier_2-0'},
    {'name': "Town Base (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Town_Base#Tier_3-0'},
    ## FORWARD BASE
    {'name': "Bunker Base (Tier 1)", 'url': 'https://foxhole.wiki.gg/wiki/Bunker_Base#Tier_1-0'},
    {'name': "Bunker Base (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Bunker_Base#Tier_2-0'},
    {'name': "Bunker Base (Tier 3)", 'url': ' https://foxhole.wiki.gg/wiki/Bunker_Base#Tier_3-0'},
    {'name': "Encampment", 'url': 'https://foxhole.wiki.gg/wiki/Encampment'},
    {'name': "Keep", 'url': 'https://foxhole.wiki.gg/wiki/Keep'},
    {'name': "Safe House (Tier 1)", 'url': 'https://foxhole.wiki.gg/wiki/Safe_House#Tier_1-0'},
    {'name': "Safe House (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Safe_House#Tier_2-0'},
    {'name': "Safe House (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Safe_House#Tier_3-0'},
    ## WORLD STORAGE
    {'name': "Seaport", 'url': 'https://foxhole.wiki.gg/wiki/Seaport'},
    {'name': "Storage Depot", 'url': 'https://foxhole.wiki.gg/wiki/Storage_Depot'},
    ## PLAYER MADE STORAGE
    {'name': "Liquid Container", 'url': 'https://foxhole.wiki.gg/wiki/Liquid_Container'},
    {'name': "Liquid Transfer Station", 'url': 'https://foxhole.wiki.gg/wiki/Liquid_Transfer_Station'},
    {'name': "Material Pallet", 'url': 'https://foxhole.wiki.gg/wiki/Material_Pallet'},
    {'name': "Material Transfer Station", 'url': 'https://foxhole.wiki.gg/wiki/Material_Transfer_Station'},
    {'name': "Resource Container", 'url': 'https://foxhole.wiki.gg/wiki/Resource_Container'},
    {'name': "Resource Transfer Station", 'url': 'https://foxhole.wiki.gg/wiki/Resource_Transfer_Station'},
    {'name': "Shippable Crate", 'url': 'https://foxhole.wiki.gg/wiki/Shippable_Crate'},
    {'name': "Shipping Container", 'url': 'https://foxhole.wiki.gg/wiki/Shipping_Container'},
    {'name': "Storage Box", 'url': 'https://foxhole.wiki.gg/wiki/Storage_Box'},
    {'name': "Storage Room (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Storage_Room#Tier_2-0'},
    {'name': "Storage Room (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Storage_Room#Tier_3-0'},
    ## AUTOMATED WORLD DEFENSE
    {'name': "Coastal Gun", 'url': 'https://foxhole.wiki.gg/wiki/Coastal_Gun'},
    {'name': "Garrisoned House", 'url': 'https://foxhole.wiki.gg/wiki/Garrisoned_House'},
    {'name': "Observation Tower", 'url': 'https://foxhole.wiki.gg/wiki/Observation_Tower'},
    ## PLAYER MADE DEFENSE
    {'name': "Anti-Tank Pillbox", 'url': 'https://foxhole.wiki.gg/wiki/Anti-Tank_Pillbox'},
    {'name': "AT Gun Garrison (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/AT_Gun_Garrison#Tier_2-0'},
    {'name': "AT Gun Garrison (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/AT_Gun_Garrison#Tier_3-0'},
    {'name': "Howitzer Garrison", 'url': 'https://foxhole.wiki.gg/wiki/Howitzer_Garrison'},
    {'name': "Machine Gun Garrison (Tier 1)", 'url': 'https://foxhole.wiki.gg/wiki/Machine_Gun_Garrison#Tier_1-0'},
    {'name': "Machine Gun Garrison (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Machine_Gun_Garrison#Tier_2-0'},
    {'name': "Machine Gun Garrison (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Machine_Gun_Garrison#Tier_3-0'},
    {'name': "Machine Gun Pillbox", 'url': 'https://foxhole.wiki.gg/wiki/Machine_Gun_Pillbox'},
    {'name': "Observation Bunker (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Observation_Bunker#Tier_2-0'},
    {'name': "Observation Bunker (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Observation_Bunker#Tier_3-0'},
    {'name': "Rifle Garrison (Tier 1)", 'url': 'https://foxhole.wiki.gg/wiki/Rifle_Garrison#Tier_1-0'},
    {'name': "Rifle Garrison (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Rifle_Garrison#Tier_2-0'},
    {'name': "Rifle Garrison (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Rifle_Garrison#Tier_3-0'},
    {'name': "Rifle Pillbox", 'url': 'https://foxhole.wiki.gg/wiki/Rifle_Pillbox'},
    {'name': "Watch Tower", 'url': 'https://foxhole.wiki.gg/wiki/Watch_Tower'},
    ## PLAYER MANNED EMPLACEMENT
    {'name': "Emplacement House", 'url': 'https://foxhole.wiki.gg/wiki/Emplacement_House'},
    {'name': "50-500 “Thunderbolt” Cannon", 'url': 'https://foxhole.wiki.gg/wiki/50-500_%E2%80%9CThunderbolt%E2%80%9D_Cannon'},
    {'name': "DAE 1b-2 “Serra”", 'url': 'https://foxhole.wiki.gg/wiki/DAE_1b-2_%E2%80%9CSerra%E2%80%9D'},
    {'name': "DAE 1o-3 “Polybolos”", 'url': 'https://foxhole.wiki.gg/wiki/DAE_1o-3_%E2%80%9CPolybolos%E2%80%9D'},
    {'name': "DAE 2a-1 “Ruptura”", 'url': 'https://foxhole.wiki.gg/wiki/DAE_2a-1_%E2%80%9CRuptura%E2%80%9D'},
    {'name': "DAE 3b-2 “Hades' Net”", 'url': 'https://foxhole.wiki.gg/wiki/DAE_3b-2_%E2%80%9CHades%27_Net%E2%80%9D'},
    {'name': "Huber Exalt 150mm", 'url': 'https://foxhole.wiki.gg/wiki/Huber_Exalt_150mm'},
    {'name': "Huber Lariat 120mm", 'url': 'https://foxhole.wiki.gg/wiki/Light_Artillery'},
    {'name': "Huber Starbreaker 94.5mm", 'url': 'https://foxhole.wiki.gg/wiki/Huber_Starbreaker_94.5mm'},
    {'name': "Intelligence Center", 'url': 'https://foxhole.wiki.gg/wiki/Intelligence_Center'},
    {'name': "Leary Shellbore 68mm", 'url': 'https://foxhole.wiki.gg/wiki/Leary_Shellbore_68mm'},
    {'name': "Leary Snare Trap 127", 'url': 'https://foxhole.wiki.gg/wiki/Leary_Snare_Trap_127'},
    {'name': "Storm Cannon", 'url': 'https://foxhole.wiki.gg/wiki/Storm_Cannon'},
    ## PROTECTIONS
    {'name': "Barbed Wire", 'url': 'https://foxhole.wiki.gg/wiki/Barbed_Wire_(Structure)'},
    {'name': "Barbed Wire Fence", 'url': 'https://foxhole.wiki.gg/wiki/Barbed_Wire_Fence'},
    {'name': "Bunker (Tier 1)", 'url': 'https://foxhole.wiki.gg/wiki/Bunker#Tier_1-0'},
    {'name': "Bunker (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Bunker#Tier_2-0'},
    {'name': "Bunker (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Bunker#Tier_3-0'},
    {'name': "Bunker Corner (Tier 1)", 'url': 'https://foxhole.wiki.gg/wiki/Bunker_Corner#Tier_1-0'},
    {'name': "Bunker Corner (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Bunker_Corner#Tier_2-0'},
    {'name': "Bunker Corner (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Bunker_Corner#Tier_3-0'},
    {'name': "Bunker Ramp (Tier 1)", 'url': 'https://foxhole.wiki.gg/wiki/Bunker_Ramp#Tier_1-0'},
    {'name': "Bunker Ramp (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Bunker_Ramp#Tier_2-0'},
    {'name': "Bunker Ramp (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Bunker_Ramp#Tier_3-0'},
    {'name': "Dragon's Teeth", 'url': 'https://foxhole.wiki.gg/wiki/Dragon%27s_Teeth'},
    {'name': "Foxhole", 'url': 'https://foxhole.wiki.gg/wiki/Dug_Foxhole'},
    {'name': "Gate (Tier 1)", 'url': 'https://foxhole.wiki.gg/wiki/Gate#Tier_1-0'},
    {'name': "Gate (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Gate#Tier_2-0'},
    {'name': "Gate (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Gate#Tier_3-0'},
    {'name': "Sandbag Cover", 'url': 'https://foxhole.wiki.gg/wiki/Sandbag_Cover#Sandbag_Cover_(Tier_1)-0'},
    {'name': "Sandbag Wall", 'url': 'https://foxhole.wiki.gg/wiki/Sandbag_Cover#Sandbag_Wall_(Tier_2)-0'},
    {'name': "Tank Trap", 'url': 'https://foxhole.wiki.gg/wiki/Tank_Trap'},
    {'name': "Trench (Tier 1)", 'url': 'https://foxhole.wiki.gg/wiki/Trench#Tier_1-0'},
    {'name': "Trench (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Trench#Tier_2-0'},
    {'name': "Trench (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Trench#Tier_3-0'},
    {'name': "Trench Connector (Tier 1)", 'url': 'https://foxhole.wiki.gg/wiki/Trench_Connector#Tier_1-0'},
    {'name': "Trench Connector (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Trench_Connector#Tier_2-0'},
    {'name': "Trench Connector (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Trench_Connector#Tier_3-0'},
    {'name': "Trench Emplacement (Tier 1)", 'url': 'https://foxhole.wiki.gg/wiki/Trench_Emplacement#Tier_1-0'},
    {'name': "Trench Emplacement (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Trench_Emplacement#Tier_2-0'},
    {'name': "Trench Emplacement (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Trench_Emplacement#Tier_3-0'},
    {'name': "Wall (Tier 1)", 'url': 'https://foxhole.wiki.gg/wiki/Wall#Tier_1-0'},
    {'name': "Wall (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Wall#Tier_2-0'},
    {'name': "Wall (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Wall#Tier_3-0'},
    ## WORLD PRODUCTION
    {'name': "Construction Yard", 'url': 'https://foxhole.wiki.gg/wiki/Construction_Yard'},
    {'name': "Engineering Center", 'url': 'https://foxhole.wiki.gg/wiki/Engineering_Center'},
    {'name': "Factory", 'url': 'https://foxhole.wiki.gg/wiki/Factory'},
    {'name': "Garage", 'url': 'https://foxhole.wiki.gg/wiki/Garage'},
    {'name': "Hospital", 'url': 'https://foxhole.wiki.gg/wiki/Hospital'},
    {'name': "Mass Production Factory", 'url': 'https://foxhole.wiki.gg/wiki/Mass_Production_Factory'},
    {'name': "Refinery", 'url': 'https://foxhole.wiki.gg/wiki/Refinery'},
    {'name': "Shipyard", 'url': 'https://foxhole.wiki.gg/wiki/Shipyard'},
    ## PLAYER MADE PRODUCTION
    {'name': "A0E-9 Rocket Platform", 'url': 'https://foxhole.wiki.gg/wiki/A0E-9_Rocket_Platform'},
    {'name': "Ammunition Factory", 'url': 'https://foxhole.wiki.gg/wiki/Ammunition_Factory'},
    {'name': "Coal Refinery", 'url': 'https://foxhole.wiki.gg/wiki/Coal_Refinery'},
    {'name': "Concrete Mixer", 'url': 'https://foxhole.wiki.gg/wiki/Concrete_Mixer'},
    {'name': "Diesel Power Plant", 'url': 'https://foxhole.wiki.gg/wiki/Diesel_Power_Plant'},
    {'name': "Dry Dock", 'url': 'https://foxhole.wiki.gg/wiki/Dry_Dock'},
    {'name': "Field Hospital", 'url': 'https://foxhole.wiki.gg/wiki/Field_Hospital'},
    {'name': "Field Modification Center", 'url': 'https://foxhole.wiki.gg/wiki/Field_Modification_Center'},
    {'name': "Large Assembly Station", 'url': 'https://foxhole.wiki.gg/wiki/Large_Assembly_Station'},
    {'name': "Materials Factory", 'url': 'https://foxhole.wiki.gg/wiki/Materials_Factory'},
    {'name': "Metalworks Factory", 'url': 'https://foxhole.wiki.gg/wiki/Metalworks_Factory'},
    {'name': "Oil Refinery", 'url': 'https://foxhole.wiki.gg/wiki/Oil_Refinery'},
    {'name': "Power Station", 'url': 'https://foxhole.wiki.gg/wiki/Power_Station'},
    {'name': "Small Assembly Station", 'url': 'https://foxhole.wiki.gg/wiki/Small_Assembly_Station'},
    ## RESOURCE GENERATION
    {'name': "Oil Field", 'url': 'https://foxhole.wiki.gg/wiki/Oil_Field'},
    {'name': "Coal Field", 'url': 'https://foxhole.wiki.gg/wiki/Coal_Field'},
    {'name': "Salvage Field", 'url': 'https://foxhole.wiki.gg/wiki/Salvage_Field'},
    {'name': "Sulfur Field", 'url': 'https://foxhole.wiki.gg/wiki/Sulfur_Field'},
    {'name': "Component Field", 'url': 'https://foxhole.wiki.gg/wiki/Component_Field'},
    {'name': "Salvage Mine", 'url': 'https://foxhole.wiki.gg/wiki/Salvage_Mine'},
    {'name': "Sulfur Mine", 'url': 'https://foxhole.wiki.gg/wiki/Sulfur_Mine'},
    {'name': "Component Mine", 'url': 'https://foxhole.wiki.gg/wiki/Component_Mine'},
    {'name': "Offshore Platform", 'url': 'https://foxhole.wiki.gg/wiki/Offshore_Platform'},
    ## PLAYER MADE RESOURCE EXTRACTION
    {'name': "Oil Well", 'url': 'https://foxhole.wiki.gg/wiki/Oil_Well'},
    {'name': "Stationary Harvester (Coal)", 'url': 'https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Coal)'},
    {'name': "Stationary Harvester (Components)", 'url': 'https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Components)'},
    {'name': "Stationary Harvester (Scrap)", 'url': 'https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Scrap)'},
    {'name': "Stationary Harvester (Sulfur)", 'url': 'https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Sulfur)'},
    {'name': "Water Pump", 'url': 'https://foxhole.wiki.gg/wiki/Water_Pump'},
    ## BRIDGES
    # TODO: MAKER INFOBOX FOR ALL BRIDGES, EXCEPT FIELD BRIDGE
    {'name': "Wooden Bridge", 'url': 'https://foxhole.wiki.gg/wiki/Bridge#Wooden_Bridge-0'},
    {'name': "Stone Bridge", 'url': 'https://foxhole.wiki.gg/wiki/Bridge#Stone_Bridge-0'},
    {'name': "Two Tier Bridge", 'url': 'https://foxhole.wiki.gg/wiki/Bridge#Two_Tier_Bridge-1'},
    {'name': "Double Bridge", 'url': 'https://foxhole.wiki.gg/wiki/Bridge#Double_Bridge-1'},
    {'name': "Long Bridge", 'url': 'https://foxhole.wiki.gg/wiki/Bridge#Long_Bridge-1'},
    {'name': "Train Bridge", 'url': 'https://foxhole.wiki.gg/wiki/Bridge#Train_Bridge-1'},
    {'name': "Field Bridge", 'url': 'https://foxhole.wiki.gg/wiki/Field_Bridge'},
    ## UTILITY STRUCTURES
    {'name': "Dock", 'url': 'https://foxhole.wiki.gg/wiki/Dock'},
    {'name': "Stationary Crane", 'url': 'https://foxhole.wiki.gg/wiki/Stationary_Crane'},
    {'name': "A0E-9 Rocket", 'url': 'https://foxhole.wiki.gg/wiki/A0E-9_Rocket'},
    {'name': "BMS Foreman Stacker", 'url': 'https://foxhole.wiki.gg/wiki/Facility_Crane'},
    {'name': "Catwalk Bridge", 'url': 'https://foxhole.wiki.gg/wiki/Catwalk_Bridge'},
    {'name': "Catwalk Platform", 'url': 'https://foxhole.wiki.gg/wiki/Catwalk_Platform'},
    {'name': "Catwalk Stairs", 'url': 'https://foxhole.wiki.gg/wiki/Catwalk_Stairs'},
    {'name': "Crane Railway Track", 'url': 'https://foxhole.wiki.gg/wiki/Crane_Railway_Track'},
    {'name': "Deployed Listening Kit", 'url': 'https://foxhole.wiki.gg/wiki/Listening_Kit'},
    {'name': "Deployed Tripod", 'url': 'https://foxhole.wiki.gg/wiki/Tripod'},
    {'name': "Engine Room (Tier 2)", 'url': 'https://foxhole.wiki.gg/wiki/Engine_Room#Tier_2-0'},
    {'name': "Engine Room (Tier 3)", 'url': 'https://foxhole.wiki.gg/wiki/Engine_Room#Tier_3-0'},
    {'name': "Fire Pit", 'url': 'https://foxhole.wiki.gg/wiki/Fire_Pit'},
    {'name': "Foundation (1x1)", 'url': 'https://foxhole.wiki.gg/wiki/Foundation#1x1-0'},
    {'name': "Concrete Foundation (1x1)", 'url': 'https://foxhole.wiki.gg/wiki/Foundation#1x1_Concrete-0'},
    {'name': "Foundation Corner (1x1)", 'url': 'https://foxhole.wiki.gg/wiki/Foundation#Corner_1x1-0'},
    {'name': "Concrete Foundation Corner (1x1)", 'url': 'https://foxhole.wiki.gg/wiki/Foundation#Corner_1x1_Concrete-0'},
    {'name': "Foundation (1x2)", 'url': 'https://foxhole.wiki.gg/wiki/Foundation#1x2-0'},
    {'name': "Concrete Foundation (1x2)", 'url': 'https://foxhole.wiki.gg/wiki/Foundation#1x2_Concrete-0'},
    {'name': "Foundation (2x2)", 'url': 'https://foxhole.wiki.gg/wiki/Foundation#2x2-0'},
    {'name': "Concrete Foundation (2x2)", 'url': 'https://foxhole.wiki.gg/wiki/Foundation#2x2_Concrete-0'},
    {'name': "Fuel Silo", 'url': 'https://foxhole.wiki.gg/wiki/Fuel_Silo'},
    {'name': "Maintenance Tunnel", 'url': 'https://foxhole.wiki.gg/wiki/Maintenance_Tunnel'},
    {'name': "Navy Pier", 'url': 'https://foxhole.wiki.gg/wiki/Navy_Pier'},
    {'name': "Pipeline", 'url': 'https://foxhole.wiki.gg/wiki/Pipeline'},
    {'name': "Pipeline (Overhead)", 'url': 'https://foxhole.wiki.gg/wiki/Pipeline_(Overhead)'},
    {'name': "Pipeline (Underground)", 'url': 'https://foxhole.wiki.gg/wiki/Pipeline_(Underground)'},
    {'name': "Pipeline Valve", 'url': 'https://foxhole.wiki.gg/wiki/Pipeline_Valve'},
    {'name': "Power Pole", 'url': 'https://foxhole.wiki.gg/wiki/Power_Pole'},
    {'name': "Power Switch", 'url': 'https://foxhole.wiki.gg/wiki/Power_Switch'},
    {'name': "Provisional Road", 'url': 'https://foxhole.wiki.gg/wiki/Provisional_Road'},
    {'name': "Railway Track", 'url': 'https://foxhole.wiki.gg/wiki/Railway_Track#Standard-0'},
    {'name': "Railway Track (Biarc)", 'url': 'https://foxhole.wiki.gg/wiki/Railway_Track#Biarc-0'},
    {'name': "Railway Track (Foundation)", 'url': 'https://foxhole.wiki.gg/wiki/Railway_Track#Foundation-0'},
    {'name': "Small Gauge Railway Track", 'url': 'https://foxhole.wiki.gg/wiki/Small_Gauge_Railway_Track#Standard-0'},
    {'name': "Small Gauge Railway Track (Biarc)", 'url': 'https://foxhole.wiki.gg/wiki/Small_Gauge_Railway_Track#Biarc-0'},
    {'name': "Small Gauge Railway Track (Foundation)",'url': 'https://foxhole.wiki.gg/wiki/Small_Gauge_Railway_Track#Foundation-0'},
]
