from src.utils.oisol_enums import FoxholeBuildings

MODULES_CSV_KEYS = {
    'stockpiles': ['region', 'subregion', 'code', 'name', 'type'],
    'register': ['member', 'timer'],
}


NAMES_TO_ACRONYMS = {
    'Assembly Materials I': 'Asmats I',
    'Assembly Materials II': 'Asmats II',
    'Assembly Materials III': 'Asmats III',
    'Assembly Materials IV': 'Asmats IV',
    'Assembly Materials V': 'Asmats V',
    'Construction Materials': 'Cmats',
    'Processed Construction Materials': 'PCmats',
    'Steel Construction Materials': 'SCmats',
    'Unstable Substances': 'Unstable Subs.',
    'Rare Alloys': 'Rare Alloys',
    'Thermal Shielding': 'Thermal Shield.',
    'Naval Hull Segments': 'Naval Hull Seg.',
    'Naval Shell Plating': 'Naval Shell Plat.',
    'Naval Turbine Components': 'Naval Turbine Comp.',
    'A0E-9 Rocket Warhead': 'Rocket Warhead',
    'A0E-9 Rocket Body': 'Rocket Body',
    'A0E-9 Rocket Booster': 'Rocket Booster',
}


EMOJIS_FROM_DICT = {
    'Light Kinetic': '<:light_kinetic:1239343508725174355>',
    'Heavy Kinetic': '<:heavy_kinetic:1239343499787112490>',
    'Anti-Tank Kinetic': '<:AT_kinetic:1239343491138588722>',
    'Anti-Tank Kinetic Structure': '<:AT_kinetic_structure:1316490474479157388>',
    'Anti-Tank Explosive': '<:AT_explosive:1239343415854891071>',
    'Anti-Tank Pillbox': '<:AT_pillbox:1316491732225097770>',
    'Explosive': '<:explosive:1239343451447758878>',
    'High Explosive': '<:high_explosive:1239343441025175583>',
    'Armour Piercing': '<:AP:1239343423807553547>',
    'Demolition': '<:demolition:1239343432367870035>',
    'Shrapnel': '<:shrapnel:1239343483286716417>',
    'Incendiary High Explosive': '<:incendiary:1239343406854049824>',
    'Tracks': '<:tracked:1239349968767291454>',
    'Fuel Tank': '<:fuel_leak:1239349986471313499>',
    'Turret': '<:turret:1239349978170921060>',
    'Second Turret/Cannon': '<:secondary_turret_cannon:1239616804184264818>',
    'Naval Hull Segments': '<:naval_hull_segments:1239559749482188910>',
    'Naval Shell Plating': '<:naval_shell_plating:1239559747921772649>',
    'Naval Turbine Components': '<:naval_turbine_components:1274278845817552986>',
    'Assembly Materials I': '<:asmat1:1239353117120659557>',
    'Assembly Materials II': '<:asmat2:1239353144484302953>',
    'Assembly Materials III': '<:asmat3:1239353124653760584>',
    'Assembly Materials IV': '<:asmat4:1239353135772995584>',
    'Assembly Materials V': '<:asmat5:1239353106404474951>',
    'Refined Materials': '<:rmat:1239353730172715048>',
    'Basic Materials': '<:bmat:1239353181474127943>',
    'Construction Materials': '<:cmat:1239353162616279122>',
    'Processed Construction Materials': '<:pcmat:1239353173488042005>',
    'Steel Construction Materials': '<:scmat:1239353153694994533>',
    'Rare Alloys': '<:rare_alloy:1244071935168741386>',
    'Unstable Substances': '<:unstable_substances:1244071933989879818>',
    'Thermal Shielding': '<:thermal_shielding:1251473216111640586>',
    'LegendLargeShips': '<:large_ship:1239361716777914479>',
    'LegendFacilities': '<:facility:1239361717922828371>',
    'LegendMedical': '<:medical:1239361720288284693>',
    'LegendStructure': '<:intel:1239361723429949461>',
    'LegendArtillery': '<:arty:1239361721324539986>',
    'LegendDefense': '<:defense:1239361722700271727>',
    'LegendOutpost': '<:outpost:1239361719084515329>',
    'Shovel': '<:shovel:1239530825591164930>',
    'Hammer': '<:hammer_tool:1239541780035403849>',
    'Construction Vehicle': '<:cv:1239542192587018240>',
    'Concrete Materials': '<:concrete:1239542632963768400>',
    'Diesel': '<:diesel:1239545026107674714>',
    'Petrol': '<:petrol:1239545022433722469>',
    'Heavy Oil': '<:hoil:1239545024920948756>',
    'Enriched Oil': '<:eoil:1239545023696207952>',
    '7.62mm': '<:7_62mm:1088823887510388959>',
    '7.92mm': '<:7_92mm:1088823653027815424>',
    '9mm': '<:9mm:1088823410412503141>',
    '12.7mm': '<:12_7mm:1088826018883719281>',
    '20mm': '<:20mm:1088826350850281492>',
    '30mm': '<:30mm:1077033326407335956>',
    '40mm': '<:40mm:1077032968310239292>',
    '68mm': '<:68mm:1077033006881063003>',
    '75mm': '<:75mm:1077033155749482546>',
    '94.5mm': '<:94_5mm:1077033020856483880>',
    '120mm': '<:120mm:1239625566655877201>',
    '150mm': '<:150mm:1239625565695119360>',
    '300mm': '<:300mm:1239625564428697640>',
    'Torpedo': '<:torpedo:1239625563057160345>',
    'Depth Charge': '<:depth_charge:1239625562373361737>',
    'RPG': '<:rpg:1088828056073945179>',
    'R.P.G. Shell': '<:rpg:1088828056073945179>',
    'ARC⧸RPG': '<:arcrpg:1088830211799392316>',
    '250mm': '<:250mm:1239630880289329262>',
    '3C-High Explosive Rocket': '<:3c_rocket:1239630879026970655>',
    '4C-Fire Rocket': '<:4c_rocket:1239630881421791313>',
    'Havoc Charge': '<:havoc:1240724687252623400>',
    'Mortar Shell': '<:mortar_shell:1240724693728755864>',
    'Alligator Charge': '<:satchel:1240724690054545479>',
    "Hydra's Whisper": '<:hydras_whisper:1240724688523628565>',
    'Mammon 91-b': '<:mamon:1088827447128109146>',
    'Ignifist 30': '<:ignifist:1088829111859949619>',
    'AP⧸RPG': '<:aprpg:1088829901341212693>',
    'BF5 White Ash Flask Grenade': '<:flask:1088831037766893669>',
    'Anti-Tank Sticky Bomb': '<:sticky:1088831015964909749>',
    'Abisme AT-99': '<:landmine:1088831369762848850>',
    'MapIconTownBase1': '<:townbase_t1:1239654764896321647>',
    'MapIconTownBase2': '<:townbase_t2:1239654763709075591>',
    'MapIconTownBase3': '<:townbase_t3:1239654762576875551>',
    'MapIconBunkerBaseT1': '<:bunkerbase_t1:1239654849490980944>',
    'MapIconBunkerBaseT2': '<:bunkerbase_t2:1239654847918116946>',
    'MapIconBunkerBaseT3': '<:bunkerbase_t3:1239654847175721050>',
    'MapIconBorderBase': '<:borderbase:1239655115913302048>',
    'MapIcon Encampment': '<:encampment:1239655114122203176>',
    'Map Icon Keep': '<:keep:1239655117549211800>',
    'MapIconLiquidTransferStation': '<:lts:1239655346037854239>',
    'MapIconMaterialTransferStation': '<:mts:1239655344666316840>',
    'MapIconResourceTransferStation': '<:rts:1239655343618003065>',
    'MapIconShipyard': '<:shipyard:1239655207353323640>',
    'MapIconConstructionYard': '<:construction_yard:1239655212705251410>',
    'Tech Center Map Icon': '<:tech_center:1239655211161616427>',
    'MapIconMassProductionFactory': '<:mpf:1239655209903456267>',
    'MapIconFactory': '<:factory_building:1239655208485781575>',
    'MapIconManufacturing': '<:refinery:1239656064761200640>',
    'MapIconSeaport': '<:seaport:1239655214059880529>',
    'MapIconStorageFacility': '<:storage_depot:1239655214936752159>',
    'MapIconComponentMine': '<:component_mine:1240332913296281631>',
    'MapIconComponents': '<:component_field:1240332911933391030>',
    'MapIconSulfur': '<:sulfur_field:1240332908846125077>',
    'MapIconSulfurMine': '<:sulfur_mine:1240332910268121108>',
    'MapIconScrap': '<:salvage_field:1240332914571350056>',
    'MapIconScrapMine': '<:salvage_mine:1240332915653742613>',
    'MapIconFuel': '<:oil_field:1240332907181244446>',
    'MapIconCoal': '<:coal_field:1240332917369212940>',
    'MapIconRocketSite': '<:rocket_site:1244068454688886844>',
    'A3 Harpa Fragmentation Grenade': '<:harpa:1088824018653679626>',
    'Tremola Grenade GPb-1': '<:tremola:1088827774787125349>',
    'PT-815 Smoke Grenade': '<:smoke:1239713145375948840>',
    'Green Ash Grenade': '<:gas:1239713326720880740>',
    'Sea Mine': '<:sea_mine:1244048778063773716>',
    'A0E-9 Rocket Warhead': '<:rocket_warhead:1244069007347286046>',
    'A0E-9 Rocket Body': '<:rocket_body:1244069016541069464>',
    'A0E-9 Rocket Booster': '<:rocket_booster:1244069024996786238>',
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

# All regions and their subregions
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
    'Oarbreaker Isles': ['Fort Fogwood', 'Gold', 'Grisly Refuge', 'Integrum', 'Partisan Island', 'Posterus', 'Silver', 'The Conclave', 'The Dirk'],
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
    'Tempest Island': ['Blackwatch', 'Isle of Psyche', "Liar's Heaven", 'Plana Fada', 'Reef', 'Surge Gate', 'The Gale', 'The Iris', 'The Rush'],
    'Terminus': ['Bloody Palm Fort', 'Cerberus Wake', 'Therizó', 'Thunderbolt', "Warlord's Stead", 'Winding Bolas'],
    'The Fingers': ["Captain's Dread", 'Fort Barley', "Headsman's Villa", 'Plankhouse', 'Second Man', 'Tethys Base', 'The Old Captain', 'The Tusk', 'Titancall'],
    'The Moors': ['Borderlane', "Gravekeeper's Holdfast", 'Headstone', "Luch's Workshop", 'MacConmara Barrows', "Morrighan's Grave", 'Ogmaran', 'Reaching River', 'The Cut', 'The Spade', 'The Wind Hills', 'Wiccwalk'],
    'Umbral Wildwood': ['Amethyst', "Atropos' Fate", "Clotho's Refuge", 'GoldenRoot Ranch', "Hermit's Rest", "Lachesis' Tally ", 'Sentry', 'Stray', 'The Foundry', 'Thunderfoot', 'Vagrant Bastion'],
    'Viper Pit': ['Blackthroat', 'Earl Crowley', 'Fleck Crossing', 'Fort Viper', 'Kirknell', 'Moltworth', "Serenity's Blight", 'The Friars'],
    'Weathered Expanse': ["Crow's Nest", 'Foxcatcher', 'Frostmarch', 'Huntsfort', 'Necropolis', 'Shattered Advance', 'Spirit Watch', 'The Weathering Halls', 'Wightwalk'],
    'Westgate': ['Holdfast', 'Kingstone', 'Longstone', "Lord's Mouth", 'Lost Partition', "Rancher's Fast", 'The Gallows', 'Westgate Keep', 'Wyattwick', "Zeus' Demise"]
}

# All regions and their subregions with depot / seaport
REGIONS_STOCKPILES = {
    'Acrithia': [('Legion Ranch', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Thetus Ring', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Patridia', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Allods Bight': [('Scurvyshire', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ("Mercy's Wail", FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Ash Fields': [('Electi', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Ashtown', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Basin Sionnach': [('Sess', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Den', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Cuttail Station', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Callahans Passage': [('Solas Gorge', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Lochan Berth', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Callums Cape': [('Holdout', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ("Callum's Keep", FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Clahstra': [('East Narthex', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Third Chapter', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Treasury', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value)],
    'Clanshead Valley': [('The Pike', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The King', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Deadlands': [('Abandoned Ward', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Brine Glen', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ("Callahan's Gate", FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Salt Farms', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Spine', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value)],
    'Drowned Vale': [('Loggerhead', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Baths', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Endless Shore': [('Brackish Point', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Iron Junction', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Tuatha Watchpost', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Saltbrook Channel', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Farranac Coast': [('Mara', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Bone Haft', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Pleading Wharf', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Victa', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Jade Cove', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Fishermans Row': [('Arcadia', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Black Well', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Eidolo', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Godcrofts': [('Isawa', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value), ('The Axehead', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Great March': [('Sitaria', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Violethome', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value)],
    'Heartlands': [('Greenfield Orchard', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Blemish', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value)],
    'Howl County': [('Hungry Wolf', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Little Lamb', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Great Warden Dam', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Kalokai': [('Hallow', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Sweethearth', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Baccae Ridge', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Kings Cage': [('Gibbet Fields', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Manacle', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Linn Mercy': [('The Prairie Bazaar', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Ulster Falls', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Loch Mor': [("Mercy's Wish", FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Feirmor', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Marban Hollow': [('Lockheed', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ("Maiden's Veil", FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Morgens Crossing': [('Allsight', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Lividus', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Quietus', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Nevish Line': [('Blackcoat Way', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Mistle Shrine', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Scrying Belt', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Oarbreaker Isles': [('Integrum', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value), ('The Conclave', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Origin': [('Finis', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Teichotima', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Initium', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Reaching Trail': [('Brodytown', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Reprieve', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value)],
    'Reavers Pass': [('Breakwater', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Scuttletown', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Keelhaul', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Red River': [('Judicium', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Penance', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Cannonsmoke', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Sableport': [('Barronhome', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Cinderwick', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ("Light's End", FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Shackled Chasm': [('Savages', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Silk Farms', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Speaking Woods': [('Sotto Bank', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Filament', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Tine', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Stema Landing': [('Alchimio Estate', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value), ('The Spearhead', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Stlican Shelf': [('Cavilltown', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Vulpine Watch', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Port of Rime', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Stonecradle': [('Fading Lights', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Buckler Sound', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Tempest Island': [("Liar's Heaven", FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Rush', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Iris', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Terminus': [("Warlord's Stead", FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Therizó', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'The Fingers': [("Headsman's Villa", FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value), ('The Old Captain', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'The Moors': [("Morrighan's Grave", FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Ogmaran', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Umbral Wildwood': [("Hermit's Rest", FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Thunderfoot', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Viper Pit': [('Earl Crowley', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Kirknell', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Weathered Expanse': [("Crow's Nest", FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Foxcatcher', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Weathering Halls', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)],
    'Westgate': [('Kingstone', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('The Gallows', FoxholeBuildings.STORAGE_DEPOT_NEUTRAL.value, FoxholeBuildings.STORAGE_DEPOT_WARDEN.value, FoxholeBuildings.STORAGE_DEPOT_COLONIAL.value), ('Longstone', FoxholeBuildings.SEAPORT_NEUTRAL.value, FoxholeBuildings.SEAPORT_WARDEN.value, FoxholeBuildings.SEAPORT_COLONIAL.value)]
}

ITEMS_WIKI_ENTRIES = [
    {
        "name": "Argenti r.II Rifle",
        "url": "https://foxhole.wiki.gg/wiki/Argenti_r.II_Rifle",
        "keywords": {'argenti', 'colonial', 'rifle'}
    },
    {
        "name": "Blakerow 871",
        "url": "https://foxhole.wiki.gg/wiki/Blakerow_871",
        "keywords": {'blakerow', 'warden', 'rifle'}
    },
    {
        "name": "Catena rt.IV Auto-Rifle",
        "url": "https://foxhole.wiki.gg/wiki/Catena_rt.IV_Auto-Rifle",
        "keywords": {'catena', 'colonial', 'auto', 'rifle'}
    },
    {
        "name": "Fuscina pi.I",
        "url": "https://foxhole.wiki.gg/wiki/Fuscina_pi.I",
        "keywords": {'fuscina', 'fucina', 'colonial', 'rifle', 'fusina'}
    },
    {
        "name": "No.2 Loughcaster",
        "url": "https://foxhole.wiki.gg/wiki/No.2_Loughcaster",
        "keywords": {'warden', 'loughcaster', 'rifle'}
    },
    {
        "name": "No.2B Hawthorne",
        "url": "https://foxhole.wiki.gg/wiki/No.2B_Hawthorne",
        "keywords": {'warden', 'hawthorne', 'rifle'}
    },
    {
        "name": "Sampo Auto-Rifle 77",
        "url": "https://foxhole.wiki.gg/wiki/Sampo_Auto-Rifle_77",
        "keywords": {'sampo', 'rifle', 'warden', 'auto'}
    },
    {
        "name": "The Hangman 757",
        "url": "https://foxhole.wiki.gg/wiki/The_Hangman_757",
        "keywords": {'the', 'rifle', 'heavy', 'hangman', 'warden'}
    },
    {
        "name": "Volta r.I Repeater",
        "url": "https://foxhole.wiki.gg/wiki/Volta_r.I_Repeater",
        "keywords": {'repeater', 'colonial', 'rifle', 'volta', 'heavy'}
    },
    {
        "name": "Clancy Cinder M3",
        "url": "https://foxhole.wiki.gg/wiki/Clancy_Cinder_M3",
        "keywords": {'cinder', 'long', 'rifle', 'clancy', 'warden'}
    },
    {
        "name": "KRR2-790 Omen",
        "url": "https://foxhole.wiki.gg/wiki/KRR2-790_Omen",
        "keywords": {'omen', 'colonial', 'long', 'rifle'}
    },
    {
        "name": "Clancy-Raca M4",
        "url": "https://foxhole.wiki.gg/wiki/Clancy-Raca_M4",
        "keywords": {'rifle', 'clancy', 'raca', 'sniper', 'warden'}
    },
    {
        "name": "KRR3-792 Auger",
        "url": "https://foxhole.wiki.gg/wiki/KRR3-792_Auger",
        "keywords": {'auger', 'colonial', 'rifle', 'sniper'}
    },
    {
        "name": "“Lionclaw” mc.VIII",
        "url": "https://foxhole.wiki.gg/wiki/%E2%80%9CLionclaw%E2%80%9D_mc.VIII",
        "keywords": {'submachine', 'colonial', 'gun', 'lionclaw'}
    },
    {
        "name": "“The Pitch Gun” mc.V",
        "url": "https://foxhole.wiki.gg/wiki/%E2%80%9CThe_Pitch_Gun%E2%80%9D_mc.V",
        "keywords": {'submachine', 'colonial', 'gun', 'pitch'}
    },
    {
        "name": "Fiddler Submachine Gun Model 868",
        "url": "https://foxhole.wiki.gg/wiki/Fiddler_Submachine_Gun_Model_868",
        "keywords": {'fiddler', 'submachine', 'warden', 'gun'}
    },
    {
        "name": "No.1 “The Liar” Submachine Gun",
        "url": "https://foxhole.wiki.gg/wiki/No.1_%E2%80%9CThe_Liar%E2%80%9D_Submachine_Gun",
        "keywords": {'liar', 'warden', 'gun', 'submachine'}
    },
    {
        "name": "“Dusk” ce.III",
        "url": "https://foxhole.wiki.gg/wiki/%E2%80%9CDusk%E2%80%9D_ce.III",
        "keywords": {'dusk', 'colonial', 'assault', 'rifle'}
    },
    {
        "name": "Aalto Storm Rifle 24",
        "url": "https://foxhole.wiki.gg/wiki/Aalto_Storm_Rifle_24",
        "keywords": {'storm', 'assault', 'aalto', 'rifle', 'warden'}
    },
    {
        "name": "Booker Storm Rifle Model 838",
        "url": "https://foxhole.wiki.gg/wiki/Booker_Storm_Rifle_Model_838",
        "keywords": {'storm', 'assault', 'rifle', 'warden', 'booker'}
    },
    {
        "name": "KRF1-750 Dragonfly",
        "url": "https://foxhole.wiki.gg/wiki/KRF1-750_Dragonfly",
        "keywords": {'shotgun', 'dragonfly', 'colonial'}
    },
    {
        "name": "No.4 The Pillory Scattergun",
        "url": "https://foxhole.wiki.gg/wiki/No.4_The_Pillory_Scattergun",
        "keywords": {'shotgun', 'warden', 'scattergun', 'pillory'}
    },
    {
        "name": "Ahti Model 2",
        "url": "https://foxhole.wiki.gg/wiki/Ahti_Model_2",
        "keywords": {'pistol', 'warden', 'ati', 'ahti'}
    },
    {
        "name": "Cascadier 873",
        "url": "https://foxhole.wiki.gg/wiki/Cascadier_873",
        "keywords": {'pistol', 'warden', 'cascadier'}
    },
    {
        "name": "Ferro 879",
        "url": "https://foxhole.wiki.gg/wiki/Ferro_879",
        "keywords": {'pistol', 'colonial', 'ferro'}
    },
    {
        "name": "Cometa T2-9",
        "url": "https://foxhole.wiki.gg/wiki/Cometa_T2-9",
        "keywords": {'pistol', 'revolver', 'cometa'}
    },
    {
        "name": "Catara mo.II",
        "url": "https://foxhole.wiki.gg/wiki/Catara_mo.II",
        "keywords": {'light', 'colonial', 'catara', 'gun', 'machine', 'lmg'}
    },
    {
        "name": "KRN886-127 Gast Machine Gun",
        "url": "https://foxhole.wiki.gg/wiki/KRN886-127_Gast_Machine_Gun",
        "keywords": {'colonial', 'mg', 'gun', 'machine', 'gast'}
    },
    {
        "name": "Malone MK.2",
        "url": "https://foxhole.wiki.gg/wiki/Malone_MK.2",
        "keywords": {'malone', 'mg', 'warden', 'gun', 'machine'}
    },
    {
        "name": "20 Neville Anti-Tank Rifle",
        "url": "https://foxhole.wiki.gg/wiki/20_Neville_Anti-Tank_Rifle",
        "keywords": {'atr', 'neville', 'tank', 'rifle', 'warden', 'anti'}
    },
    {
        "name": "228 Satterley Heavy Storm Rifle",
        "url": "https://foxhole.wiki.gg/wiki/228_Satterley_Heavy_Storm_Rifle",
        "keywords": {'storm', 'atr', 'tank', 'rifle', 'scatterley', 'heavy', 'warden', 'anti'}
    },
    {
        "name": "Booker Greyhound Model 910",
        "url": "https://foxhole.wiki.gg/wiki/Booker_Greyhound_Model_910",
        "keywords": {'storm', 'atr', 'tank', 'rifle', 'warden', 'anti', 'booker'}
    },
    {
        "name": "“Dawn” Ve.II",
        "url": "https://foxhole.wiki.gg/wiki/%E2%80%9CDawn%E2%80%9D_Ve.II",
        "keywords": {'atr', 'tank', 'colonial', 'rifle', 'dawn', 'anti'}
    },
    {
        "name": "“Quickhatch” Rt.I",
        "url": "https://foxhole.wiki.gg/wiki/%E2%80%9CQuickhatch%E2%80%9D_Rt.I",
        "keywords": {'atr', 'quickhatch', 'tank', 'colonial', 'rifle', 'sniper', 'anti'}
    },
    {
        "name": "Lamentum mm.IV",
        "url": "https://foxhole.wiki.gg/wiki/Lamentum_mm.IV",
        "keywords": {'colonial', 'mg', 'gun', 'mounted', 'lamentum', 'machine'}
    },
    {
        "name": "Malone Ratcatcher MK.1",
        "url": "https://foxhole.wiki.gg/wiki/Malone_Ratcatcher_MK.1",
        "keywords": {'ratcatcher', 'malone', 'mg', 'warden', 'gun', 'mounted', 'machine'}
    },
    {
        "name": "Mounted Fissura gd.I",
        "url": "https://foxhole.wiki.gg/wiki/Mounted_Fissura_gd.I",
        "keywords": {'colonial', 'grenade', 'mounted', 'fissura', 'launcher'}
    },
    {
        "name": "Daucus isg.III",
        "url": "https://foxhole.wiki.gg/wiki/Daucus_isg.III",
        "keywords": {'colonial', 'support', 'mounted', 'daucus', 'gun', 'infantry', 'isg'}
    },
    {
        "name": "Cutler Foebreaker",
        "url": "https://foxhole.wiki.gg/wiki/Cutler_Foebreaker",
        "keywords": {'rpg', 'warden', 'mounted', 'cutler', 'foebreaker', 'launcher'}
    },
    {
        "name": "Mounted Bonesaw MK.3",
        "url": "https://foxhole.wiki.gg/wiki/Mounted_Bonesaw_MK.3",
        "keywords": {'rpg', 'bonesaw', 'warden', 'mounted', 'arc', 'launcher'}
    },
    {
        "name": "“Typhon” ra.XII",
        "url": "https://foxhole.wiki.gg/wiki/%E2%80%9CTyphon%E2%80%9D_ra.XII",
        "keywords": {'atr', 'tank', 'colonial', 'rifle', 'mounted', 'anti', 'typhon'}
    },
    {
        "name": "“Molten Wind” v.II Flame Torch",
        "url": "https://foxhole.wiki.gg/wiki/%E2%80%9CMolten_Wind%E2%80%9D_v.II_Flame_Torch",
        "keywords": {'torch', 'colonial', 'thrower', 'molten', 'flame', 'flamethrower', 'wind'}
    },
    {
        "name": "Willow's Bane Model 845",
        "url": "https://foxhole.wiki.gg/wiki/Willow%27s_Bane_Model_845",
        "keywords": {'thrower', 'model', 'bane', 'flamethrower', 'warden', 'flame', 'willow'}
    },
    {
        "name": "A3 Harpa Fragmentation Grenade",
        "url": "https://foxhole.wiki.gg/wiki/A3_Harpa_Fragmentation_Grenade",
        "keywords": {'grenade', 'a3', 'warden', 'fragmentation', 'harpa'}
    },
    {
        "name": "Bomastone Grenade",
        "url": "https://foxhole.wiki.gg/wiki/Bomastone_Grenade",
        "keywords": {'colonial', 'grenade', 'bomastone'}
    },
    {
        "name": "Green Ash Grenade",
        "url": "https://foxhole.wiki.gg/wiki/Gas_Grenade",
        "keywords": {'gas', 'grenade', 'ash', 'green'}
    },
    {
        "name": "PT-815 Smoke Grenade",
        "url": "https://foxhole.wiki.gg/wiki/Smoke_Grenade",
        "keywords": {'smoke', 'grenade'}
    },
    {
        "name": "Mammon 91-b",
        "url": "https://foxhole.wiki.gg/wiki/Mammon_91-b",
        "keywords": {'he', 'mammon', 'grenade', 'mamon'}
    },
    {
        "name": "Tremola Grenade GPb-1",
        "url": "https://foxhole.wiki.gg/wiki/Tremola_Grenade_GPb-1",
        "keywords": {'he', 'grenade', 'tremola'}
    },
    {
        "name": "Anti-Tank Sticky Bomb",
        "url": "https://foxhole.wiki.gg/wiki/Anti-Tank_Sticky_Bomb",
        "keywords": {'anti', 'tank', 'sticky', 'bomb'}
    },
    {
        "name": "BF5 White Ash Flask Grenade",
        "url": "https://foxhole.wiki.gg/wiki/BF5_White_Ash_Flask_Grenade",
        "keywords": {'tank', 'grenade', 'flask', 'white', 'warden', 'ash', 'anti'}
    },
    {
        "name": "B2 Varsi Anti-Tank Grenade",
        "url": "https://foxhole.wiki.gg/wiki/B2_Varsi_Anti-Tank_Grenade",
        "keywords": {'tank', 'grenade', 'warden', 'varsi', 'anti'}
    },
    {
        "name": "Alligator Charge",
        "url": "https://foxhole.wiki.gg/wiki/Alligator_Charge",
        "keywords": {'aligator', 'charge', 'alligator', 'warden', 'explosive'}
    },
    {
        "name": "Hydra's Whisper",
        "url": "https://foxhole.wiki.gg/wiki/Hydra%27s_Whisper",
        "keywords": {'whisper', 'colonial', 'charge', 'hydra', 'explosive'}
    },
    {
        "name": "Havoc Charge",
        "url": "https://foxhole.wiki.gg/wiki/Havoc_Charge",
        "keywords": {'explosive', 'charge', 'havoc'}
    },
    {
        "name": "Abisme AT-99",
        "url": "https://foxhole.wiki.gg/wiki/Abisme_AT-99",
        "keywords": {'abisme', 'tank', 'anti', 'at', 'mine'}
    },
    {
        "name": "E680-S Rudder Lock",
        "url": "https://foxhole.wiki.gg/wiki/Sea_Mine",
        "keywords": {'rudder', 'sea', 'naval', 'lock', 'mine'}
    },
    {
        "name": "Crow's Foot Mine",
        "url": "https://foxhole.wiki.gg/wiki/Crow%27s_Foot_Mine",
        "keywords": {'personnel', 'crow', 'land', 'infantry', 'foot', 'anti', 'mine'}
    },
    {
        "name": "The Ospreay",
        "url": "https://foxhole.wiki.gg/wiki/The_Ospreay",
        "keywords": {'grenade', 'warden', 'ospreay', 'launcher'}
    },
    {
        "name": "KLG901-2 Lunaire F",
        "url": "https://foxhole.wiki.gg/wiki/KLG901-2_Lunaire_F",
        "keywords": {'lunaire', 'colonial', 'grenade', 'launcher'}
    },
    {
        "name": "Cutler Launcher 4",
        "url": "https://foxhole.wiki.gg/wiki/Cutler_Launcher_4",
        "keywords": {'rpg', 'cutler', 'warden', 'launcher'}
    },
    {
        "name": "Bane 45",
        "url": "https://foxhole.wiki.gg/wiki/Bane_45",
        "keywords": {'tank', 'rpg', 'colonial', 'bane', 'anti', 'at', 'ap', 'launcher'}
    },
    {
        "name": "Bonesaw MK.3",
        "url": "https://foxhole.wiki.gg/wiki/Bonesaw_MK.3",
        "keywords": {'rpg', 'bonesaw', 'warden', 'arc', 'launcher'}
    },
    {
        "name": "Ignifist 30",
        "url": "https://foxhole.wiki.gg/wiki/Ignifist_30",
        "keywords": {'colonial', 'ignifist', 'at', 'launcher'}
    },
    {
        "name": "Venom c.II 35",
        "url": "https://foxhole.wiki.gg/wiki/Venom_c.II_35",
        "keywords": {'rpg', 'colonial', 'ap', 'at', 'venom', 'launcher'}
    },
    {
        "name": "Cremari Mortar",
        "url": "https://foxhole.wiki.gg/wiki/Cremari_Mortar",
        "keywords": {'mortar', 'cremari'}
    },
    {
        "name": "Buckhorn CCQ-18",
        "url": "https://foxhole.wiki.gg/wiki/Bayonet",
        "keywords": {'buckhorn', 'bayonet'}
    },
    {
        "name": "Fists",
        "url": "https://foxhole.wiki.gg/wiki/Fists",
        "keywords": {'fists'}
    },
    {
        "name": "Eleos Infantry Dagger",
        "url": "https://foxhole.wiki.gg/wiki/Eleos_Infantry_Dagger",
        "keywords": {'colonial', 'dagger', 'melee', 'infantry', 'weapon', 'eleos'}
    },
    {
        "name": "Falias Raiding Club",
        "url": "https://foxhole.wiki.gg/wiki/Falias_Raiding_Club",
        "keywords": {'falias', 'raiding', 'melee', 'warden', 'weapon', 'club'}
    },
    {
        "name": "9mm",
        "url": "https://foxhole.wiki.gg/wiki/9mm",
        "keywords": {'magazine', '9', 'mm'}
    },
    {
        "name": "8mm",
        "url": "https://foxhole.wiki.gg/wiki/8mm",
        "keywords": {'magazine', '8', 'mm'}
    },
    {
        "name": "7.92mm",
        "url": "https://foxhole.wiki.gg/wiki/7.92mm",
        "keywords": {'magazine', '7', '7.92' 'mm'}
    },
    {
        "name": "7.62mm",
        "url": "https://foxhole.wiki.gg/wiki/7.62mm",
        "keywords": {'magazine', '7', '7.62', 'mm'}
    },
    {
        "name": ".44",
        "url": "https://foxhole.wiki.gg/wiki/.44",
        "keywords": {'44', 'magazine', 'mm'}
    },
    {
        "name": "Buckshot",
        "url": "https://foxhole.wiki.gg/wiki/Buckshot",
        "keywords": {'shotgun', 'buckshot', 'ammo'}
    },
    {
        "name": "Flame Ammo",
        "url": "https://foxhole.wiki.gg/wiki/Flame_Ammo",
        "keywords": {'flame', 'ammo'}
    },
    {
        "name": "12.7mm",
        "url": "https://foxhole.wiki.gg/wiki/12.7mm",
        "keywords": {'magazine', '12.7', '12', 'mm'}
    },
    {
        "name": "20mm",
        "url": "https://foxhole.wiki.gg/wiki/20mm",
        "keywords": {'magazine', '20', 'mm'}
    },
    {
        "name": "30mm",
        "url": "https://foxhole.wiki.gg/wiki/30mm",
        "keywords": {'30', 'shell', 'mm'}
    },
    {
        "name": "40mm",
        "url": "https://foxhole.wiki.gg/wiki/40mm",
        "keywords": {'40', 'shell', 'mm'}
    },
    {
        "name": "68mm",
        "url": "https://foxhole.wiki.gg/wiki/68mm",
        "keywords": {'shell', '68', 'mm'}
    },
    {
        "name": "75mm",
        "url": "https://foxhole.wiki.gg/wiki/75mm",
        "keywords": {'shell', '75', 'mm'}
    },
    {
        "name": "94.5mm",
        "url": "https://foxhole.wiki.gg/wiki/94.5mm",
        "keywords": {'94.5', 'shell', '94', 'mm'}
    },
    {
        "name": "Flare Mortar Shell",
        "url": "https://foxhole.wiki.gg/wiki/Flare_Mortar_Shell",
        "keywords": {'mortar', 'shell', 'flare'}
    },
    {
        "name": "Shrapnel Mortar Shell",
        "url": "https://foxhole.wiki.gg/wiki/Shrapnel_Mortar_Shell",
        "keywords": {'shrapnel', 'mortar', 'shell'}
    },
    {
        "name": "Mortar Shell",
        "url": "https://foxhole.wiki.gg/wiki/Mortar_Shell",
        "keywords": {'mortar', 'shell'}
    },
    {
        "name": "Incendiary Mortar Shell",
        "url": "https://foxhole.wiki.gg/wiki/Incendiary_Mortar_Shell",
        "keywords": {'mortar', 'fire', 'shell', 'incendiary'}
    },
    {
        "name": "4C-Fire Rocket",
        "url": "https://foxhole.wiki.gg/wiki/4C-Fire_Rocket",
        "keywords": {'4c', 'fire', 'rocket'}
    },
    {
        "name": "3C-High Explosive Rocket",
        "url": "https://foxhole.wiki.gg/wiki/3C-High_Explosive_Rocket",
        "keywords": {'high', 'rocket', 'fire', 'explosive', '3c'}
    },
    {
        "name": "120mm",
        "url": "https://foxhole.wiki.gg/wiki/120mm",
        "keywords": {'shell', '120', 'mm'}
    },
    {
        "name": "150mm",
        "url": "https://foxhole.wiki.gg/wiki/150mm",
        "keywords": {'150', 'shell', 'mm'}
    },
    {
        "name": "300mm",
        "url": "https://foxhole.wiki.gg/wiki/300mm",
        "keywords": {'300', 'shell', 'mm'}
    },
    {
        "name": "RPG",
        "url": "https://foxhole.wiki.gg/wiki/RPG",
        "keywords": {'rpg', 'shell'}
    },
    {
        "name": "AP⧸RPG",
        "url": "https://foxhole.wiki.gg/wiki/AP%E2%A7%B8RPG",
        "keywords": {'rpg', 'ap', 'shell'}
    },
    {
        "name": "ARC⧸RPG",
        "url": "https://foxhole.wiki.gg/wiki/ARC%E2%A7%B8RPG",
        "keywords": {'rpg', 'arc', 'shell'}
    },
    {
        "name": "250mm",
        "url": "https://foxhole.wiki.gg/wiki/250mm",
        "keywords": {'shell', '250', 'mm'}
    },
    {
        "name": "“Molten Wind” v.II Ammo",
        "url": "https://foxhole.wiki.gg/wiki/%E2%80%9CMolten_Wind%E2%80%9D_v.II_Ammo",
        "keywords": {'ammo', 'molten', 'flame', 'wind'}
    },
    {
        "name": "Willow's Bane Ammo",
        "url": "https://foxhole.wiki.gg/wiki/Willow%27s_Bane_Ammo",
        "keywords": {'willows', 'flame', 'ammo', 'bane'}
    },
    {
        "name": "Moray Torpedo",
        "url": "https://foxhole.wiki.gg/wiki/Torpedo",
        "keywords": {'torpedo', 'moray'}
    },
    {
        "name": "Model-7 “Evie”",
        "url": "https://foxhole.wiki.gg/wiki/Depth_Charge",
        "keywords": {'evie', 'charge', 'depth'}
    },
    {
        "name": "Herne QMW 1a Scourge Hunter",
        "url": "https://foxhole.wiki.gg/wiki/Herne_QMW_1a_Scourge_Hunter",
        "keywords": {'hunter', 'mecha', 'scourge', 'herne'}
    },
    {
        "name": "Centurion MV-2",
        "url": "https://foxhole.wiki.gg/wiki/Centurion_MV-2",
        "keywords": {'mecha', 'centurion'}
    },
    {
        "name": "Heavy Infantry Carrier",
        "url": "https://foxhole.wiki.gg/wiki/Heavy_Infantry_Carrier",
        "keywords": {'carrier', 'relic', 'heavy', 'vehicle', 'infantry'}
    },
    {
        "name": "Oil Field",
        "url": "https://foxhole.wiki.gg/wiki/Oil_Field",
        "keywords": {'field', 'oil'}
    },
    {
        "name": "Coal Field",
        "url": "https://foxhole.wiki.gg/wiki/Coal_Field",
        "keywords": {'coal', 'field'}
    },
    {
        "name": "Salvage Field",
        "url": "https://foxhole.wiki.gg/wiki/Salvage_Field",
        "keywords": {'scrap', 'field', 'salvage'}
    },
    {
        "name": "Sulfur Field",
        "url": "https://foxhole.wiki.gg/wiki/Sulfur_Field",
        "keywords": {'field', 'sulfur'}
    },
    {
        "name": "Component Field",
        "url": "https://foxhole.wiki.gg/wiki/Component_Field",
        "keywords": {'component', 'field'}
    },
    {
        "name": "A0E-9 Rocket Booster",
        "url": "https://foxhole.wiki.gg/wiki/A0E-9_Rocket_Booster",
        "keywords": {'booster', 'rocket', 'nuke'}
    },
    {
        "name": "A0E-9 Rocket Body",
        "url": "https://foxhole.wiki.gg/wiki/A0E-9_Rocket_Body",
        "keywords": {'rocket', 'body', 'nuke'}
    },
    {
        "name": "A0E-9 Rocket Warhead",
        "url": "https://foxhole.wiki.gg/wiki/A0E-9_Rocket_Warhead",
        "keywords": {'warhead', 'rocket', 'nuke'}
    },
    {
        "name": "A0E-9 Rocket Platform",
        "url": "https://foxhole.wiki.gg/wiki/A0E-9_Rocket_Platform",
        "keywords": {'rocket', 'platform', 'nuke'}
    },
    {
        "name": "Diesel Power Plant",
        "url": "https://foxhole.wiki.gg/wiki/Diesel_Power_Plant",
        "keywords": {'diesel', 'power', 'plant'}
    },
    {
        "name": "Power Station",
        "url": "https://foxhole.wiki.gg/wiki/Power_Station",
        "keywords": {'station', 'power'}
    },
    # TRIPODS
    {
        "name": "Deployed Listening Kit",
        "url": "https://foxhole.wiki.gg/wiki/Listening_Kit",
        "keywords": {'deployed', 'kit', 'listening', 'lk'}
    },
    {
        "name": "Tripod",
        "url": "https://foxhole.wiki.gg/wiki/Tripod",
        "keywords": {'tripod'}
    },
]

VEHICLES_WIKI_ENTRIES = [
    {
        "name": "T3 “Xiphos”",
        "url": "https://foxhole.wiki.gg/wiki/T3_%E2%80%9CXiphos%E2%80%9D",
        "keywords": {'t3', 'xiphos', 'ac', 'colonial', 'car', 'armored', 'armoured'}
    },
    {
        "name": "T5 “Percutio”",
        "url": "https://foxhole.wiki.gg/wiki/T5_%E2%80%9CPercutio%E2%80%9D",
        "keywords": {'colonial', 'percutio', 'car', 'armored', 't5', 'atac', 'armoured'}
    },
    {
        "name": "T8 “Gemini”",
        "url": "https://foxhole.wiki.gg/wiki/T8_%E2%80%9CGemini%E2%80%9D",
        "keywords": {'gemini', 'ac', 't8', 'colonial', 'car', 'armored', 'armoured'}
    },
    {
        "name": "O'Brien V.110",
        "url": "https://foxhole.wiki.gg/wiki/O%27Brien_V.110",
        "keywords": {'110', 'obrien', 'ac', 'warden', 'car', 'armored', 'armoured'}
    },
    {
        "name": "O'Brien V.113 Gravekeeper",
        "url": "https://foxhole.wiki.gg/wiki/O%27Brien_V.113_Gravekeeper",
        "keywords": {'obrien', 'ac', 'bonewagon', 'warden', 'car', 'gravekeeper', 'amored', '113', 'armoured'}
    },
    {
        "name": "O'Brien V.121 Highlander",
        "url": "https://foxhole.wiki.gg/wiki/O%27Brien_V.121_Highlander",
        "keywords": {'obrien', 'highlander', 'warden', 'car', '121', 'tac', 'amored', 'armoured'}
    },
    {
        "name": "O'Brien V.130 Wild Jack",
        "url": "https://foxhole.wiki.gg/wiki/O%27Brien_V.130_Wild_Jack",
        "keywords": {'wildjack', 'flame', 'obrien', 'ac', 'warden', '130', 'car', 'armored', 'armoured'}
    },
    {
        "name": "O'Brien V.190 Knave",
        "url": "https://foxhole.wiki.gg/wiki/O%27Brien_V.190_Knave",
        "keywords": {'obrien', '190', 'warden', 'knave', 'car', 'gac', 'armored', 'glac'}
    },
    {
        "name": "O'Brien V.101 Freeman",
        "url": "https://foxhole.wiki.gg/wiki/O%27Brien_V.101_Freeman",
        "keywords": {'hac', 'obrien', 'warden', 'car', 'freeman', 'armored', '101', 'armoured'}
    },
    {
        "name": "T12 “Actaeon” Tankette",
        "url": "https://foxhole.wiki.gg/wiki/T12_%E2%80%9CActaeon%E2%80%9D_Tankette",
        "keywords": {'t12', 'tankette', 'actaeon', 'colonial'}
    },
    {
        "name": "T13 “Deioneus” Rocket Battery",
        "url": "https://foxhole.wiki.gg/wiki/T13_%E2%80%9CDeioneus%E2%80%9D_Rocket_Battery",
        "keywords": {'rocket', 'tankette', 'deioneus', 'colonial', 't13', 'battery'}
    },
    {
        "name": "T14 “Vesta” Tankette",
        "url": "https://foxhole.wiki.gg/wiki/T14_%E2%80%9CVesta%E2%80%9D_Tankette",
        "keywords": {'tankette', 'vesta', 'flame', 'colonial', 't14'}
    },
    {
        "name": "T20 “Ixion” Tankette",
        "url": "https://foxhole.wiki.gg/wiki/T20_%E2%80%9CIxion%E2%80%9D_Tankette",
        "keywords": {'tankette', 'ixion', 'colonial', 't20', '30mm'}
    },
    {
        "name": "AB-8 “Acheron”",
        "url": "https://foxhole.wiki.gg/wiki/AB-8_%E2%80%9CAcheron%E2%80%9D",
        "keywords": {'ab8', 'apc', 'acheron', 'colonial'}
    },
    {
        "name": "AB-11 “Doru”",
        "url": "https://foxhole.wiki.gg/wiki/AB-11_%E2%80%9CDoru%E2%80%9D",
        "keywords": {'apc', 'ab11', 'colonial', 'doru', '12.7', 'mm'}
    },
    {
        "name": "Mulloy LPC",
        "url": "https://foxhole.wiki.gg/wiki/Mulloy_LPC",
        "keywords": {'apc', 'lpc', 'mulloy', 'warden'}
    },
    {
        "name": "HH-a “Javelin”",
        "url": "https://foxhole.wiki.gg/wiki/HH-a_%E2%80%9CJavelin%E2%80%9D",
        "keywords": {'ht', 'colonial', 'javelin', 'halftrack'}
    },
    {
        "name": "HH-b “Hoplite”",
        "url": "https://foxhole.wiki.gg/wiki/HH-b_%E2%80%9CHoplite%E2%80%9D",
        "keywords": {'ht', 'colonial', 'hoplite', 'halftrack'}
    },
    {
        "name": "HH-d “Peltast”",
        "url": "https://foxhole.wiki.gg/wiki/HH-d_%E2%80%9CPeltast%E2%80%9D",
        "keywords": {'mht', 'colonial', 'mortart', 'peltast', 'halftrack'}
    },
    {
        "name": "Niska Mk. I Gun Motor Carriage",
        "url": "https://foxhole.wiki.gg/wiki/Niska_Mk._I_Gun_Motor_Carriage",
        "keywords": {'motor', 'ht', 'warden', 'halftrack', 'niska', 'gun', 'carriage'}
    },
    {
        "name": "Niska Mk. II Blinder",
        "url": "https://foxhole.wiki.gg/wiki/Niska_Mk._II_Blinder",
        "keywords": {'atht', 'blinder', '68mm', 'warden', 'niska', 'halftrack'}
    },
    {
        "name": "Niska Mk. III Scar Twin",
        "url": "https://foxhole.wiki.gg/wiki/Niska_Mk._III_Scar_Twin",
        "keywords": {'twin', 'scar', 'ht', 'warden', 'niska', 'halftrack'}
    },
    {
        "name": "Niska-Rycker Mk. IX Skycaller",
        "url": "https://foxhole.wiki.gg/wiki/Niska-Rycker_Mk._IX_Skycaller",
        "keywords": {'rocket', 'ht', 'warden', 'niska', 'skycaller', 'rycker', 'halftrack'}
    },
    {
        "name": "Swallowtail 988/127-2",
        "url": "https://foxhole.wiki.gg/wiki/Swallowtail_988/127-2",
        "keywords": {'field', 'fmg', 'warden', 'swallotail', 'machine', 'gun'}
    },
    {
        "name": "G40 “Sagittarii”",
        "url": "https://foxhole.wiki.gg/wiki/G40_%E2%80%9CSagittarii%E2%80%9D",
        "keywords": {'field', 'fmg', 'colonial', 'sagittarii', 'machine', 'g40', 'gun'}
    },
    {
        "name": "Duncan's Coin 20mm",
        "url": "https://foxhole.wiki.gg/wiki/Duncan%27s_Coin_20mm",
        "keywords": {'20mm', 'anti', 'fatr', 'field', 'duncans', 'tank', 'warden', 'coin'}
    },
    {
        "name": "GA6 “Cestus”",
        "url": "https://foxhole.wiki.gg/wiki/GA6_%E2%80%9CCestus%E2%80%9D",
        "keywords": {'ga6', 'anti', 'fatr', 'field', 'colonial', 'tank', 'cestus'}
    },
    {
        "name": "120-68 “Koronides” Field Gun",
        "url": "https://foxhole.wiki.gg/wiki/Field_Artillery",
        "keywords": {'arty', 'field', 'colonial', 'artillery', '120', 'gun', 'koronides'}
    },
    {
        "name": "Balfour Wolfhound 40mm",
        "url": "https://foxhole.wiki.gg/wiki/Field_Cannon",
        "keywords": {'40mm', 'wolfhound', 'field', 'pushgun', 'warden', 'balfour', 'cannon'}
    },
    {
        "name": "Rycker 4/3-F Wasp Nest",
        "url": "https://foxhole.wiki.gg/wiki/Field_Launcher",
        "keywords": {'rocket', 'field', 'wasp', 'warden', 'launcher', 'rycker', 'nest'}
    },
    {
        "name": "Collins Cannon 68mm",
        "url": "https://foxhole.wiki.gg/wiki/Collins_Cannon_68mm",
        "keywords": {'anti', 'cannon', '68mm', 'collins', 'field', 'warden', 'fat', 'tank'}
    },
    {
        "name": "AA-2 Battering Ram",
        "url": "https://foxhole.wiki.gg/wiki/AA-2_Battering_Ram",
        "keywords": {'anti', 'battering', 'field', 'ram', 'tank', 'colonial', 'fat'}
    },
    {
        "name": "Balfour Falconer 250mm",
        "url": "https://foxhole.wiki.gg/wiki/Field_Mortar",
        "keywords": {'baby', '250mm', 'ballista', 'pushgun', 'warden', 'barlfour', 'fm', 'falconer'}
    },
    {
        "name": "Balfour Rampart 68mm",
        "url": "https://foxhole.wiki.gg/wiki/Heavy_Field_Cannon",
        "keywords": {'68mm', 'balfour', 'pushgun', 'warden', 'rampart', 'hv68', 'hvfat'}
    },
    {
        "name": "40-45 “Smelter” Heavy Field Gun",
        "url": "https://foxhole.wiki.gg/wiki/Heavy_Field_Gun",
        "keywords": {'smelter', 'hv40', 'field', 'pushgun', 'colonial', 'heavy', 'gun'}
    },
    {
        "name": "Balfour Stockade 75mm",
        "url": "https://foxhole.wiki.gg/wiki/Balfour_Stockade_75mm",
        "keywords": {'stockade', 'field', 'pushgun', '75mm', 'warden', 'balfour', 'large', 'gun'}
    },
    {
        "name": "945g “Stygian Bolt”",
        "url": "https://foxhole.wiki.gg/wiki/945g_%E2%80%9CStygian_Bolt%E2%80%9D",
        "keywords": {'large', 'field', 'bolt', 'pushgun', 'colonial', 'stygian', '945g', 'gun'}
    },
    {
        "name": "King Spire Mk. I",
        "url": "https://foxhole.wiki.gg/wiki/King_Spire_Mk._I",
        "keywords": {'spire', 'tank', 'mgst', 'warden', 'scout', 'king'}
    },
    {
        "name": "King Gallant Mk. II",
        "url": "https://foxhole.wiki.gg/wiki/King_Gallant_Mk._II",
        "keywords": {'warden', 'scout', 'gallant', '30mm', 'tank', 'king'}
    },
    {
        "name": "King Jester - Mk. I-1",
        "url": "https://foxhole.wiki.gg/wiki/King_Jester_-_Mk._I-1",
        "keywords": {'rocket', 'jester', 'tank', 'warden', 'scout', 'king'}
    },
    {
        "name": "H-5 “Hatchet”",
        "url": "https://foxhole.wiki.gg/wiki/H-5_%E2%80%9CHatchet%E2%80%9D",
        "keywords": {'h5', 'colonial', 'hatchet', 'tank', 'light', 'lt'}
    },
    {
        "name": "H-10 “Pelekys”",
        "url": "https://foxhole.wiki.gg/wiki/H-10_%E2%80%9CPelekys%E2%80%9D",
        "keywords": {'h10', 'pelekys', 'colonial', 'destroyer', 'tank', 'light', 'ltd'}
    },
    {
        "name": "H-19 “Vulcan”",
        "url": "https://foxhole.wiki.gg/wiki/H-19_%E2%80%9CVulcan%E2%80%9D",
        "keywords": {'flame', 'colonial', 'h19', 'vulcan', 'tank', 'light', 'lt'}
    },
    {
        "name": "H-8 “Kranesca”",
        "url": "https://foxhole.wiki.gg/wiki/H-8_%E2%80%9CKranesca%E2%80%9D",
        "keywords": {'colonial', 'h8', 'kranny', 'kranesca', 'tank', 'light', 'lt'}
    },
    {
        "name": "Devitt Mk. III",
        "url": "https://foxhole.wiki.gg/wiki/Devitt_Mk._III",
        "keywords": {'warden', 'devit', 'tank', 'light', 'lt'}
    },
    {
        "name": "Devitt Ironhide Mk. IV",
        "url": "https://foxhole.wiki.gg/wiki/Devitt_Ironhide_Mk._IV",
        "keywords": {'ironhide', 'warden', 'devit', 'tank', 'light', 'lt'}
    },
    {
        "name": "Devitt-Caine Mk. IV MMR",
        "url": "https://foxhole.wiki.gg/wiki/Devitt-Caine_Mk._IV_MMR",
        "keywords": {'devitt', 'caine', 'tank', 'warden', 'mlt', 'mortar', 'light'}
    },
    {
        "name": "85K-b “Falchion”",
        "url": "https://foxhole.wiki.gg/wiki/85K-b_%E2%80%9CFalchion%E2%80%9D",
        "keywords": {'85kb', 'assault', 'falchion', 'colonial', 'tank', 'mpt'}
    },
    {
        "name": "85K-a “Spatha”",
        "url": "https://foxhole.wiki.gg/wiki/85K-a_%E2%80%9CSpatha%E2%80%9D",
        "keywords": {'assault', 'tank', 'colonial', '85ka', 'spata', 'spatah', 'spatha', 'spahta'}
    },
    {
        "name": "85V-g “Talos”",
        "url": "https://foxhole.wiki.gg/wiki/85V-g_%E2%80%9CTalos%E2%80%9D",
        "keywords": {'assault', '75mm', '85vg', 'colonial', 'tank', 'talos'}
    },
    {
        "name": "90T-v “Nemesis”",
        "url": "https://foxhole.wiki.gg/wiki/90T-v_%E2%80%9CNemesis%E2%80%9D",
        "keywords": {'nemesis', '90tv', 'assault', '68mm', 'colonial', 'tank'}
    },
    {
        "name": "86K-a “Bardiche”",
        "url": "https://foxhole.wiki.gg/wiki/86K-a_%E2%80%9CBardiche%E2%80%9D",
        "keywords": {'assault', 'bardiche', 'colonial', 'tank', '86ka'}
    },
    {
        "name": "86K-c “Ranseur”",
        "url": "https://foxhole.wiki.gg/wiki/86K-c_%E2%80%9CRanseur%E2%80%9D",
        "keywords": {'assault', 'ranseur', 'rpg', 'colonial', 'quadiche', '86kc', 'tank'}
    },
    {
        "name": "Silverhand - Mk. IV",
        "url": "https://foxhole.wiki.gg/wiki/Silverhand_-_Mk._IV",
        "keywords": {'assault', 'svh', 'warden', 'tank', 'silverhand'}
    },
    {
        "name": "Silverhand Chieftain - Mk. VI",
        "url": "https://foxhole.wiki.gg/wiki/Silverhand_Chieftain_-_Mk._VI",
        "keywords": {'assault', 'chieftain', 'warden', 'tank', 'silverhand'}
    },
    {
        "name": "Silverhand Lordscar - Mk. X",
        "url": "https://foxhole.wiki.gg/wiki/Silverhand_Lordscar_-_Mk._X",
        "keywords": {'assault', 'lordscar', 'std', 'warden', 'destroyer', 'tank', 'silverhand'}
    },
    {
        "name": "Gallagher Brigand Mk. I",
        "url": "https://foxhole.wiki.gg/wiki/Gallagher_Brigand_Mk._I",
        "keywords": {'cruiser', 'gallagher', 'warden', 'brigand', 'tank'}
    },
    {
        "name": "Gallagher Outlaw Mk. II",
        "url": "https://foxhole.wiki.gg/wiki/Gallagher_Outlaw_Mk._II",
        "keywords": {'cruiser', 'gallagher', 'warden', 'tank', 'outlaw'}
    },
    {
        "name": "Gallagher Highwayman Mk. III",
        "url": "https://foxhole.wiki.gg/wiki/Gallagher_Highwayman_Mk._III",
        "keywords": {'hwm', 'cruiser', 'highwayman', 'gallagher', 'warden', 'tank'}
    },
    {
        "name": "Gallagher Thornfall Mk. VI",
        "url": "https://foxhole.wiki.gg/wiki/Gallagher_Thornfall_Mk._VI",
        "keywords": {'cruiser', 'gallagher', 'warden', 'bonelaw', 'tank', 'thornfall'}
    },
    {
        "name": "HC-2 “Scorpion”",
        "url": "https://foxhole.wiki.gg/wiki/Light_Infantry_Tank",
        "keywords": {'support', 'ist', 'colonial', 'hc2', 'tank', 'light', 'scorpion', 'infantry'}
    },
    {
        "name": "HC-7 “Ballista”",
        "url": "https://foxhole.wiki.gg/wiki/Siege_Tank",
        "keywords": {'ballista', 'colonial', 'siege', 'tank'}
    },
    {
        "name": "Noble Widow MK. XIV",
        "url": "https://foxhole.wiki.gg/wiki/Noble_Widow_MK._XIV",
        "keywords": {'widow', 'noble', 'htd', 'tank', 'warden', 'destroyer', 'heavy'}
    },
    {
        "name": "Noble Firebrand Mk. XVII",
        "url": "https://foxhole.wiki.gg/wiki/Noble_Firebrand_Mk._XVII",
        "keywords": {'flame', 'firebrand', 'warden', 'destroyer', 'heavy', 'noblle', 'tank'}
    },
    {
        "name": "Flood Juggernaut Mk. VII",
        "url": "https://foxhole.wiki.gg/wiki/Flood_Juggernaut_Mk._VII",
        "keywords": {'juggernaut', 'flame', 'warden', 'battle', 'flood', 'bt', 'tank'}
    },
    {
        "name": "Flood Mk. I",
        "url": "https://foxhole.wiki.gg/wiki/Flood_Mk._I",
        "keywords": {'warden', 'battle', 'flood', 'bt', 'tank'}
    },
    {
        "name": "Flood Mk. IX Stain",
        "url": "https://foxhole.wiki.gg/wiki/Flood_Mk._IX_Stain",
        "keywords": {'stain', 'warden', 'battle', 'flood', 'bt', 'spg', 'tank'}
    },
    {
        "name": "Lance-25 “Hasta”",
        "url": "https://foxhole.wiki.gg/wiki/Lance-25_%E2%80%9CHasta%E2%80%9D",
        "keywords": {'lance25', 'btd', 'colonial', 'destroyer', 'battle', 'tank', 'hasta'}
    },
    {
        "name": "Lance-36",
        "url": "https://foxhole.wiki.gg/wiki/Lance-36",
        "keywords": {'colonial', 'battle', 'lance36', 'bt', 'tank'}
    },
    {
        "name": "Lance-46 “Sarissa”",
        "url": "https://foxhole.wiki.gg/wiki/Lance-46_%E2%80%9CSarissa%E2%80%9D",
        "keywords": {'lance46', 'colonial', 'battle', 'sarissa', 'spg', 'tank'}
    },
    {
        "name": "Cullen Predator Mk. III",
        "url": "https://foxhole.wiki.gg/wiki/Cullen_Predator_Mk._III",
        "keywords": {'super', 'warden', 'predator', 'cullen', 'tank', 'sht'}
    },
    {
        "name": "O-75b “Ares”",
        "url": "https://foxhole.wiki.gg/wiki/O-75b_%E2%80%9CAres%E2%80%9D",
        "keywords": {'super', 'ares', 'colonial', 'tank', 'sht'}
    },
    {
        "name": "Dunne Fuelrunner 2d",
        "url": "https://foxhole.wiki.gg/wiki/Dunne_Fuelrunner_2d",
        "keywords": {'tanker', 'dunnel', 'fuelrunner', 'warden', 'fuel'}
    },
    {
        "name": "RR-3 “Stolon” Tanker",
        "url": "https://foxhole.wiki.gg/wiki/RR-3_%E2%80%9CStolon%E2%80%9D_Tanker",
        "keywords": {'stolon', 'tanker', 'colonial', 'fuel'}
    },
    {
        "name": "R-1 Hauler",
        "url": "https://foxhole.wiki.gg/wiki/R-1_Hauler",
        "keywords": {'hauler', 'truck', 'colonial', 'r1'}
    },
    {
        "name": "R-17 “Retiarius” Skirmisher",
        "url": "https://foxhole.wiki.gg/wiki/R-17_%E2%80%9CRetiarius%E2%80%9D_Skirmisher",
        "keywords": {'katyusha', 'skirmisher', 'retiarius', 'colonial', 'r17', 'truck'}
    },
    {
        "name": "R-5b “Sisyphus” Hauler",
        "url": "https://foxhole.wiki.gg/wiki/R-5b_%E2%80%9CSisyphus%E2%80%9D_Hauler",
        "keywords": {'hauler', 'sisyphus', 'colonial', 'r5b', 'truck'}
    },
    {
        "name": "R-9 “Speartip” Escort",
        "url": "https://foxhole.wiki.gg/wiki/R-9_%E2%80%9CSpeartip%E2%80%9D_Escort",
        "keywords": {'r9', 'colonial', 'speartip', 'escort', 'truck'}
    },
    {
        "name": "R-5 “Atlas” Hauler",
        "url": "https://foxhole.wiki.gg/wiki/R-5_%E2%80%9CAtlas%E2%80%9D_Hauler",
        "keywords": {'hauler', 'colonial', 'atlas', 'truck', 'r5'}
    },
    {
        "name": "Dunne Loadlugger 3c",
        "url": "https://foxhole.wiki.gg/wiki/Dunne_Loadlugger_3c",
        "keywords": {'loadlugger', 'dunne', 'warden', '3c', 'truck'}
    },
    {
        "name": "Dunne Transport",
        "url": "https://foxhole.wiki.gg/wiki/Dunne_Transport",
        "keywords": {'transport', 'dunne', 'warden', 'truck'}
    },
    {
        "name": "Dunne Landrunner 12c",
        "url": "https://foxhole.wiki.gg/wiki/Dunne_Landrunner_12c",
        "keywords": {'landrunner', 'warden', '12c', 'dunne', 'truck'}
    },
    {
        "name": "Dunne Leatherback 2a",
        "url": "https://foxhole.wiki.gg/wiki/Dunne_Leatherback_2a",
        "keywords": {'leatherback', 'warden', 'dunner', '2a', 'truck'}
    },
    {
        "name": "BMS - Class 2 Mobile Auto-Crane",
        "url": "https://foxhole.wiki.gg/wiki/Crane",
        "keywords": {'crane', 'mobile', 'class', 'bms'}
    },
    {
        "name": "BMS - Overseer Sky-Hauler",
        "url": "https://foxhole.wiki.gg/wiki/Large_Crane",
        "keywords": {'overseer', 'skyhauler', 'large', 'bms', 'crane'}
    },
    {
        "name": "BMS - Universal Assembly Rig",
        "url": "https://foxhole.wiki.gg/wiki/Construction_Vehicle",
        "keywords": {'cv', 'construction', 'vehicle', 'rig', 'universal', 'assembly', 'bms'}
    },
    {
        "name": "BMS - Fabricator",
        "url": "https://foxhole.wiki.gg/wiki/Advanced_Construction_Vehicle",
        "keywords": {'fabricator', 'construction', 'acv', 'vehicle', 'advanced', 'bms'}
    },
    {
        "name": "BMS - Packmule Flatbed",
        "url": "https://foxhole.wiki.gg/wiki/Flatbed_Truck",
        "keywords": {'flatbed', 'packmule', 'bms', 'truck'}
    },
    {
        "name": "BMS - Scrap Hauler",
        "url": "https://foxhole.wiki.gg/wiki/Harvester",
        "keywords": {'harvester', 'scrap', 'hauler', 'bms'}
    },
    {
        "name": "Rooster - Junkwagon",
        "url": "https://foxhole.wiki.gg/wiki/Rooster_-_Junkwagon",
        "keywords": {'trailer', 'rooster', 'junkwagon'}
    },
    {
        "name": "Rooster - Lamploader",
        "url": "https://foxhole.wiki.gg/wiki/Rooster_-_Lamploader",
        "keywords": {'trailer', 'rooster', 'lamploader'}
    },
    {
        "name": "Rooster - Tumblebox",
        "url": "https://foxhole.wiki.gg/wiki/Rooster_-_Tumblebox",
        "keywords": {'tumblebox', 'trailer', 'rooster'}
    },
    {
        "name": "Dunne Dousing Engine 3r",
        "url": "https://foxhole.wiki.gg/wiki/Dunne_Dousing_Engine_3r",
        "keywords": {'dousing', 'engine', '3r', 'warden', 'firetruck', 'dunne'}
    },
    {
        "name": "R-12b - “Salva” Flame Truck",
        "url": "https://foxhole.wiki.gg/wiki/R-12b_-_%E2%80%9CSalva%E2%80%9D_Flame_Truck",
        "keywords": {'salva', 'engine', 'flame', 'r12b', 'colonial', 'firetruck', 'truck'}
    },
    {
        "name": "Dunne Caravaner 2f",
        "url": "https://foxhole.wiki.gg/wiki/Dunne_Caravaner_2f",
        "keywords": {'caravaner', 'warden', '2f', 'bus', 'dunne'}
    },
    {
        "name": "R-15 - “Chariot”",
        "url": "https://foxhole.wiki.gg/wiki/R-15_-_%E2%80%9CChariot%E2%80%9D",
        "keywords": {'colonial', 'r15', 'chariot', 'bus'}
    },
    {
        "name": "Dunne Responder 3e",
        "url": "https://foxhole.wiki.gg/wiki/Dunne_Responder_3e",
        "keywords": {'responder', 'ambulance', 'warden', 'dunner', '3e'}
    },
    {
        "name": "R-12 - “Salus” Ambulance",
        "url": "https://foxhole.wiki.gg/wiki/R-12_-_%E2%80%9CSalus%E2%80%9D_Ambulance",
        "keywords": {'r12', 'colonial', 'salus', 'ambulance'}
    },
    {
        "name": "Cnute Cliffwrest",
        "url": "https://foxhole.wiki.gg/wiki/Cnute_Cliffwrest",
        "keywords": {'cnute', 'duty', 'warden', 'heavy', 'truck', 'cliffwrest'}
    },
    {
        "name": "AU-A150 Taurine Rigger",
        "url": "https://foxhole.wiki.gg/wiki/AU-A150_Taurine_Rigger",
        "keywords": {'duty', 'colonial', 'taurine', 'heavy', 'rigger', 'truck'}
    },
    {
        "name": "Blumfield LK205",
        "url": "https://foxhole.wiki.gg/wiki/Bicycle",
        "keywords": {'blumfield', 'warden', 'colonial', 'bicycle'}
    },
    {
        "name": "03MM “Caster”",
        "url": "https://foxhole.wiki.gg/wiki/03MM_%E2%80%9CCaster%E2%80%9D",
        "keywords": {'bike', 'motorcycle', 'colonial', 'caster'}
    },
    {
        "name": "00MS “Stinger”",
        "url": "https://foxhole.wiki.gg/wiki/00MS_%E2%80%9CStinger%E2%80%9D",
        "keywords": {'bike', 'motorcycle', 'stinger', 'colonial', 'mg'}
    },
    {
        "name": "Kivela Power Wheel 80-1",
        "url": "https://foxhole.wiki.gg/wiki/Kivela_Power_Wheel_80-1",
        "keywords": {'bike', 'power', 'motorcycle', 'kivela', 'warden', 'wheel'}
    },
    {
        "name": "UV-05a “Argonaut”",
        "url": "https://foxhole.wiki.gg/wiki/UV-05a_%E2%80%9CArgonaut%E2%80%9D",
        "keywords": {'colonial', 'uv05a', 'vehicle', 'argonaut', 'luv', 'light', 'utility'}
    },
    {
        "name": "UV-24 “Icarus”",
        "url": "https://foxhole.wiki.gg/wiki/UV-24_%E2%80%9CIcarus%E2%80%9D",
        "keywords": {'jeep', 'rpg', 'colonial', 'icarus', 'vehicle', 'uv24', 'luv', 'light', 'utility'}
    },
    {
        "name": "UV-5c “Odyssey”",
        "url": "https://foxhole.wiki.gg/wiki/UV-5c_%E2%80%9COdyssey%E2%80%9D",
        "keywords": {'colonial', 'vehicle', 'uv5c', 'odyssey', 'luv', 'light', 'utility'}
    },
    {
        "name": "Drummond 100a",
        "url": "https://foxhole.wiki.gg/wiki/Drummond_100a",
        "keywords": {'warden', 'vehicle', 'drummond', 'utility', 'luv', 'light', '100a'}
    },
    {
        "name": "Drummond Loscann 55c",
        "url": "https://foxhole.wiki.gg/wiki/Drummond_Loscann_55c",
        "keywords": {'aluv', 'amphibious', 'loscann', '55c', 'warden', 'drummond', 'vehicle', 'car', 'light', 'utility'}
    },
    {
        "name": "Drummond Spitfire 100d",
        "url": "https://foxhole.wiki.gg/wiki/Drummond_Spitfire_100d",
        "keywords": {'100d', 'spitfire', 'warden', 'drummond', 'vehicle', 'luv', 'light', 'utility'}
    },
    {
        "name": "MacConmara Shorerunner",
        "url": "https://foxhole.wiki.gg/wiki/MacConmara_Shorerunner",
        "keywords": {'landing', 'warden', 'shorerunner', 'ship', 'macconmara'}
    },
    {
        "name": "Interceptor PA-12",
        "url": "https://foxhole.wiki.gg/wiki/Interceptor_PA-12",
        "keywords": {'interceptor', 'landing', 'colonial', 'pa12', 'ship'}
    },
    {
        "name": "BMS - Aquatipper",
        "url": "https://foxhole.wiki.gg/wiki/Barge",
        "keywords": {'aquatipper', 'barge', 'bms'}
    },
    {
        "name": "BMS - Ironship",
        "url": "https://foxhole.wiki.gg/wiki/Freighter",
        "keywords": {'mbs', 'ironship', 'freighter'}
    },
    {
        "name": "BMS - Grouper",
        "url": "https://foxhole.wiki.gg/wiki/Motorboat",
        "keywords": {'motorboat', 'grouper', 'bms'}
    },
    {
        "name": "74b-1 Ronan Gunship",
        "url": "https://foxhole.wiki.gg/wiki/74b-1_Ronan_Gunship",
        "keywords": {'gunship', 'ronan', 'warden', '74b1', 'gunboat'}
    },
    {
        "name": "Type C - “Charon”",
        "url": "https://foxhole.wiki.gg/wiki/Type_C_-_%E2%80%9CCharon%E2%80%9D",
        "keywords": {'colonial', 'charon', 'gunboat'}
    },
    {
        "name": "Nakki",
        "url": "https://foxhole.wiki.gg/wiki/Nakki",
        "keywords": {'submarine', 'nakki', 'warden'}
    },
    {
        "name": "AC-b “Trident”",
        "url": "https://foxhole.wiki.gg/wiki/AC-b_%E2%80%9CTrident%E2%80%9D",
        "keywords": {'colonial', 'submarine', 'trident'}
    },
    {
        "name": "Blacksteele",
        "url": "https://foxhole.wiki.gg/wiki/Blacksteele",
        "keywords": {'frigate', 'light', 'warden', 'blacksteele'}
    },
    {
        "name": "Conqueror",
        "url": "https://foxhole.wiki.gg/wiki/Conqueror",
        "keywords": {'destroyer', 'dd', 'colonial', 'conqueror'}
    },
    {
        "name": "BMS - Longhook",
        "url": "https://foxhole.wiki.gg/wiki/Base_Ship",
        "keywords": {'lh', 'ship', 'base', 'bms', 'longhook'}
    },
    {
        "name": "BMS - Bluefin",
        "url": "https://foxhole.wiki.gg/wiki/Storage_Ship",
        "keywords": {'storage', 'bluefin', 'ship', 'bms'}
    },
    {
        "name": "BMS - Bowhead",
        "url": "https://foxhole.wiki.gg/wiki/Resource_Ship",
        "keywords": {'resource', 'ship', 'bowhead', 'bms'}
    },
    {
        "name": "Callahan (Battleship)",
        "url": "https://foxhole.wiki.gg/wiki/Callahan_(Battleship)",
        "keywords": {'callahan', 'bs', 'warden', 'battleship'}
    },
    {
        "name": "Titan",
        "url": "https://foxhole.wiki.gg/wiki/Titan",
        "keywords": {'titan', 'bs', 'colonial', 'battleship'}
    },
    {
        "name": "BMS Railtruck",
        "url": "https://foxhole.wiki.gg/wiki/Small_Container_Car",
        "keywords": {'container', 'car', 'railtruck', 'bms', 'small'}
    },
    {
        "name": "BMS Linerunner",
        "url": "https://foxhole.wiki.gg/wiki/Small_Flatbed_Car",
        "keywords": {'flatbed', 'car', 'linerunner', 'bms', 'small'}
    },
    {
        "name": "BMS Tinderbox",
        "url": "https://foxhole.wiki.gg/wiki/Small_Liquid_Container_Car",
        "keywords": {'container', 'tinderbox', 'car', 'liquid', 'bms', 'small'}
    },
    {
        "name": "BMS Stowheel",
        "url": "https://foxhole.wiki.gg/wiki/Small_Box_Car",
        "keywords": {'container', 'box', 'stowheel', 'car', 'bms', 'small'}
    },
    {
        "name": "BMS Mineseeker",
        "url": "https://foxhole.wiki.gg/wiki/Small_Train_Locomotive",
        "keywords": {'mineseeker', 'locomotive', 'train', 'bms', 'small'}
    },
    {
        "name": "BMS Rockhold",
        "url": "https://foxhole.wiki.gg/wiki/Container_Car",
        "keywords": {'container', 'rockhold', 'car', 'train', 'large', 'bms'}
    },
    {
        "name": "BMS Roadhouse",
        "url": "https://foxhole.wiki.gg/wiki/Caboose",
        "keywords": {'roadhouse', 'caboose', 'train', 'large', 'bms'}
    },
    {
        "name": "BMS Longrider",
        "url": "https://foxhole.wiki.gg/wiki/Flatbed_Car",
        "keywords": {'longrider', 'flatbed', 'car', 'train', 'large', 'bms'}
    },
    {
        "name": "BMS Holdout",
        "url": "https://foxhole.wiki.gg/wiki/Infantry_Car",
        "keywords": {'bms', 'car', 'train', 'large', 'holdout', 'infantry'}
    },
    {
        "name": "BMS Black Bolt",
        "url": "https://foxhole.wiki.gg/wiki/Locomotive",
        "keywords": {'black', 'bolt', 'locomotive', 'train', 'large', 'bms'}
    },
    {
        "name": "O'Brien Warsmith v.215",
        "url": "https://foxhole.wiki.gg/wiki/O%27Brien_Warsmith_v.215",
        "keywords": {'obrien', 'v215', 'warden', 'car', 'combat', 'warsmith'}
    },
    {
        "name": "Aegis Steelbreaker K5a",
        "url": "https://foxhole.wiki.gg/wiki/Aegis_Steelbreaker_K5a",
        "keywords": {'aegis', 'steelbreaker', 'colonial', 'car', 'k5a', 'combat'}
    },
    {
        "name": "Tempest Cannon RA-2",
        "url": "https://foxhole.wiki.gg/wiki/Long-Range_Artillery_Car",
        "keywords": {'range', 'rsc', 'long', 'car', 'artillery', 'cannon', 'tempest'}
    },
    {
        "name": "Armoured Fighting Tractor",
        "url": "https://foxhole.wiki.gg/wiki/Armoured_Fighting_Tractor",
        "keywords": {'armoured', 'tractor', 'vehicle', 'fighting', 'amored', 'relic'}
    },
    {
        "name": "PL-1 “Phalanx”",
        "url": "https://foxhole.wiki.gg/wiki/Relic_Assault_Tank",
        "keywords": {'assault', 'pl1', 'vehicle', 'tank', 'phalanx', 'relic'}
    },
    {
        "name": "Storm Tank",
        "url": "https://foxhole.wiki.gg/wiki/Storm_Tank",
        "keywords": {'storm', 'tank', 'relic', 'vehicle'}
    },
    {
        "name": "Staff Car",
        "url": "https://foxhole.wiki.gg/wiki/Staff_Car",
        "keywords": {'staff', 'vehicle', 'relic', 'car'}
    },
    {
        "name": "Repurposed Truck",
        "url": "https://foxhole.wiki.gg/wiki/Repurposed_Truck",
        "keywords": {'vehicle', 'truck', 'relic', 'repurposed'}
    },
]

STRUCTURES_WIKI_ENTRIES = [
    {
        "name": "Border Base",
        "url": "https://foxhole.wiki.gg/wiki/Border_Base",
        "keywords": {'bb', 'border', 'bob', 'base'}
    },
    {
        "name": "Relic Base",
        "url": "https://foxhole.wiki.gg/wiki/Relic_Base",
        "keywords": {'relic', 'base'}
    },
    {
        "name": "Town Base (Tier 1)",
        "url": "https://foxhole.wiki.gg/wiki/Town_Base#Tier_1-0",
        "keywords": {'townbase', 't1'}
    },
    {
        "name": "Town Base (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Town_Base#Tier_2-0",
        "keywords": {'townbase', 't2'}
    },
    {
        "name": "Town Base (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Town_Base#Tier_3-0",
        "keywords": {'townbase', 't3'}
    },
    {
        "name": "Bunker Base (Tier 1)",
        "url": "https://foxhole.wiki.gg/wiki/Bunker_Base#Tier_1-0",
        "keywords": {'bb', 'bunker', 'bob', 'base', 't1'}
    },
    {
        "name": "Bunker Base (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Bunker_Base#Tier_2-0",
        "keywords": {'bunker', 'core', 'bob', 'bb', 'base', 't2'}
    },
    {
        "name": "Bunker Base (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Bunker_Base#Tier_3-0",
        "keywords": {'bunker', 'core', 'bob', 'bb', 'base', 'concrete', 't3'}
    },
    {
        "name": "Encampment",
        "url": "https://foxhole.wiki.gg/wiki/Encampment",
        "keywords": {'encampment'}
    },
    {
        "name": "Keep",
        "url": "https://foxhole.wiki.gg/wiki/Keep",
        "keywords": {'keep'}
    },
    {
        "name": "Safe House (Tier 1)",
        "url": "https://foxhole.wiki.gg/wiki/Safe_House#Tier_1-0",
        "keywords": {'house', 'safe', 't1'}
    },
    {
        "name": "Safe House (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Safe_House#Tier_2-0",
        "keywords": {'house', 'safe', 't2'}
    },
    {
        "name": "Safe House (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Safe_House#Tier_3-0",
        "keywords": {'house', 'safe', 't3'}
    },
    {
        "name": "Seaport",
        "url": "https://foxhole.wiki.gg/wiki/Seaport",
        "keywords": {'seaport'}
    },
    {
        "name": "Storage Depot",
        "url": "https://foxhole.wiki.gg/wiki/Storage_Depot",
        "keywords": {'depot', 'storage'}
    },
    {
        "name": "Liquid Container",
        "url": "https://foxhole.wiki.gg/wiki/Liquid_Container",
        "keywords": {'liquid', 'container'}
    },
    {
        "name": "Liquid Transfer Station",
        "url": "https://foxhole.wiki.gg/wiki/Liquid_Transfer_Station",
        "keywords": {'liquid', 'station', 'transfer', 'lts'}
    },
    {
        "name": "Material Pallet",
        "url": "https://foxhole.wiki.gg/wiki/Material_Pallet",
        "keywords": {'material', 'pallet'}
    },
    {
        "name": "Material Transfer Station",
        "url": "https://foxhole.wiki.gg/wiki/Material_Transfer_Station",
        "keywords": {'material', 'station', 'mts', 'transfer'}
    },
    {
        "name": "Resource Container",
        "url": "https://foxhole.wiki.gg/wiki/Resource_Container",
        "keywords": {'resource', 'container'}
    },
    {
        "name": "Resource Transfer Station",
        "url": "https://foxhole.wiki.gg/wiki/Resource_Transfer_Station",
        "keywords": {'rts', 'resource', 'station', 'transfer'}
    },
    {
        "name": "Infantry Arms Factory",
        "url": "https://foxhole.wiki.gg/wiki/Infantry_Arms_Factory",
        "keywords": {'factory', 'arms', 'infantry'}
    },
    {
        "name": "Crate Transfer Station",
        "url": "https://foxhole.wiki.gg/wiki/Crate_Transfer_Station",
        "keywords": {'crate', 'station', 'transfer'}
    },
    {
        "name": "Shippable Crate",
        "url": "https://foxhole.wiki.gg/wiki/Shippable_Crate",
        "keywords": {'crate', 'shippable'}
    },
    {
        "name": "Shipping Container",
        "url": "https://foxhole.wiki.gg/wiki/Shipping_Container",
        "keywords": {'shipping', 'container'}
    },
    {
        "name": "Storage Box",
        "url": "https://foxhole.wiki.gg/wiki/Storage_Box",
        "keywords": {'box', 'storage'}
    },
    {
        "name": "Medical Room (Tier 1)",
        "url": "https://foxhole.wiki.gg/wiki/Medical_Room",
        "keywords": {'bunker', 'room', 'medical', 't1'}
    },
    {
        "name": "Medical Room (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Medical_Room#Tier_2-0",
        "keywords": {'bunker', 'room', 'medical', 't2'}
    },
    {
        "name": "Medical Room (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Medical_Room#Tier_3-0",
        "keywords": {'bunker', 'room', 'medical', 't3'}
    },
    {
        "name": "Storage Room (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Storage_Room#Tier_2-0",
        "keywords": {'bunker', 'room', 'storage', 't2'}
    },
    {
        "name": "Storage Room (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Storage_Room#Tier_3-0",
        "keywords": {'bunker', 'room', 'storage', 't3'}
    },
    {
        "name": "Coastal Gun",
        "url": "https://foxhole.wiki.gg/wiki/Coastal_Gun",
        "keywords": {'gun', 'coastal'}
    },
    {
        "name": "Garrisoned House",
        "url": "https://foxhole.wiki.gg/wiki/Garrisoned_House",
        "keywords": {'ghouse', 'garrisoned', 'house'}
    },
    {
        "name": "Observation Tower",
        "url": "https://foxhole.wiki.gg/wiki/Observation_Tower",
        "keywords": {'observation', 'tower', 'obs'}
    },
    {
        "name": "Anti-Tank Pillbox",
        "url": "https://foxhole.wiki.gg/wiki/Anti-Tank_Pillbox",
        "keywords": {'at', 'pillbox', 'anti', 'tank'}
    },
    {
        "name": "AT Gun Garrison (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/AT_Gun_Garrison#Tier_2-0",
        "keywords": {'bunker', 'atg', 'at', 'gun', 'garrison', 't2'}
    },
    {
        "name": "AT Gun Garrison (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/AT_Gun_Garrison#Tier_3-0",
        "keywords": {'bunker', 'atg', 'at', 'gun', 'garrison', 'concrete', 't3'}
    },
    {
        "name": "Howitzer Garrison",
        "url": "https://foxhole.wiki.gg/wiki/Howitzer_Garrison",
        "keywords": {'howies', 'bunker', 'howitzer', 'garrison', 'concrete'}
    },
    {
        "name": "Machine Gun Garrison (Tier 1)",
        "url": "https://foxhole.wiki.gg/wiki/Machine_Gun_Garrison#Tier_1-0",
        "keywords": {'bunker', 'mgg', 'machine', 'gun', 'garrison', 'mg', 't1'}
    },
    {
        "name": "Machine Gun Garrison (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Machine_Gun_Garrison#Tier_2-0",
        "keywords": {'bunker', 'mgg', 'machine', 'gun', 'garrison', 'mg', 't2'}
    },
    {
        "name": "Machine Gun Garrison (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Machine_Gun_Garrison#Tier_3-0",
        "keywords": {'bunker', 'mgg', 'machine', 'gun', 'garrison', 'mg', 'concrete', 't3'}
    },
    {
        "name": "Machine Gun Pillbox",
        "url": "https://foxhole.wiki.gg/wiki/Machine_Gun_Pillbox",
        "keywords": {'pillbox', 'machine', 'gun', 'mg'}
    },
    {
        "name": "Observation Bunker (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Observation_Bunker#Tier_2-0",
        "keywords": {'observation', 'bunker', 'obs', 't2'}
    },
    {
        "name": "Observation Bunker (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Observation_Bunker#Tier_3-0",
        "keywords": {'observation', 'bunker', 'obs', 'concrete', 't3'}
    },
    {
        "name": "Rifle Garrison (Tier 1)",
        "url": "https://foxhole.wiki.gg/wiki/Rifle_Garrison#Tier_1-0",
        "keywords": {'garrison', 'rifle', 'rg', 'bunker', 't1'}
    },
    {
        "name": "Rifle Garrison (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Rifle_Garrison#Tier_2-0",
        "keywords": {'garrison', 'rifle', 'rg', 'bunker', 't2'}
    },
    {
        "name": "Rifle Garrison (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Rifle_Garrison#Tier_3-0",
        "keywords": {'rifle', 'bunker', 'rg', 'garrison', 'concrete', 't3'}
    },
    {
        "name": "Rifle Pillbox",
        "url": "https://foxhole.wiki.gg/wiki/Rifle_Pillbox",
        "keywords": {'pillbox', 'rifle'}
    },
    {
        "name": "Watch Tower",
        "url": "https://foxhole.wiki.gg/wiki/Watch_Tower",
        "keywords": {'wt', 'watch', 'tower'}
    },
    {
        "name": "Emplacement House",
        "url": "https://foxhole.wiki.gg/wiki/Emplacement_House",
        "keywords": {'mhouse', 'emplacement', 'mortar', 'mortar'}
    },
    {
        "name": "50-500 “Thunderbolt” Cannon",
        "url": "https://foxhole.wiki.gg/wiki/50-500_%E2%80%9CThunderbolt%E2%80%9D_Cannon",
        "keywords": {'thunderbolt', '150mm', 'cannon', 'arty', 'colonial', 'artillery'}
    },
    {
        "name": "DAE 1b-2 “Serra”",
        "url": "https://foxhole.wiki.gg/wiki/DAE_1b-2_%E2%80%9CSerra%E2%80%9D",
        "keywords": {'emplaced', 'emg', 'serra', 'machine', 'gun', 'colonial'}
    },
    {
        "name": "DAE 1o-3 “Polybolos”",
        "url": "https://foxhole.wiki.gg/wiki/DAE_1o-3_%E2%80%9CPolybolos%E2%80%9D",
        "keywords": {'emplaced', 'at', 'polybolos', 'gun', 'beat', 'colonial'}
    },
    {
        "name": "DAE 2a-1 “Ruptura”",
        "url": "https://foxhole.wiki.gg/wiki/DAE_2a-1_%E2%80%9CRuptura%E2%80%9D",
        "keywords": {'ruptura', 'colonial'}
    },
    {
        "name": "DAE 3b-2 “Hades' Net”",
        "url": "https://foxhole.wiki.gg/wiki/DAE_3b-2_%E2%80%9CHades%27_Net%E2%80%9D",
        "keywords": {'emplaced', 'net', 'hades', 'colonial', 'rocket', 'artillery'}
    },
    {
        "name": "Huber Exalt 150mm",
        "url": "https://foxhole.wiki.gg/wiki/Huber_Exalt_150mm",
        "keywords": {'hubert', 'exalt', '150mm', 'warden', 'arty', 'artillery'}
    },
    {
        "name": "Huber Lariat 120mm",
        "url": "https://foxhole.wiki.gg/wiki/Light_Artillery",
        "keywords": {'lariat', 'warden', 'arty', 'huber', 'artillery'}
    },
    {
        "name": "Huber Starbreaker 94.5mm",
        "url": "https://foxhole.wiki.gg/wiki/Huber_Starbreaker_94.5mm",
        "keywords": {'starbreaker', 'warden', '945mm', 'huber'}
    },
    {
        "name": "Intelligence Center",
        "url": "https://foxhole.wiki.gg/wiki/Intelligence_Center",
        "keywords": {'center', 'intelligence', 'ic'}
    },
    {
        "name": "Leary Shellbore 68mm",
        "url": "https://foxhole.wiki.gg/wiki/Leary_Shellbore_68mm",
        "keywords": {'emplaced', '68mm', 'shellbore', 'leary', 'warden', 'at', 'eat', 'gun'}
    },
    {
        "name": "Leary Snare Trap 127",
        "url": "https://foxhole.wiki.gg/wiki/Leary_Snare_Trap_127",
        "keywords": {'snare', 'emplaced', 'emg', 'leary', 'warden', 'machine', '127', 'gun', 'trap'}
    },
    {
        "name": "Storm Cannon",
        "url": "https://foxhole.wiki.gg/wiki/Storm_Cannon",
        "keywords": {'storm', 'sc', 'cannon'}
    },
    {
        "name": "Barbed Wire",
        "url": "https://foxhole.wiki.gg/wiki/Barbed_Wire_(Structure)",
        "keywords": {'barbed', 'wire'}
    },
    {
        "name": "Barbed Wire Fence",
        "url": "https://foxhole.wiki.gg/wiki/Barbed_Wire_Fence",
        "keywords": {'barbed', 'wire', 'fence'}
    },
    {
        "name": "Prepared Minefield",
        "url": "https://foxhole.wiki.gg/wiki/Prepared_Minefield",
        "keywords": {'prepared', 'minefield'}
    },
    {
        "name": "Crow's Foot Minefield",
        "url": "https://foxhole.wiki.gg/wiki/Crow%27s_Foot_Minefield",
        "keywords": {'anti', 'personal', 'infantry', 'minefield', 'crows', 'foot'}
    },
    {
        "name": "Abisme AT-99 Minefield",
        "url": "https://foxhole.wiki.gg/wiki/Abisme_AT-99_Minefield",
        "keywords": {'anti', 'minefield', 'at', 'abisme', 'tank'}
    },
    {
        "name": "Bunker (Tier 1)",
        "url": "https://foxhole.wiki.gg/wiki/Bunker#Tier_1-0",
        "keywords": {'bunker', 't1'}
    },
    {
        "name": "Bunker (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Bunker#Tier_2-0",
        "keywords": {'bunker', 't2'}
    },
    {
        "name": "Bunker (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Bunker#Tier_3-0",
        "keywords": {'bunker', 't3'}
    },
    {
        "name": "Bunker Corner (Tier 1)",
        "url": "https://foxhole.wiki.gg/wiki/Bunker_Corner#Tier_1-0",
        "keywords": {'bunker', 'corner', 't1'}
    },
    {
        "name": "Bunker Corner (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Bunker_Corner#Tier_2-0",
        "keywords": {'bunker', 'corner', 't2'}
    },
    {
        "name": "Bunker Corner (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Bunker_Corner#Tier_3-0",
        "keywords": {'bunker', 'corner', 't3'}
    },
    {
        "name": "Bunker Ramp (Tier 1)",
        "url": "https://foxhole.wiki.gg/wiki/Bunker_Ramp#Tier_1-0",
        "keywords": {'ramp', 'bunker', 't1'}
    },
    {
        "name": "Bunker Ramp (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Bunker_Ramp#Tier_2-0",
        "keywords": {'ramp', 'bunker', 't2'}
    },
    {
        "name": "Bunker Ramp (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Bunker_Ramp#Tier_3-0",
        "keywords": {'ramp', 'bunker', 't3'}
    },
    {
        "name": "Dragon's Teeth",
        "url": "https://foxhole.wiki.gg/wiki/Dragon%27s_Teeth",
        "keywords": {'dragon', 'teeth'}
    },
    {
        "name": "Foxhole",
        "url": "https://foxhole.wiki.gg/wiki/Foxhole_(Structure)",
        "keywords": {'dug', 'foxhole'}
    },
    {
        "name": "Gate (Tier 1)",
        "url": "https://foxhole.wiki.gg/wiki/Gate#Tier_1-0",
        "keywords": {'gate', 't1'}
    },
    {
        "name": "Gate (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Gate#Tier_2-0",
        "keywords": {'gate', 't2'}
    },
    {
        "name": "Gate (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Gate#Tier_3-0",
        "keywords": {'gate', 'concrete', 't3'}
    },
    {
        "name": "Sandbag Cover",
        "url": "https://foxhole.wiki.gg/wiki/Sandbag_Cover#Sandbag_Cover_(Tier_1)-0",
        "keywords": {'sandbags', 'cover'}
    },
    {
        "name": "Sandbag Wall",
        "url": "https://foxhole.wiki.gg/wiki/Sandbag_Cover#Sandbag_Wall_(Tier_2)-0",
        "keywords": {'sandbags', 'wall'}
    },
    {
        "name": "Tank Trap",
        "url": "https://foxhole.wiki.gg/wiki/Tank_Trap",
        "keywords": {'trap', 'tank'}
    },
    {
        "name": "Trench (Tier 1)",
        "url": "https://foxhole.wiki.gg/wiki/Trench#Tier_1-0",
        "keywords": {'trench', 't1'}
    },
    {
        "name": "Trench (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Trench#Tier_2-0",
        "keywords": {'trench', 't2'}
    },
    {
        "name": "Trench (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Trench#Tier_3-0",
        "keywords": {'trench', 't3'}
    },
    {
        "name": "Trench Connector (Tier 1)",
        "url": "https://foxhole.wiki.gg/wiki/Trench_Connector#Tier_1-0",
        "keywords": {'connector', 'trench', 't1'}
    },
    {
        "name": "Trench Connector (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Trench_Connector#Tier_2-0",
        "keywords": {'connector', 'trench', 't2'}
    },
    {
        "name": "Trench Connector (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Trench_Connector#Tier_3-0",
        "keywords": {'connector', 'trench', 'concrete', 't3'}
    },
    {
        "name": "Trench Emplacement (Tier 1)",
        "url": "https://foxhole.wiki.gg/wiki/Trench_Emplacement#Tier_1-0",
        "keywords": {'emplacement', 'pit', 'trench', 't1'}
    },
    {
        "name": "Trench Emplacement (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Trench_Emplacement#Tier_2-0",
        "keywords": {'emplacement', 'pit', 'trench', 't2'}
    },
    {
        "name": "Trench Emplacement (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Trench_Emplacement#Tier_3-0",
        "keywords": {'emplacement', 'pit', 'trench', 'concrete', 't3'}
    },
    {
        "name": "Wall (Tier 1)",
        "url": "https://foxhole.wiki.gg/wiki/Wall#Tier_1-0",
        "keywords": {'t1', 'wall'}
    },
    {
        "name": "Wall (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Wall#Tier_2-0",
        "keywords": {'t2', 'wall'}
    },
    {
        "name": "Wall (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Wall#Tier_3-0",
        "keywords": {'t3', 'wall', 'concrete'}
    },
    {
        "name": "Construction Yard",
        "url": "https://foxhole.wiki.gg/wiki/Construction_Yard",
        "keywords": {'yard', 'construction'}
    },
    {
        "name": "Engineering Center",
        "url": "https://foxhole.wiki.gg/wiki/Engineering_Center",
        "keywords": {'center', 'tech', 'engineering'}
    },
    {
        "name": "Factory",
        "url": "https://foxhole.wiki.gg/wiki/Factory",
        "keywords": {'factory'}
    },
    {
        "name": "Garage",
        "url": "https://foxhole.wiki.gg/wiki/Garage",
        "keywords": {'garage'}
    },
    {
        "name": "Hospital",
        "url": "https://foxhole.wiki.gg/wiki/Hospital",
        "keywords": {'hospital'}
    },
    {
        "name": "Mass Production Factory",
        "url": "https://foxhole.wiki.gg/wiki/Mass_Production_Factory",
        "keywords": {'production', 'mpf', 'mass', 'factory'}
    },
    {
        "name": "Refinery",
        "url": "https://foxhole.wiki.gg/wiki/Refinery",
        "keywords": {'refinery', 'raf'}
    },
    {
        "name": "Shipyard",
        "url": "https://foxhole.wiki.gg/wiki/Shipyard",
        "keywords": {'shipyard'}
    },
    {
        "name": "Ammunition Factory",
        "url": "https://foxhole.wiki.gg/wiki/Ammunition_Factory",
        "keywords": {'factory', 'ammunition', 'ammo'}
    },
    {
        "name": "Coal Refinery",
        "url": "https://foxhole.wiki.gg/wiki/Coal_Refinery",
        "keywords": {'refinery', 'coal'}
    },
    {
        "name": "Concrete Mixer",
        "url": "https://foxhole.wiki.gg/wiki/Concrete_Mixer",
        "keywords": {'mixer', 'concrete'}
    },
    {
        "name": "Dry Dock",
        "url": "https://foxhole.wiki.gg/wiki/Dry_Dock",
        "keywords": {'dock', 'dry'}
    },
    {
        "name": "Field Hospital",
        "url": "https://foxhole.wiki.gg/wiki/Field_Hospital",
        "keywords": {'hospital', 'field'}
    },
    {
        "name": "Field Modification Center",
        "url": "https://foxhole.wiki.gg/wiki/Field_Modification_Center",
        "keywords": {'center', 'modification', 'field'}
    },
    {
        "name": "Large Assembly Station",
        "url": "https://foxhole.wiki.gg/wiki/Large_Assembly_Station",
        "keywords": {'pad', 'large', 'station', 'assembly', 'upgrade'}
    },
    {
        "name": "Materials Factory",
        "url": "https://foxhole.wiki.gg/wiki/Materials_Factory",
        "keywords": {'factory', 'materials'}
    },
    {
        "name": "Metalworks Factory",
        "url": "https://foxhole.wiki.gg/wiki/Metalworks_Factory",
        "keywords": {'factory', 'metalworks'}
    },
    {
        "name": "Oil Refinery",
        "url": "https://foxhole.wiki.gg/wiki/Oil_Refinery",
        "keywords": {'refinery', 'oil'}
    },
    {
        "name": "Small Assembly Station",
        "url": "https://foxhole.wiki.gg/wiki/Small_Assembly_Station",
        "keywords": {'small', 'pad', 'station', 'assembly', 'upgrade'}
    },
    {
        "name": "Salvage Mine",
        "url": "https://foxhole.wiki.gg/wiki/Salvage_Mine",
        "keywords": {'salvage', 'scrap', 'mine'}
    },
    {
        "name": "Sulfur Mine",
        "url": "https://foxhole.wiki.gg/wiki/Sulfur_Mine",
        "keywords": {'mine', 'sulfur'}
    },
    {
        "name": "Component Mine",
        "url": "https://foxhole.wiki.gg/wiki/Component_Mine",
        "keywords": {'mine', 'component'}
    },
    {
        "name": "Offshore Platform",
        "url": "https://foxhole.wiki.gg/wiki/Offshore_Platform",
        "keywords": {'platform', 'offshore'}
    },
    {
        "name": "Oil Well",
        "url": "https://foxhole.wiki.gg/wiki/Oil_Well",
        "keywords": {'well', 'oil'}
    },
    {
        "name": "Stationary Harvester (Coal)",
        "url": "https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Coal)",
        "keywords": {'stationary', 'coal', 'harvester'}
    },
    {
        "name": "Stationary Harvester (Components)",
        "url": "https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Components)",
        "keywords": {'components', 'stationary', 'harvester'}
    },
    {
        "name": "Stationary Harvester (Salvage)",
        "url": "https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Salvage)",
        "keywords": {'salvage', 'stationary', 'harvester'}
    },
    {
        "name": "Stationary Harvester (Sulfur)",
        "url": "https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Sulfur)",
        "keywords": {'stationary', 'sulfur', 'harvester'}
    },
    {
        "name": "Water Pump",
        "url": "https://foxhole.wiki.gg/wiki/Water_Pump",
        "keywords": {'pump', 'water'}
    },
    {
        "name": "Stone Bridge",
        "url": "https://foxhole.wiki.gg/wiki/Stone_Bridge",
        "keywords": {'bridge', 'stone'}
    },
    {
        "name": "Two Tier Bridge",
        "url": "https://foxhole.wiki.gg/wiki/Two_Tier_Bridge",
        "keywords": {'tier', 'bridge', 'two'}
    },
    {
        "name": "Double Bridge",
        "url": "https://foxhole.wiki.gg/wiki/Double_Bridge",
        "keywords": {'double', 'bridge'}
    },
    {
        "name": "Long Bridge",
        "url": "https://foxhole.wiki.gg/wiki/Long_Bridge",
        "keywords": {'bridge', 'long'}
    },
    {
        "name": "Train Bridge",
        "url": "https://foxhole.wiki.gg/wiki/Train_Bridge",
        "keywords": {'train', 'bridge'}
    },
    {
        "name": "Field Bridge",
        "url": "https://foxhole.wiki.gg/wiki/Field_Bridge",
        "keywords": {'bridge', 'field'}
    },
    {
        "name": "Dock",
        "url": "https://foxhole.wiki.gg/wiki/Dock",
        "keywords": {'dock', 'docks'}
    },
    {
        "name": "Stationary Crane",
        "url": "https://foxhole.wiki.gg/wiki/Stationary_Crane",
        "keywords": {'stationary', 'crane'}
    },
    {
        "name": "A0E-9 Rocket",
        "url": "https://foxhole.wiki.gg/wiki/A0E-9_Rocket",
        "keywords": {'nuke', 'rocket'}
    },
    {
        "name": "BMS Foreman Stacker",
        "url": "https://foxhole.wiki.gg/wiki/Facility_Crane",
        "keywords": {'crane', 'bms', 'stacker', 'facility', 'foreman'}
    },
    {
        "name": "Catwalk Bridge",
        "url": "https://foxhole.wiki.gg/wiki/Catwalk_Bridge",
        "keywords": {'catwalk', 'bridge'}
    },
    {
        "name": "Catwalk Platform",
        "url": "https://foxhole.wiki.gg/wiki/Catwalk_Platform",
        "keywords": {'catwalk', 'platform'}
    },
    {
        "name": "Catwalk Stairs",
        "url": "https://foxhole.wiki.gg/wiki/Catwalk_Stairs",
        "keywords": {'catwalk', 'stairs'}
    },
    {
        "name": "Crane Railway Track",
        "url": "https://foxhole.wiki.gg/wiki/Crane_Railway_Track",
        "keywords": {'crane', 'railway', 'track'}
    },
    {
        "name": "Engine Room (Tier 2)",
        "url": "https://foxhole.wiki.gg/wiki/Engine_Room#Tier_2-0",
        "keywords": {'bunker', 'engine', 'room', 't2'}
    },
    {
        "name": "Engine Room (Tier 3)",
        "url": "https://foxhole.wiki.gg/wiki/Engine_Room#Tier_3-0",
        "keywords": {'bunker', 'engine', 'room', 'concrete', 't3'}
    },
    {
        "name": "Fire Pit",
        "url": "https://foxhole.wiki.gg/wiki/Fire_Pit",
        "keywords": {'fire', 'pit', 'campfire'}
    },
    {
        "name": "Foundation (1x1)",
        "url": "https://foxhole.wiki.gg/wiki/Foundation#1x1-0",
        "keywords": {'foundation'}
    },
    {
        "name": "Concrete Foundation (1x1)",
        "url": "https://foxhole.wiki.gg/wiki/Foundation#1x1_Concrete-0",
        "keywords": {'foundation', 'concrete'}
    },
    {
        "name": "Foundation Corner (1x1)",
        "url": "https://foxhole.wiki.gg/wiki/Foundation#Corner_1x1-0",
        "keywords": {'foundation'}
    },
    {
        "name": "Concrete Foundation Corner (1x1)",
        "url": "https://foxhole.wiki.gg/wiki/Foundation#Corner_1x1_Concrete-0",
        "keywords": {'foundation', 'concrete'}
    },
    {
        "name": "Foundation (1x2)",
        "url": "https://foxhole.wiki.gg/wiki/Foundation#1x2-0",
        "keywords": {'foundation'}
    },
    {
        "name": "Concrete Foundation (1x2)",
        "url": "https://foxhole.wiki.gg/wiki/Foundation#1x2_Concrete-0",
        "keywords": {'foundation', 'concrete'}
    },
    {
        "name": "Foundation (2x2)",
        "url": "https://foxhole.wiki.gg/wiki/Foundation#2x2-0",
        "keywords": {'foundation'}
    },
    {
        "name": "Concrete Foundation (2x2)",
        "url": "https://foxhole.wiki.gg/wiki/Foundation#2x2_Concrete-0",
        "keywords": {'foundation', 'concrete'}
    },
    {
        "name": "Fuel Silo",
        "url": "https://foxhole.wiki.gg/wiki/Fuel_Silo",
        "keywords": {'silo', 'fuel'}
    },
    {
        "name": "Maintenance Tunnel",
        "url": "https://foxhole.wiki.gg/wiki/Maintenance_Tunnel",
        "keywords": {'maintenance', 'tunnel'}
    },
    {
        "name": "Navy Pier",
        "url": "https://foxhole.wiki.gg/wiki/Navy_Pier",
        "keywords": {'pier', 'navy'}
    },
    {
        "name": "Pipeline",
        "url": "https://foxhole.wiki.gg/wiki/Pipeline",
        "keywords": {'pipeline'}
    },
    {
        "name": "Pipeline (Overhead)",
        "url": "https://foxhole.wiki.gg/wiki/Pipeline_(Overhead)",
        "keywords": {'overhead', 'pipeline'}
    },
    {
        "name": "Pipeline (Underground)",
        "url": "https://foxhole.wiki.gg/wiki/Pipeline_(Underground)",
        "keywords": {'underground', 'pipeline'}
    },
    {
        "name": "Pipeline Valve",
        "url": "https://foxhole.wiki.gg/wiki/Pipeline_Valve",
        "keywords": {'valve', 'pipeline'}
    },
    {
        "name": "Power Pole",
        "url": "https://foxhole.wiki.gg/wiki/Power_Pole",
        "keywords": {'power', 'pole'}
    },
    {
        "name": "Power Switch",
        "url": "https://foxhole.wiki.gg/wiki/Power_Switch",
        "keywords": {'switch', 'power'}
    },
    {
        "name": "Provisional Road",
        "url": "https://foxhole.wiki.gg/wiki/Provisional_Road",
        "keywords": {'provisional', 'road'}
    },
    {
        "name": "Railway Track",
        "url": "https://foxhole.wiki.gg/wiki/Railway_Track",
        "keywords": {'track', 'railway', 'large'}
    },
    {
        "name": "Railway Track (Biarc)",
        "url": "https://foxhole.wiki.gg/wiki/Railway_Track_(Biarc)",
        "keywords": {'track', 'railway', 'large', 'biarc'}
    },
    {
        "name": "Railway Track (Foundation)",
        "url": "https://foxhole.wiki.gg/wiki/Railway_Track_(Foundation)",
        "keywords": {'track', 'railway', 'large', 'foundation'}
    },
    {
        "name": "Small Gauge Railway Track",
        "url": "https://foxhole.wiki.gg/wiki/Small_Gauge_Railway_Track",
        "keywords": {'small', 'gauge', 'railway', 'track'}
    },
    {
        "name": "Small Gauge Railway Track (Biarc)",
        "url": "https://foxhole.wiki.gg/wiki/Small_Gauge_Railway_Track_(Biarc)",
        "keywords": {'small', 'gauge', 'railway', 'track', 'biarc'}
    },
    {
        "name": "Small Gauge Railway Track (Foundation)",
        "url": "https://foxhole.wiki.gg/wiki/Small_Gauge_Railway_Track_(Foundation)",
        "keywords": {'small', 'gauge', 'railway', 'track', 'foundation'}
    },
    {
        "name": "Deployed Tripod",
        "url": "https://foxhole.wiki.gg/wiki/Deployed_Tripod",
        "keywords": {'deployed', 'tripod'}
    },
    {
        "name": "Field Range",
        "url": "https://foxhole.wiki.gg/wiki/Field_Range",
        "keywords": {'range', 'field'}
    },
]

ALL_WIKI_ENTRIES = ITEMS_WIKI_ENTRIES + VEHICLES_WIKI_ENTRIES + STRUCTURES_WIKI_ENTRIES
