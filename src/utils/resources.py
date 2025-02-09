import pathlib

from .oisol_enums import DamageTypes


OISOL_HOME_PATH = pathlib.Path('/') / 'oisol'
TODOLIST_MAXIMUM_TASKS_ON_INTERFACE = 24


DAMAGE_TYPES_ATTRIBUTION = {
    '.44': DamageTypes.LIGHT_KINETIC.value,
    '7.62mm': DamageTypes.LIGHT_KINETIC.value,
    '7.92mm': DamageTypes.LIGHT_KINETIC.value,
    '8mm': DamageTypes.LIGHT_KINETIC.value,
    '9mm': DamageTypes.LIGHT_KINETIC.value,
    'A3 Harpa Fragmentation Grenade': DamageTypes.LIGHT_KINETIC.value,
    'Buckshot': DamageTypes.LIGHT_KINETIC.value,
    "Crow's Foot Mine": DamageTypes.LIGHT_KINETIC.value,
    '12.7mm': DamageTypes.HEAVY_KINETIC.value,
    '20mm': DamageTypes.ANTI_TANK_KINETIC.value,
    'Garrisoned House': DamageTypes.ANTI_TANK_KINETIC_STRUCTURE.value,
    'Safe House': DamageTypes.ANTI_TANK_KINETIC_STRUCTURE.value,
    'Town Base': DamageTypes.ANTI_TANK_KINETIC_STRUCTURE.value,
    'Anti-Tank Pillbox': DamageTypes.ANTI_TANK_KINETIC_STRUCTURE.value,
    'Bomastone Grenade': DamageTypes.SHRAPNEL.value,
    'Shrapnel Mortar Shell': DamageTypes.SHRAPNEL.value,
    'Flare Mortar Shell': DamageTypes.FLARE.value,
    'Green Ash Grenade': DamageTypes.POISONOUS_GAS.value,
    '30mm': DamageTypes.EXPLOSIVE.value,
    '40mm': DamageTypes.EXPLOSIVE.value,
    '75mm': DamageTypes.EXPLOSIVE.value,
    'Mammon 91-b': DamageTypes.EXPLOSIVE.value,
    'RPG': DamageTypes.EXPLOSIVE.value,
    'Tremola Grenade GPb-1': DamageTypes.EXPLOSIVE.value,
    '120mm': DamageTypes.HIGH_EXPLOSIVE.value,
    '150mm': DamageTypes.HIGH_EXPLOSIVE.value,
    '300mm': DamageTypes.HIGH_EXPLOSIVE.value,
    'E680-S Rudder Lock': DamageTypes.HIGH_EXPLOSIVE.value,
    'Sea Mine': DamageTypes.HIGH_EXPLOSIVE.value,  # Alias of E680-S Rudder Lock
    'Model-7 “Evie”': DamageTypes.HIGH_EXPLOSIVE.value,
    'Depth Charge': DamageTypes.HIGH_EXPLOSIVE.value,  # Alias of Model-7 “Evie”
    'Moray Torpedo': DamageTypes.HIGH_EXPLOSIVE.value,
    'Torpedo': DamageTypes.HIGH_EXPLOSIVE.value,  # Alias of Moray Torpedo
    'Mortar Shell': DamageTypes.HIGH_EXPLOSIVE.value,
    '250mm': DamageTypes.DEMOLITION.value,
    'Alligator Charge': DamageTypes.DEMOLITION.value,
    'Havoc Charge': DamageTypes.DEMOLITION.value,
    "Hydra's Whisper": DamageTypes.DEMOLITION.value,
    '68mm': DamageTypes.ARMOUR_PIERCING.value,
    '94.5mm': DamageTypes.ARMOUR_PIERCING.value,
    'AP⧸RPG': DamageTypes.ARMOUR_PIERCING.value,
    'ARC⧸RPG': DamageTypes.ARMOUR_PIERCING.value,
    'Ignifist 30': DamageTypes.ARMOUR_PIERCING.value,
    'Abisme AT-99': DamageTypes.ANTI_TANK_EXPLOSIVE.value,
    'Anti-Tank Sticky Bomb': DamageTypes.ANTI_TANK_EXPLOSIVE.value,
    'B2 Varsi Anti-Tank Grenade': DamageTypes.ANTI_TANK_EXPLOSIVE.value,
    'BF5 White Ash Flask Grenade': DamageTypes.ANTI_TANK_EXPLOSIVE.value,
    'Flamethrower Ammo': DamageTypes.INCENDIARY.value,  # Alias of Willow's Bane Ammo & “Molten Wind” v.II Ammo
    '“Molten Wind” v.II Ammo': DamageTypes.INCENDIARY.value,
    'Flame Ammo': DamageTypes.INCENDIARY.value,
    "Willow's Bane Ammo": DamageTypes.INCENDIARY.value,
    '3C-High Explosive Rocket': DamageTypes.INCENDIARY_HIGH_EXPLOSIVE.value,
    '4C-Fire Rocket': DamageTypes.INCENDIARY_HIGH_EXPLOSIVE.value,
    'Incendiary Mortar Shell': DamageTypes.INCENDIARY_HIGH_EXPLOSIVE.value,
    'Buckhorn CCQ-18': DamageTypes.MELEE.value,
    'Eleos Infantry Dagger': DamageTypes.MELEE.value,
    'Falias Raiding Club': DamageTypes.MELEE.value,
    'Fists': DamageTypes.MELEE.value,
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


RESOURCE_TO_CRATE = {
    'Refined Materials': 20,
    'Basic Materials': 100,
    'Explosive Powder': 40,
    'Heavy Explosive Powder': 30,
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
    'Incendiary High Explosive': '<:incendiary_high_explosive:1317944748157173770>',
    'Incendiary': '<:incendiary:1239343406854049824>',
    'Flamethrower Ammo': '<:flamethrower_ammo:1317941667386490992>',
    'Flame Ammo': '<:flame_ammo:1317941665016844392>',
    'Shrapnel Mortar Shell': '<:shrapnel_mortar:1317941666019152012>',
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
    'Crate': '<:crate:1327695652494508085>',
    'Refined Materials': '<:rmat:1239353730172715048>',
    'Basic Materials': '<:bmat:1239353181474127943>',
    'Explosive Powder': '<:emat:1327687090590449818>',
    'Heavy Explosive Powder': '<:hemat:1327688754617647184>',
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
    'Mass Production Factory': '<:mpf:1239655209903456267>',
    'Factory': '<:factory_building:1239655208485781575>',
    'Garage': '<:garage:1078410297099948032>',
    'MW of power': '<:mw_of_power:1327439074184794185>',
    'Small Assembly Station': '<:lightassembly:1196074987879153724>',
    'Infantry Arms Factory': '<:infantry_arms_factory:1327437914719780884>',
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
    'Bomastone Grenade': '<:bomastone:1317941669785501840>',
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
    '🇿': 'TodoButtonZ',
}


ITEMS_WIKI_ENTRIES = [
    {
        'name': 'Argenti r.II Rifle',
        'url': 'https://foxhole.wiki.gg/wiki/Argenti_r.II_Rifle',
        'keywords': 'colonialrifleargenti',
    },
    {
        'name': 'Blakerow 871',
        'url': 'https://foxhole.wiki.gg/wiki/Blakerow_871',
        'keywords': 'rifleblakerowwarden',
    },
    {
        'name': 'Catena rt.IV Auto-Rifle',
        'url': 'https://foxhole.wiki.gg/wiki/Catena_rt.IV_Auto-Rifle',
        'keywords': 'colonialcatenarifleauto',
    },
    {
        'name': 'Fuscina pi.I',
        'url': 'https://foxhole.wiki.gg/wiki/Fuscina_pi.I',
        'keywords': 'colonialfusinafucinariflefuscina',
    },
    {
        'name': 'No.2 Loughcaster',
        'url': 'https://foxhole.wiki.gg/wiki/No.2_Loughcaster',
        'keywords': 'loughcasterriflewarden',
    },
    {
        'name': 'No.2B Hawthorne',
        'url': 'https://foxhole.wiki.gg/wiki/No.2B_Hawthorne',
        'keywords': 'riflehawthornewarden',
    },
    {
        'name': 'Sampo Auto-Rifle 77',
        'url': 'https://foxhole.wiki.gg/wiki/Sampo_Auto-Rifle_77',
        'keywords': 'autoriflesampowarden',
    },
    {
        'name': 'The Hangman 757',
        'url': 'https://foxhole.wiki.gg/wiki/The_Hangman_757',
        'keywords': 'riflewardenheavythehangman',
    },
    {
        'name': 'Volta r.I Repeater',
        'url': 'https://foxhole.wiki.gg/wiki/Volta_r.I_Repeater',
        'keywords': 'colonialriflerepeaterheavyvolta',
    },
    {
        'name': 'Clancy Cinder M3',
        'url': 'https://foxhole.wiki.gg/wiki/Clancy_Cinder_M3',
        'keywords': 'longcinderclancywardenrifle',
    },
    {
        'name': 'KRR2-790 Omen',
        'url': 'https://foxhole.wiki.gg/wiki/KRR2-790_Omen',
        'keywords': 'coloniallongrifleomen',
    },
    {
        'name': 'Clancy-Raca M4',
        'url': 'https://foxhole.wiki.gg/wiki/Clancy-Raca_M4',
        'keywords': 'clancysniperwardenrifleraca',
    },
    {
        'name': 'KRR3-792 Auger',
        'url': 'https://foxhole.wiki.gg/wiki/KRR3-792_Auger',
        'keywords': 'colonialrifleaugersniper',
    },
    {
        'name': '“Lionclaw” mc.VIII',
        'url': 'https://foxhole.wiki.gg/wiki/%E2%80%9CLionclaw%E2%80%9D_mc.VIII',
        'keywords': 'colonialgunlionclawsubmachine',
    },
    {
        'name': '“The Pitch Gun” mc.V',
        'url': 'https://foxhole.wiki.gg/wiki/%E2%80%9CThe_Pitch_Gun%E2%80%9D_mc.V',
        'keywords': 'colonialgunpitchsubmachine',
    },
    {
        'name': 'Fiddler Submachine Gun Model 868',
        'url': 'https://foxhole.wiki.gg/wiki/Fiddler_Submachine_Gun_Model_868',
        'keywords': 'gunfiddlersubmachinewarden',
    },
    {
        'name': 'No.1 “The Liar” Submachine Gun',
        'url': 'https://foxhole.wiki.gg/wiki/No.1_%E2%80%9CThe_Liar%E2%80%9D_Submachine_Gun',
        'keywords': 'wardengunliarsubmachine',
    },
    {
        'name': '“Dusk” ce.III',
        'url': 'https://foxhole.wiki.gg/wiki/%E2%80%9CDusk%E2%80%9D_ce.III',
        'keywords': 'colonialrifleassaultdusk',
    },
    {
        'name': 'Aalto Storm Rifle 24',
        'url': 'https://foxhole.wiki.gg/wiki/Aalto_Storm_Rifle_24',
        'keywords': 'stormwardenrifleaaltoassault',
    },
    {
        'name': 'Booker Storm Rifle Model 838',
        'url': 'https://foxhole.wiki.gg/wiki/Booker_Storm_Rifle_Model_838',
        'keywords': 'stormbookerwardenrifleassault',
    },
    {
        'name': 'KRF1-750 Dragonfly',
        'url': 'https://foxhole.wiki.gg/wiki/KRF1-750_Dragonfly',
        'keywords': 'colonialshotgundragonfly',
    },
    {
        'name': 'No.4 The Pillory Scattergun',
        'url': 'https://foxhole.wiki.gg/wiki/No.4_The_Pillory_Scattergun',
        'keywords': 'wardenpilloryscattergunshotgun',
    },
    {
        'name': 'Cascadier 873',
        'url': 'https://foxhole.wiki.gg/wiki/Cascadier_873',
        'keywords': 'cascadierpistolwarden',
    },
    {
        'name': 'Cometa T2-9',
        'url': 'https://foxhole.wiki.gg/wiki/Cometa_T2-9',
        'keywords': 'revolvercometapistol',
    },
    {
        'name': 'Catara mo.II',
        'url': 'https://foxhole.wiki.gg/wiki/Catara_mo.II',
        'keywords': 'machinecolonialguncataralmglight',
    },
    {
        'name': 'KRN886-127 Gast Machine Gun',
        'url': 'https://foxhole.wiki.gg/wiki/KRN886-127_Gast_Machine_Gun',
        'keywords': 'machinecolonialgungastmg',
    },
    {
        'name': 'Malone MK.2',
        'url': 'https://foxhole.wiki.gg/wiki/Malone_MK.2',
        'keywords': 'machinegunwardenmalonemg',
    },
    {
        'name': '20 Neville Anti-Tank Rifle',
        'url': 'https://foxhole.wiki.gg/wiki/20_Neville_Anti-Tank_Rifle',
        'keywords': 'wardennevilleatrrifleantitank',
    },
    {
        'name': '228 Satterley Heavy Storm Rifle',
        'url': 'https://foxhole.wiki.gg/wiki/228_Satterley_Heavy_Storm_Rifle',
        'keywords': 'scatterleywardenatrheavyantitankstormrifle',
    },
    {
        'name': 'Booker Greyhound Model 910',
        'url': 'https://foxhole.wiki.gg/wiki/Booker_Greyhound_Model_910',
        'keywords': 'stormbookerwardenatrrifleantitank',
    },
    {
        'name': '“Dawn” Ve.II',
        'url': 'https://foxhole.wiki.gg/wiki/%E2%80%9CDawn%E2%80%9D_Ve.II',
        'keywords': 'colonialdawnatrrifleantitank',
    },
    {
        'name': '“Quickhatch” Rt.I',
        'url': 'https://foxhole.wiki.gg/wiki/%E2%80%9CQuickhatch%E2%80%9D_Rt.I',
        'keywords': 'colonialquickhatchsniperatrrifleantitank',
    },
    {
        'name': 'Lamentum mm.IV',
        'url': 'https://foxhole.wiki.gg/wiki/Lamentum_mm.IV',
        'keywords': 'machinelamentumcolonialgunmountedmg',
    },
    {
        'name': 'Malone Ratcatcher MK.1',
        'url': 'https://foxhole.wiki.gg/wiki/Malone_Ratcatcher_MK.1',
        'keywords': 'machineratcatchergunwardenmountedmalonemg',
    },
    {
        'name': 'Mounted Fissura gd.I',
        'url': 'https://foxhole.wiki.gg/wiki/Mounted_Fissura_gd.I',
        'keywords': 'fissuracoloniallaunchermountedgrenade',
    },
    {
        'name': 'Daucus isg.III',
        'url': 'https://foxhole.wiki.gg/wiki/Daucus_isg.III',
        'keywords': 'colonialguninfantrydaucusmountedisgsupport',
    },
    {
        'name': 'Cutler Foebreaker',
        'url': 'https://foxhole.wiki.gg/wiki/Cutler_Foebreaker',
        'keywords': 'cutlerfoebreakerlauncherwardenrpgmounted',
    },
    {
        'name': 'Mounted Bonesaw MK.3',
        'url': 'https://foxhole.wiki.gg/wiki/Mounted_Bonesaw_MK.3',
        'keywords': 'arclauncherrpgwardenmountedbonesaw',
    },
    {
        'name': '“Typhon” ra.XII',
        'url': 'https://foxhole.wiki.gg/wiki/%E2%80%9CTyphon%E2%80%9D_ra.XII',
        'keywords': 'colonialtyphonmountedatrrifleantitank',
    },
    {
        'name': '“Molten Wind” v.II Flame Torch',
        'url': 'https://foxhole.wiki.gg/wiki/%E2%80%9CMolten_Wind%E2%80%9D_v.II_Flame_Torch',
        'keywords': 'flamethrowercolonialtorchwindthrowermoltenflame',
    },
    {
        'name': "Willow's Bane Model 845",
        'url': 'https://foxhole.wiki.gg/wiki/Willow%27s_Bane_Model_845',
        'keywords': 'flamethrowerwillowthrowermodelwardenbaneflame',
    },
    {
        'name': 'A3 Harpa Fragmentation Grenade',
        'url': 'https://foxhole.wiki.gg/wiki/A3_Harpa_Fragmentation_Grenade',
        'keywords': 'fragmentationharpawardena3grenade',
    },
    {
        'name': 'Bomastone Grenade',
        'url': 'https://foxhole.wiki.gg/wiki/Bomastone_Grenade',
        'keywords': 'colonialgrenadebomastone',
    },
    {
        'name': 'Green Ash Grenade',
        'url': 'https://foxhole.wiki.gg/wiki/Gas_Grenade',
        'keywords': 'grenadeashgasgreen',
    },
    {
        'name': 'PT-815 Smoke Grenade',
        'url': 'https://foxhole.wiki.gg/wiki/Smoke_Grenade',
        'keywords': 'smokegrenade',
    },
    {
        'name': 'Mammon 91-b',
        'url': 'https://foxhole.wiki.gg/wiki/Mammon_91-b',
        'keywords': 'grenadehemammonmamon',
    },
    {
        'name': 'Tremola Grenade GPb-1',
        'url': 'https://foxhole.wiki.gg/wiki/Tremola_Grenade_GPb-1',
        'keywords': 'grenadehetremola',
    },
    {
        'name': 'Anti-Tank Sticky Bomb',
        'url': 'https://foxhole.wiki.gg/wiki/Anti-Tank_Sticky_Bomb',
        'keywords': 'antistickybombtank',
    },
    {
        'name': 'BF5 White Ash Flask Grenade',
        'url': 'https://foxhole.wiki.gg/wiki/BF5_White_Ash_Flask_Grenade',
        'keywords': 'flaskwhitewardengrenadeashantitank',
    },
    {
        'name': 'B2 Varsi Anti-Tank Grenade',
        'url': 'https://foxhole.wiki.gg/wiki/B2_Varsi_Anti-Tank_Grenade',
        'keywords': 'grenadewardenantivarsitank',
    },
    {
        'name': 'Alligator Charge',
        'url': 'https://foxhole.wiki.gg/wiki/Alligator_Charge',
        'keywords': 'chargeexplosivealigatorwardenalligator',
    },
    {
        'name': "Hydra's Whisper",
        'url': 'https://foxhole.wiki.gg/wiki/Hydra%27s_Whisper',
        'keywords': 'colonialchargeexplosivehydrawhisper',
    },
    {
        'name': 'Havoc Charge',
        'url': 'https://foxhole.wiki.gg/wiki/Havoc_Charge',
        'keywords': 'chargeexplosivehavoc',
    },
    {
        'name': 'Abisme AT-99',
        'url': 'https://foxhole.wiki.gg/wiki/Abisme_AT-99',
        'keywords': 'abismeatmineantitank',
    },
    {
        'name': 'E680-S Rudder Lock',
        'url': 'https://foxhole.wiki.gg/wiki/Sea_Mine',
        'keywords': 'lockseaminenavalrudder',
    },
    {
        'name': "Crow's Foot Mine",
        'url': 'https://foxhole.wiki.gg/wiki/Crow%27s_Foot_Mine',
        'keywords': 'crowinfantrylandpersonnelfootmineanti',
    },
    {
        'name': 'The Ospreay',
        'url': 'https://foxhole.wiki.gg/wiki/The_Ospreay',
        'keywords': 'grenadeospreaylauncherwarden',
    },
    {
        'name': 'KLG901-2 Lunaire F',
        'url': 'https://foxhole.wiki.gg/wiki/KLG901-2_Lunaire_F',
        'keywords': 'colonialgrenadelauncherlunaire',
    },
    {
        'name': 'Cutler Launcher 4',
        'url': 'https://foxhole.wiki.gg/wiki/Cutler_Launcher_4',
        'keywords': 'cutlerrpglauncherwarden',
    },
    {
        'name': 'Bane 45',
        'url': 'https://foxhole.wiki.gg/wiki/Bane_45',
        'keywords': 'apantitankcolonialrpglauncheratbane',
    },
    {
        'name': 'Bonesaw MK.3',
        'url': 'https://foxhole.wiki.gg/wiki/Bonesaw_MK.3',
        'keywords': 'arclauncherrpgwardenbonesaw',
    },
    {
        'name': 'Ignifist 30',
        'url': 'https://foxhole.wiki.gg/wiki/Ignifist_30',
        'keywords': 'colonialignifistlauncherat',
    },
    {
        'name': 'Venom c.II 35',
        'url': 'https://foxhole.wiki.gg/wiki/Venom_c.II_35',
        'keywords': 'coloniallauncherrpgapatvenom',
    },
    {
        'name': 'Cremari Mortar',
        'url': 'https://foxhole.wiki.gg/wiki/Cremari_Mortar',
        'keywords': 'mortarcremari',
    },
    {
        'name': 'Buckhorn CCQ-18',
        'url': 'https://foxhole.wiki.gg/wiki/Bayonet',
        'keywords': 'buckhornbayonet',
    },
    {
        'name': 'Eleos Infantry Dagger',
        'url': 'https://foxhole.wiki.gg/wiki/Eleos_Infantry_Dagger',
        'keywords': 'colonialdaggermeleeinfantryeleosweapon',
    },
    {
        'name': 'Falias Raiding Club',
        'url': 'https://foxhole.wiki.gg/wiki/Falias_Raiding_Club',
        'keywords': 'meleeclubraidingwardenfaliasweapon',
    },
    {
        'name': '9mm',
        'url': 'https://foxhole.wiki.gg/wiki/9mm',
        'keywords': 'magazinemm9',
    },
    {
        'name': '8mm',
        'url': 'https://foxhole.wiki.gg/wiki/8mm',
        'keywords': 'magazinemm8',
    },
    {
        'name': '7.92mm',
        'url': 'https://foxhole.wiki.gg/wiki/7.92mm',
        'keywords': '7.92mm7magazine',
    },
    {
        'name': '7.62mm',
        'url': 'https://foxhole.wiki.gg/wiki/7.62mm',
        'keywords': 'magazine7mm7.62',
    },
    {
        'name': '.44',
        'url': 'https://foxhole.wiki.gg/wiki/.44',
        'keywords': 'magazinemm44',
    },
    {
        'name': 'Buckshot',
        'url': 'https://foxhole.wiki.gg/wiki/Buckshot',
        'keywords': 'buckshotammoshotgun',
    },
    {
        'name': 'Flame Ammo',
        'url': 'https://foxhole.wiki.gg/wiki/Flame_Ammo',
        'keywords': 'ammoflame',
    },
    {
        'name': '12.7mm',
        'url': 'https://foxhole.wiki.gg/wiki/12.7mm',
        'keywords': 'magazine1212.7mm',
    },
    {
        'name': '20mm',
        'url': 'https://foxhole.wiki.gg/wiki/20mm',
        'keywords': 'magazinemm20',
    },
    {
        'name': '30mm',
        'url': 'https://foxhole.wiki.gg/wiki/30mm',
        'keywords': 'shellmm30',
    },
    {
        'name': '40mm',
        'url': 'https://foxhole.wiki.gg/wiki/40mm',
        'keywords': 'shellmm40',
    },
    {
        'name': '68mm',
        'url': 'https://foxhole.wiki.gg/wiki/68mm',
        'keywords': 'shell68mm',
    },
    {
        'name': '75mm',
        'url': 'https://foxhole.wiki.gg/wiki/75mm',
        'keywords': 'shell75mm',
    },
    {
        'name': '94.5mm',
        'url': 'https://foxhole.wiki.gg/wiki/94.5mm',
        'keywords': '9494.5shellmm',
    },
    {
        'name': 'Flare Mortar Shell',
        'url': 'https://foxhole.wiki.gg/wiki/Flare_Mortar_Shell',
        'keywords': 'shellflaremortar',
    },
    {
        'name': 'Shrapnel Mortar Shell',
        'url': 'https://foxhole.wiki.gg/wiki/Shrapnel_Mortar_Shell',
        'keywords': 'shellmortarshrapnel',
    },
    {
        'name': 'Mortar Shell',
        'url': 'https://foxhole.wiki.gg/wiki/Mortar_Shell',
        'keywords': 'shellmortar',
    },
    {
        'name': 'Incendiary Mortar Shell',
        'url': 'https://foxhole.wiki.gg/wiki/Incendiary_Mortar_Shell',
        'keywords': 'fireshellmortarincendiary',
    },
    {
        'name': '4C-Fire Rocket',
        'url': 'https://foxhole.wiki.gg/wiki/4C-Fire_Rocket',
        'keywords': '4crocketfire',
    },
    {
        'name': '3C-High Explosive Rocket',
        'url': 'https://foxhole.wiki.gg/wiki/3C-High_Explosive_Rocket',
        'keywords': 'explosivefire3crockethigh',
    },
    {
        'name': '120mm',
        'url': 'https://foxhole.wiki.gg/wiki/120mm',
        'keywords': 'shellmm120',
    },
    {
        'name': '150mm',
        'url': 'https://foxhole.wiki.gg/wiki/150mm',
        'keywords': '150shellmm',
    },
    {
        'name': '300mm',
        'url': 'https://foxhole.wiki.gg/wiki/300mm',
        'keywords': 'shellmm300',
    },
    {
        'name': 'RPG',
        'url': 'https://foxhole.wiki.gg/wiki/RPG',
        'keywords': 'shellrpg',
    },
    {
        'name': 'AP⧸RPG',
        'url': 'https://foxhole.wiki.gg/wiki/AP%E2%A7%B8RPG',
        'keywords': 'shellrpgap',
    },
    {
        'name': 'ARC⧸RPG',
        'url': 'https://foxhole.wiki.gg/wiki/ARC%E2%A7%B8RPG',
        'keywords': 'arcshellrpg',
    },
    {
        'name': '250mm',
        'url': 'https://foxhole.wiki.gg/wiki/250mm',
        'keywords': 'shell250mm',
    },
    {
        'name': '“Molten Wind” v.II Ammo',
        'url': 'https://foxhole.wiki.gg/wiki/%E2%80%9CMolten_Wind%E2%80%9D_v.II_Ammo',
        'keywords': 'moltenammoflamewind',
    },
    {
        'name': "Willow's Bane Ammo",
        'url': 'https://foxhole.wiki.gg/wiki/Willow%27s_Bane_Ammo',
        'keywords': 'willowsflameammobane',
    },
    {
        'name': 'Moray Torpedo',
        'url': 'https://foxhole.wiki.gg/wiki/Torpedo',
        'keywords': 'torpedomoray',
    },
    {
        'name': 'Model-7 “Evie”',
        'url': 'https://foxhole.wiki.gg/wiki/Depth_Charge',
        'keywords': 'eviechargedepth',
    },
    {
        'name': 'A0E-9 Rocket Booster',
        'url': 'https://foxhole.wiki.gg/wiki/A0E-9_Rocket_Booster',
        'keywords': 'nukeboosterrocket',
    },
    {
        'name': 'A0E-9 Rocket Body',
        'url': 'https://foxhole.wiki.gg/wiki/A0E-9_Rocket_Body',
        'keywords': 'nukerocketbody',
    },
    {
        'name': 'A0E-9 Rocket Warhead',
        'url': 'https://foxhole.wiki.gg/wiki/A0E-9_Rocket_Warhead',
        'keywords': 'nukewarheadrocket',
    },
    {
        'name': 'Deployed Listening Kit',
        'url': 'https://foxhole.wiki.gg/wiki/Listening_Kit',
        'keywords': 'deployedlklisteningkit',
    },
    {
        'name': 'Tripod',
        'url': 'https://foxhole.wiki.gg/wiki/Tripod',
        'keywords': 'tripod',
    },
]


# Specific entries that should only be handled within the wiki command
PLACEHOLDER_ENTRIES = [
    {
        'name': 'Power Station',
        'url': 'https://foxhole.wiki.gg/wiki/Power_Station',
        'keywords': 'powerstation',
    },
    {
        'name': 'A0E-9 Rocket Platform',
        'url': 'https://foxhole.wiki.gg/wiki/A0E-9_Rocket_Platform',
        'keywords': 'nukerocketplatform',
    },
    {
        'name': 'Diesel Power Plant',
        'url': 'https://foxhole.wiki.gg/wiki/Diesel_Power_Plant',
        'keywords': 'powerdieselplant',
    },
    {
        'name': 'Heavy Infantry Carrier',
        'url': 'https://foxhole.wiki.gg/wiki/Heavy_Infantry_Carrier',
        'keywords': 'vehiclerelicinfantrycarrierheavy',
    },
    {
        'name': 'Oil Field',
        'url': 'https://foxhole.wiki.gg/wiki/Oil_Field',
        'keywords': 'oilfield',
    },
    {
        'name': 'Coal Field',
        'url': 'https://foxhole.wiki.gg/wiki/Coal_Field',
        'keywords': 'coalfield',
    },
    {
        'name': 'Salvage Field',
        'url': 'https://foxhole.wiki.gg/wiki/Salvage_Field',
        'keywords': 'fieldscrapsalvage',
    },
    {
        'name': 'Sulfur Field',
        'url': 'https://foxhole.wiki.gg/wiki/Sulfur_Field',
        'keywords': 'sulfurfield',
    },
    {
        'name': 'Component Field',
        'url': 'https://foxhole.wiki.gg/wiki/Component_Field',
        'keywords': 'componentfield',
    },
    {
        'name': 'Herne QMW 1a Scourge Hunter',
        'url': 'https://foxhole.wiki.gg/wiki/Herne_QMW_1a_Scourge_Hunter',
        'keywords': 'scourgemechahunterherne',
    },
    {
        'name': 'Centurion MV-2',
        'url': 'https://foxhole.wiki.gg/wiki/Centurion_MV-2',
        'keywords': 'centurionmecha',
    },
    {
        'name': 'Fists',
        'url': 'https://foxhole.wiki.gg/wiki/Fists',
        'keywords': 'fists',
    },
    {
        'name': 'Ferro 879',
        'url': 'https://foxhole.wiki.gg/wiki/Ferro_879',
        'keywords': 'colonialferropistol',
    },
    {
        'name': 'Ahti Model 2',
        'url': 'https://foxhole.wiki.gg/wiki/Ahti_Model_2',
        'keywords': 'wardenatipistolahti',
    },
    {
        'name': 'Blumfield LK205',
        'url': 'https://foxhole.wiki.gg/wiki/Bicycle',
        'keywords': 'blumfieldcolonialwardenbicycle',
    },
]


FACILITY_MATERIAL_ENTRIES = [
    {
        'name': 'Diesel',
        'url': 'https://foxhole.wiki.gg/wiki/Diesel',
        'keywords': 'dieselfuel',
    },
    {
        'name': 'Petrol',
        'url': 'https://foxhole.wiki.gg/wiki/Petrol',
        'keywords': 'petrolfuel',
    },
    {
        'name': 'Oil',
        'url': 'https://foxhole.wiki.gg/wiki/Oil',
        'keywords': 'oil',
    },
    {
        'name': 'Heavy Oil',
        'url': 'https://foxhole.wiki.gg/wiki/Heavy_Oil',
        'keywords': 'heavyhoil',
    },
    {
        'name': 'Enriched Oil',
        'url': 'https://foxhole.wiki.gg/wiki/Enriched_Oil',
        'keywords': 'enrichedeoil',
    },
    {
        'name': 'Coal',
        'url': 'https://foxhole.wiki.gg/wiki/Coal',
        'keywords': 'coal',
    },
    {
        'name': 'Coke',
        'url': 'https://foxhole.wiki.gg/wiki/Coke',
        'keywords': 'coke',
    },
    {
        'name': 'Components',
        'url': 'https://foxhole.wiki.gg/wiki/Components',
        'keywords': 'components',
    },
    {
        'name': 'Salvage',
        'url': 'https://foxhole.wiki.gg/wiki/Salvage',
        'keywords': 'salvagescroopscrap',
    },
    {
        'name': 'Sulfur',
        'url': 'https://foxhole.wiki.gg/wiki/Sulfur',
        'keywords': 'sulfur',
    },
    {
        'name': 'Water',
        'url': 'https://foxhole.wiki.gg/wiki/Water',
        'keywords': 'water',
    },
    {
        'name': 'Construction Materials',
        'url': 'https://foxhole.wiki.gg/wiki/Construction_Materials',
        'keywords': 'constructionmaterialscmats',
    },
    {
        'name': 'Processed Construction Materials',
        'url': 'https://foxhole.wiki.gg/wiki/Processed_Construction_Materials',
        'keywords': 'processedconstructionmaterialspcmats',
    },
    {
        'name': 'Steel Construction Materials',
        'url': 'https://foxhole.wiki.gg/wiki/Steel_Construction_Materials',
        'keywords': 'steelconstructionmaterialsscmats',
    },
    {
        'name': 'Assembly Materials I',
        'url': 'https://foxhole.wiki.gg/wiki/Assembly_Materials_I',
        'keywords': 'amatsasmatsassemblymaterialsi1',
    },
    {
        'name': 'Assembly Materials II',
        'url': 'https://foxhole.wiki.gg/wiki/Assembly_Materials_II',
        'keywords': 'amatsasmatsassemblymaterialsii2',
    },
    {
        'name': 'Assembly Materials III',
        'url': 'https://foxhole.wiki.gg/wiki/Assembly_Materials_III',
        'keywords': 'amatsasmatsassemblymaterialsiii3',
    },
    {
        'name': 'Assembly Materials IV',
        'url': 'https://foxhole.wiki.gg/wiki/Assembly_Materials_IV',
        'keywords': 'amatsasmatsassemblymaterialsiv4',
    },
    {
        'name': 'Assembly Materials V',
        'url': 'https://foxhole.wiki.gg/wiki/Assembly_Materials_V',
        'keywords': 'amatsasmatsassemblymaterialsv5',
    },
    {
        'name': 'Thermal Shielding',
        'url': 'https://foxhole.wiki.gg/wiki/Thermal_Shielding',
        'keywords': 'thermalshielding',
    },
    {
        'name': 'Naval Hull Segments',
        'url': 'https://foxhole.wiki.gg/wiki/Naval_Hull_Segments',
        'keywords': 'navalhullsegments',
    },
    {
        'name': 'Naval Shell Plating',
        'url': 'https://foxhole.wiki.gg/wiki/Naval_Shell_Plating',
        'keywords': 'navalshellplating',
    },
    {
        'name': 'Naval Turbine Components',
        'url': 'https://foxhole.wiki.gg/wiki/Naval_Turbine_Components',
        'keywords': 'navalturbinecomponents',
    },
]


VEHICLES_WIKI_ENTRIES = [
    {
        'name': 'T3 “Xiphos”',
        'url': 'https://foxhole.wiki.gg/wiki/T3_%E2%80%9CXiphos%E2%80%9D',
        'keywords': 'colonialt3armouredarmoredxiphoscarac',
    },
    {
        'name': 'T5 “Percutio”',
        'url': 'https://foxhole.wiki.gg/wiki/T5_%E2%80%9CPercutio%E2%80%9D',
        'keywords': 'colonialatacarmouredt5carpercutioarmored',
    },
    {
        'name': 'T8 “Gemini”',
        'url': 'https://foxhole.wiki.gg/wiki/T8_%E2%80%9CGemini%E2%80%9D',
        'keywords': 'colonialgeminiarmouredt8caracarmored',
    },
    {
        'name': "O'Brien V.110",
        'url': 'https://foxhole.wiki.gg/wiki/O%27Brien_V.110',
        'keywords': 'warden110armouredarmoredcaracobrien',
    },
    {
        'name': "O'Brien V.113 Gravekeeper",
        'url': 'https://foxhole.wiki.gg/wiki/O%27Brien_V.113_Gravekeeper',
        'keywords': 'gravekeeperarmouredcaracwarden113bonewagonobrienamored',
    },
    {
        'name': "O'Brien V.121 Highlander",
        'url': 'https://foxhole.wiki.gg/wiki/O%27Brien_V.121_Highlander',
        'keywords': 'armoured121carhighlandertacwardenobrienamored',
    },
    {
        'name': "O'Brien V.130 Wild Jack",
        'url': 'https://foxhole.wiki.gg/wiki/O%27Brien_V.130_Wild_Jack',
        'keywords': 'armouredflamecaracwardenarmoredwildjackobrien130',
    },
    {
        'name': "O'Brien V.190 Knave",
        'url': 'https://foxhole.wiki.gg/wiki/O%27Brien_V.190_Knave',
        'keywords': '190carwardenarmoredknavegacglacobrien',
    },
    {
        'name': "O'Brien V.101 Freeman",
        'url': 'https://foxhole.wiki.gg/wiki/O%27Brien_V.101_Freeman',
        'keywords': 'freemanarmouredcar101hacwardenarmoredobrien',
    },
    {
        'name': 'T12 “Actaeon” Tankette',
        'url': 'https://foxhole.wiki.gg/wiki/T12_%E2%80%9CActaeon%E2%80%9D_Tankette',
        'keywords': 'colonialtankettet12actaeon',
    },
    {
        'name': 'T13 “Deioneus” Rocket Battery',
        'url': 'https://foxhole.wiki.gg/wiki/T13_%E2%80%9CDeioneus%E2%80%9D_Rocket_Battery',
        'keywords': 'colonialrockettankettet13deioneusbattery',
    },
    {
        'name': 'T14 “Vesta” Tankette',
        'url': 'https://foxhole.wiki.gg/wiki/T14_%E2%80%9CVesta%E2%80%9D_Tankette',
        'keywords': 'colonialtankettet14flamevesta',
    },
    {
        'name': 'T20 “Ixion” Tankette',
        'url': 'https://foxhole.wiki.gg/wiki/T20_%E2%80%9CIxion%E2%80%9D_Tankette',
        'keywords': 'colonialtankettet2030mmixion',
    },
    {
        'name': 'AB-8 “Acheron”',
        'url': 'https://foxhole.wiki.gg/wiki/AB-8_%E2%80%9CAcheron%E2%80%9D',
        'keywords': 'colonialapcacheronab8',
    },
    {
        'name': 'AB-11 “Doru”',
        'url': 'https://foxhole.wiki.gg/wiki/AB-11_%E2%80%9CDoru%E2%80%9D',
        'keywords': 'colonialapc12.7ab11dorumm',
    },
    {
        'name': 'Mulloy LPC',
        'url': 'https://foxhole.wiki.gg/wiki/Mulloy_LPC',
        'keywords': 'apcwardenmulloylpc',
    },
    {
        'name': 'HH-a “Javelin”',
        'url': 'https://foxhole.wiki.gg/wiki/HH-a_%E2%80%9CJavelin%E2%80%9D',
        'keywords': 'colonialhalftrackhtjavelin',
    },
    {
        'name': 'HH-b “Hoplite”',
        'url': 'https://foxhole.wiki.gg/wiki/HH-b_%E2%80%9CHoplite%E2%80%9D',
        'keywords': 'colonialhalftrackhopliteht',
    },
    {
        'name': 'HH-d “Peltast”',
        'url': 'https://foxhole.wiki.gg/wiki/HH-d_%E2%80%9CPeltast%E2%80%9D',
        'keywords': 'colonialhalftrackmortartmhtpeltast',
    },
    {
        'name': 'Niska Mk. I Gun Motor Carriage',
        'url': 'https://foxhole.wiki.gg/wiki/Niska_Mk._I_Gun_Motor_Carriage',
        'keywords': 'halftrackwardenhtcarriageniskagunmotor',
    },
    {
        'name': 'Niska Mk. II Blinder',
        'url': 'https://foxhole.wiki.gg/wiki/Niska_Mk._II_Blinder',
        'keywords': 'halftrackwarden68mmniskablinderatht',
    },
    {
        'name': 'Niska Mk. III Scar Twin',
        'url': 'https://foxhole.wiki.gg/wiki/Niska_Mk._III_Scar_Twin',
        'keywords': 'halftrackwardenhtniskatwinscar',
    },
    {
        'name': 'Niska-Rycker Mk. IX Skycaller',
        'url': 'https://foxhole.wiki.gg/wiki/Niska-Rycker_Mk._IX_Skycaller',
        'keywords': 'skycallerhalftrackrockethtwardenniskarycker',
    },
    {
        'name': 'Swallowtail 988/127-2',
        'url': 'https://foxhole.wiki.gg/wiki/Swallowtail_988/127-2',
        'keywords': 'wardenfieldfmgswallotailgunmachine',
    },
    {
        'name': 'G40 “Sagittarii”',
        'url': 'https://foxhole.wiki.gg/wiki/G40_%E2%80%9CSagittarii%E2%80%9D',
        'keywords': 'colonialsagittariig40fieldfmggunmachine',
    },
    {
        'name': "Duncan's Coin 20mm",
        'url': 'https://foxhole.wiki.gg/wiki/Duncan%27s_Coin_20mm',
        'keywords': 'tank20mmfieldfatrantiwardencoinduncans',
    },
    {
        'name': 'GA6 “Cestus”',
        'url': 'https://foxhole.wiki.gg/wiki/GA6_%E2%80%9CCestus%E2%80%9D',
        'keywords': 'tankcolonialga6fieldfatranticestus',
    },
    {
        'name': '120-68 “Koronides” Field Gun',
        'url': 'https://foxhole.wiki.gg/wiki/Field_Artillery',
        'keywords': 'colonialkoronidesartyfieldartillery120gun',
    },
    {
        'name': 'Balfour Wolfhound 40mm',
        'url': 'https://foxhole.wiki.gg/wiki/Field_Cannon',
        'keywords': 'pushgunbalfourwardenwolfhoundfieldcannon40mm',
    },
    {
        'name': 'Rycker 4/3-F Wasp Nest',
        'url': 'https://foxhole.wiki.gg/wiki/Field_Launcher',
        'keywords': 'wasprocketfieldwardenlauncherryckernest',
    },
    {
        'name': 'Collins Cannon 68mm',
        'url': 'https://foxhole.wiki.gg/wiki/Collins_Cannon_68mm',
        'keywords': 'tankfieldanticannonwarden68mmfatcollins',
    },
    {
        'name': 'AA-2 Battering Ram',
        'url': 'https://foxhole.wiki.gg/wiki/AA-2_Battering_Ram',
        'keywords': 'tankcolonialbatteringfatfieldantiram',
    },
    {
        'name': 'Balfour Falconer 250mm',
        'url': 'https://foxhole.wiki.gg/wiki/Field_Mortar',
        'keywords': 'falconerbarlfourfmpushgunwardenbaby250mmballista',
    },
    {
        'name': 'Balfour Rampart 68mm',
        'url': 'https://foxhole.wiki.gg/wiki/Heavy_Field_Cannon',
        'keywords': 'pushgunbalfourhv68wardenrampart68mmhvfat',
    },
    {
        'name': '40-45 “Smelter” Heavy Field Gun',
        'url': 'https://foxhole.wiki.gg/wiki/Heavy_Field_Gun',
        'keywords': 'colonialpushgunheavyfieldsmeltergunhv40',
    },
    {
        'name': 'Balfour Stockade 75mm',
        'url': 'https://foxhole.wiki.gg/wiki/Balfour_Stockade_75mm',
        'keywords': 'stockadefield75mmlargegunpushgunbalfourwarden',
    },
    {
        'name': '945g “Stygian Bolt”',
        'url': 'https://foxhole.wiki.gg/wiki/945g_%E2%80%9CStygian_Bolt%E2%80%9D',
        'keywords': 'colonialfieldlargeboltgun945gpushgunstygian',
    },
    {
        'name': 'King Spire Mk. I',
        'url': 'https://foxhole.wiki.gg/wiki/King_Spire_Mk._I',
        'keywords': 'tankscoutkingwardenspiremgst',
    },
    {
        'name': 'King Gallant Mk. II',
        'url': 'https://foxhole.wiki.gg/wiki/King_Gallant_Mk._II',
        'keywords': 'tankscoutkingwarden30mmgallant',
    },
    {
        'name': 'King Jester - Mk. I-1',
        'url': 'https://foxhole.wiki.gg/wiki/King_Jester_-_Mk._I-1',
        'keywords': 'tankscoutkingwardenrocketjester',
    },
    {
        'name': 'H-5 “Hatchet”',
        'url': 'https://foxhole.wiki.gg/wiki/H-5_%E2%80%9CHatchet%E2%80%9D',
        'keywords': 'tankcolonialh5lightlthatchet',
    },
    {
        'name': 'H-10 “Pelekys”',
        'url': 'https://foxhole.wiki.gg/wiki/H-10_%E2%80%9CPelekys%E2%80%9D',
        'keywords': 'tankpelekyscolonialdestroyerlightltdh10',
    },
    {
        'name': 'H-19 “Vulcan”',
        'url': 'https://foxhole.wiki.gg/wiki/H-19_%E2%80%9CVulcan%E2%80%9D',
        'keywords': 'tankcoloniallightvulcanh19flamelt',
    },
    {
        'name': 'H-8 “Kranesca”',
        'url': 'https://foxhole.wiki.gg/wiki/H-8_%E2%80%9CKranesca%E2%80%9D',
        'keywords': 'tankcoloniallightkrannylth8kranesca',
    },
    {
        'name': 'Devitt Mk. III',
        'url': 'https://foxhole.wiki.gg/wiki/Devitt_Mk._III',
        'keywords': 'tankwardenlightltdevitt',
    },
    {
        'name': 'Devitt Ironhide Mk. IV',
        'url': 'https://foxhole.wiki.gg/wiki/Devitt_Ironhide_Mk._IV',
        'keywords': 'tankwardenlightltdevittironhide',
    },
    {
        'name': 'Devitt-Caine Mk. IV MMR',
        'url': 'https://foxhole.wiki.gg/wiki/Devitt-Caine_Mk._IV_MMR',
        'keywords': 'tankwardencainelightmortardevittmlt',
    },
    {
        'name': '85K-b “Falchion”',
        'url': 'https://foxhole.wiki.gg/wiki/85K-b_%E2%80%9CFalchion%E2%80%9D',
        'keywords': 'tankcolonialassaultmpt85kbfalchion',
    },
    {
        'name': '85K-a “Spatha”',
        'url': 'https://foxhole.wiki.gg/wiki/85K-a_%E2%80%9CSpatha%E2%80%9D',
        'keywords': 'tankcolonialspata85kaassaultspathaspahtaspatah',
    },
    {
        'name': '85V-g “Talos”',
        'url': 'https://foxhole.wiki.gg/wiki/85V-g_%E2%80%9CTalos%E2%80%9D',
        'keywords': 'tankcolonial85vgassault75mmtalos',
    },
    {
        'name': '90T-v “Nemesis”',
        'url': 'https://foxhole.wiki.gg/wiki/90T-v_%E2%80%9CNemesis%E2%80%9D',
        'keywords': 'tankcolonialassault68mm90tvnemesis',
    },
    {
        'name': '86K-a “Bardiche”',
        'url': 'https://foxhole.wiki.gg/wiki/86K-a_%E2%80%9CBardiche%E2%80%9D',
        'keywords': 'tankcolonialassaultbardiche86ka',
    },
    {
        'name': '86K-c “Ranseur”',
        'url': 'https://foxhole.wiki.gg/wiki/86K-c_%E2%80%9CRanseur%E2%80%9D',
        'keywords': 'tankcolonialrpgassaultranseurquadiche86kc',
    },
    {
        'name': 'Silverhand - Mk. IV',
        'url': 'https://foxhole.wiki.gg/wiki/Silverhand_-_Mk._IV',
        'keywords': 'tankassaultwardensilverhandsvh',
    },
    {
        'name': 'Silverhand Chieftain - Mk. VI',
        'url': 'https://foxhole.wiki.gg/wiki/Silverhand_Chieftain_-_Mk._VI',
        'keywords': 'tankassaultwardenchieftainsilverhand',
    },
    {
        'name': 'Silverhand Lordscar - Mk. X',
        'url': 'https://foxhole.wiki.gg/wiki/Silverhand_Lordscar_-_Mk._X',
        'keywords': 'tankassaultwardendestroyerlordscarsilverhandstd',
    },
    {
        'name': 'Gallagher Brigand Mk. I',
        'url': 'https://foxhole.wiki.gg/wiki/Gallagher_Brigand_Mk._I',
        'keywords': 'tankwardencruiserbrigandgallagher',
    },
    {
        'name': 'Gallagher Outlaw Mk. II',
        'url': 'https://foxhole.wiki.gg/wiki/Gallagher_Outlaw_Mk._II',
        'keywords': 'tankwardenoutlawcruisergallagher',
    },
    {
        'name': 'Gallagher Highwayman Mk. III',
        'url': 'https://foxhole.wiki.gg/wiki/Gallagher_Highwayman_Mk._III',
        'keywords': 'tankwardenhwmcruiserhighwaymangallagher',
    },
    {
        'name': 'Gallagher Thornfall Mk. VI',
        'url': 'https://foxhole.wiki.gg/wiki/Gallagher_Thornfall_Mk._VI',
        'keywords': 'tankwardenbonelawcruiserthornfallgallagher',
    },
    {
        'name': 'HC-2 “Scorpion”',
        'url': 'https://foxhole.wiki.gg/wiki/Light_Infantry_Tank',
        'keywords': 'tankcolonialistsupporthc2scorpioninfantrylight',
    },
    {
        'name': 'HC-7 “Ballista”',
        'url': 'https://foxhole.wiki.gg/wiki/Siege_Tank',
        'keywords': 'tankcolonialsiegeballista',
    },
    {
        'name': 'Noble Widow MK. XIV',
        'url': 'https://foxhole.wiki.gg/wiki/Noble_Widow_MK._XIV',
        'keywords': 'widowtankhtdheavywardendestroyernoble',
    },
    {
        'name': 'Noble Firebrand Mk. XVII',
        'url': 'https://foxhole.wiki.gg/wiki/Noble_Firebrand_Mk._XVII',
        'keywords': 'firebrandtankheavywardendestroyernoblleflame',
    },
    {
        'name': 'Flood Juggernaut Mk. VII',
        'url': 'https://foxhole.wiki.gg/wiki/Flood_Juggernaut_Mk._VII',
        'keywords': 'tankwardenflamebattlejuggernautbtflood',
    },
    {
        'name': 'Flood Mk. I',
        'url': 'https://foxhole.wiki.gg/wiki/Flood_Mk._I',
        'keywords': 'tankwardenbattlebtflood',
    },
    {
        'name': 'Flood Mk. IX Stain',
        'url': 'https://foxhole.wiki.gg/wiki/Flood_Mk._IX_Stain',
        'keywords': 'tankwardenbattlestainspgbtflood',
    },
    {
        'name': 'Lance-25 “Hasta”',
        'url': 'https://foxhole.wiki.gg/wiki/Lance-25_%E2%80%9CHasta%E2%80%9D',
        'keywords': 'tankcolonialdestroyerlance25battlebtdhasta',
    },
    {
        'name': 'Lance-36',
        'url': 'https://foxhole.wiki.gg/wiki/Lance-36',
        'keywords': 'tankcoloniallance36battlebt',
    },
    {
        'name': 'Lance-46 “Sarissa”',
        'url': 'https://foxhole.wiki.gg/wiki/Lance-46_%E2%80%9CSarissa%E2%80%9D',
        'keywords': 'tankcoloniallance46battlesarissaspg',
    },
    {
        'name': 'Cullen Predator Mk. III',
        'url': 'https://foxhole.wiki.gg/wiki/Cullen_Predator_Mk._III',
        'keywords': 'tanksuperwardenshtcullenpredator',
    },
    {
        'name': 'O-75b “Ares”',
        'url': 'https://foxhole.wiki.gg/wiki/O-75b_%E2%80%9CAres%E2%80%9D',
        'keywords': 'tankcolonialsupershtares',
    },
    {
        'name': 'Dunne Fuelrunner 2d',
        'url': 'https://foxhole.wiki.gg/wiki/Dunne_Fuelrunner_2d',
        'keywords': 'wardentankerdunnelfuelfuelrunner',
    },
    {
        'name': 'RR-3 “Stolon” Tanker',
        'url': 'https://foxhole.wiki.gg/wiki/RR-3_%E2%80%9CStolon%E2%80%9D_Tanker',
        'keywords': 'fuelcolonialstolontanker',
    },
    {
        'name': 'R-1 Hauler',
        'url': 'https://foxhole.wiki.gg/wiki/R-1_Hauler',
        'keywords': 'colonialtruckr1hauler',
    },
    {
        'name': 'R-17 “Retiarius” Skirmisher',
        'url': 'https://foxhole.wiki.gg/wiki/R-17_%E2%80%9CRetiarius%E2%80%9D_Skirmisher',
        'keywords': 'colonialskirmisherretiariusr17katyushatruck',
    },
    {
        'name': 'R-5b “Sisyphus” Hauler',
        'url': 'https://foxhole.wiki.gg/wiki/R-5b_%E2%80%9CSisyphus%E2%80%9D_Hauler',
        'keywords': 'colonialr5btrucksisyphushauler',
    },
    {
        'name': 'R-9 “Speartip” Escort',
        'url': 'https://foxhole.wiki.gg/wiki/R-9_%E2%80%9CSpeartip%E2%80%9D_Escort',
        'keywords': 'colonialescortspeartiptruckr9',
    },
    {
        'name': 'R-5 “Atlas” Hauler',
        'url': 'https://foxhole.wiki.gg/wiki/R-5_%E2%80%9CAtlas%E2%80%9D_Hauler',
        'keywords': 'colonialr5truckatlashauler',
    },
    {
        'name': 'Dunne Loadlugger 3c',
        'url': 'https://foxhole.wiki.gg/wiki/Dunne_Loadlugger_3c',
        'keywords': 'loadluggerwardendunne3ctruck',
    },
    {
        'name': 'Dunne Transport',
        'url': 'https://foxhole.wiki.gg/wiki/Dunne_Transport',
        'keywords': 'transportwardentruckdunne',
    },
    {
        'name': 'Dunne Landrunner 12c',
        'url': 'https://foxhole.wiki.gg/wiki/Dunne_Landrunner_12c',
        'keywords': 'dunnewardenlandrunnertruck12c',
    },
    {
        'name': 'Dunne Leatherback 2a',
        'url': 'https://foxhole.wiki.gg/wiki/Dunne_Leatherback_2a',
        'keywords': '2adunnerleatherbackwardentruck',
    },
    {
        'name': 'BMS - Class 2 Mobile Auto-Crane',
        'url': 'https://foxhole.wiki.gg/wiki/Crane',
        'keywords': 'bmscraneclassmobile',
    },
    {
        'name': 'BMS - Overseer Sky-Hauler',
        'url': 'https://foxhole.wiki.gg/wiki/Large_Crane',
        'keywords': 'overseercranelargebmsskyhauler',
    },
    {
        'name': 'BMS - Universal Assembly Rig',
        'url': 'https://foxhole.wiki.gg/wiki/Construction_Vehicle',
        'keywords': 'rigassemblyvehicleuniversalcvconstructionbms',
    },
    {
        'name': 'BMS - Fabricator',
        'url': 'https://foxhole.wiki.gg/wiki/Advanced_Construction_Vehicle',
        'keywords': 'fabricatorvehicleadvancedbmsconstructionacv',
    },
    {
        'name': 'BMS - Packmule Flatbed',
        'url': 'https://foxhole.wiki.gg/wiki/Flatbed_Truck',
        'keywords': 'bmstruckflatbedpackmule',
    },
    {
        'name': 'BMS - Scrap Hauler',
        'url': 'https://foxhole.wiki.gg/wiki/Harvester',
        'keywords': 'bmsscrapharvesterhauler',
    },
    {
        'name': 'Rooster - Junkwagon',
        'url': 'https://foxhole.wiki.gg/wiki/Rooster_-_Junkwagon',
        'keywords': 'junkwagonroostertrailer',
    },
    {
        'name': 'Rooster - Lamploader',
        'url': 'https://foxhole.wiki.gg/wiki/Rooster_-_Lamploader',
        'keywords': 'lamploaderroostertrailer',
    },
    {
        'name': 'Rooster - Tumblebox',
        'url': 'https://foxhole.wiki.gg/wiki/Rooster_-_Tumblebox',
        'keywords': 'tumbleboxroostertrailer',
    },
    {
        'name': 'Dunne Dousing Engine 3r',
        'url': 'https://foxhole.wiki.gg/wiki/Dunne_Dousing_Engine_3r',
        'keywords': 'dousingwardenfiretruckdunne3rengine',
    },
    {
        'name': 'R-12b - “Salva” Flame Truck',
        'url': 'https://foxhole.wiki.gg/wiki/R-12b_-_%E2%80%9CSalva%E2%80%9D_Flame_Truck',
        'keywords': 'colonialtruckfiretruckflamesalvaenginer12b',
    },
    {
        'name': 'Dunne Caravaner 2f',
        'url': 'https://foxhole.wiki.gg/wiki/Dunne_Caravaner_2f',
        'keywords': 'caravanerwardenbus2fdunne',
    },
    {
        'name': 'R-15 - “Chariot”',
        'url': 'https://foxhole.wiki.gg/wiki/R-15_-_%E2%80%9CChariot%E2%80%9D',
        'keywords': 'colonialchariotbusr15',
    },
    {
        'name': 'Dunne Responder 3e',
        'url': 'https://foxhole.wiki.gg/wiki/Dunne_Responder_3e',
        'keywords': '3eresponderdunnerwardenambulance',
    },
    {
        'name': 'R-12 - “Salus” Ambulance',
        'url': 'https://foxhole.wiki.gg/wiki/R-12_-_%E2%80%9CSalus%E2%80%9D_Ambulance',
        'keywords': 'ambulancecolonialsalusr12',
    },
    {
        'name': 'Cnute Cliffwrest',
        'url': 'https://foxhole.wiki.gg/wiki/Cnute_Cliffwrest',
        'keywords': 'cnutecliffwrestheavywardendutytruck',
    },
    {
        'name': 'AU-A150 Taurine Rigger',
        'url': 'https://foxhole.wiki.gg/wiki/AU-A150_Taurine_Rigger',
        'keywords': 'colonialtaurineheavydutytruckrigger',
    },
    {
        'name': '03MM “Caster”',
        'url': 'https://foxhole.wiki.gg/wiki/03MM_%E2%80%9CCaster%E2%80%9D',
        'keywords': 'motorcyclebikecolonialcaster',
    },
    {
        'name': '00MS “Stinger”',
        'url': 'https://foxhole.wiki.gg/wiki/00MS_%E2%80%9CStinger%E2%80%9D',
        'keywords': 'motorcyclecolonialbikemgstinger',
    },
    {
        'name': 'Kivela Power Wheel 80-1',
        'url': 'https://foxhole.wiki.gg/wiki/Kivela_Power_Wheel_80-1',
        'keywords': 'motorcyclebikewheelwardenpowerkivela',
    },
    {
        'name': 'UV-05a “Argonaut”',
        'url': 'https://foxhole.wiki.gg/wiki/UV-05a_%E2%80%9CArgonaut%E2%80%9D',
        'keywords': 'colonialargonautlightvehicleluvuv05autility',
    },
    {
        'name': 'UV-24 “Icarus”',
        'url': 'https://foxhole.wiki.gg/wiki/UV-24_%E2%80%9CIcarus%E2%80%9D',
        'keywords': 'colonialrpguv24vehiclejeepicarusluvlightutility',
    },
    {
        'name': 'UV-5c “Odyssey”',
        'url': 'https://foxhole.wiki.gg/wiki/UV-5c_%E2%80%9COdyssey%E2%80%9D',
        'keywords': 'coloniallightvehicleluvodysseyuv5cutility',
    },
    {
        'name': 'Drummond 100a',
        'url': 'https://foxhole.wiki.gg/wiki/Drummond_100a',
        'keywords': 'wardenlightvehicledrummondluv100autility',
    },
    {
        'name': 'Drummond Loscann 55c',
        'url': 'https://foxhole.wiki.gg/wiki/Drummond_Loscann_55c',
        'keywords': 'aluvdrummondvehiclecar55camphibiouswardenloscannlightutility',
    },
    {
        'name': 'Drummond Spitfire 100d',
        'url': 'https://foxhole.wiki.gg/wiki/Drummond_Spitfire_100d',
        'keywords': '100ddrummondvehiclespitfirewardenluvlightutility',
    },
    {
        'name': 'MacConmara Shorerunner',
        'url': 'https://foxhole.wiki.gg/wiki/MacConmara_Shorerunner',
        'keywords': 'wardenshiplandingshorerunnermacconmara',
    },
    {
        'name': 'Interceptor PA-12',
        'url': 'https://foxhole.wiki.gg/wiki/Interceptor_PA-12',
        'keywords': 'colonialinterceptorshippa12landing',
    },
    {
        'name': 'BMS - Aquatipper',
        'url': 'https://foxhole.wiki.gg/wiki/Barge',
        'keywords': 'bmsbargeaquatipper',
    },
    {
        'name': 'BMS - Ironship',
        'url': 'https://foxhole.wiki.gg/wiki/Freighter',
        'keywords': 'mbsironshipfreighter',
    },
    {
        'name': 'BMS - Grouper',
        'url': 'https://foxhole.wiki.gg/wiki/Motorboat',
        'keywords': 'bmsmotorboatgrouper',
    },
    {
        'name': '74b-1 Ronan Gunship',
        'url': 'https://foxhole.wiki.gg/wiki/74b-1_Ronan_Gunship',
        'keywords': 'warden74b1gunboatgunshipronan',
    },
    {
        'name': 'Type C - “Charon”',
        'url': 'https://foxhole.wiki.gg/wiki/Type_C_-_%E2%80%9CCharon%E2%80%9D',
        'keywords': 'colonialcharongunboat',
    },
    {
        'name': 'Nakki',
        'url': 'https://foxhole.wiki.gg/wiki/Nakki',
        'keywords': 'submarinenakkiwarden',
    },
    {
        'name': 'AC-b “Trident”',
        'url': 'https://foxhole.wiki.gg/wiki/AC-b_%E2%80%9CTrident%E2%80%9D',
        'keywords': 'colonialsubmarinetrident',
    },
    {
        'name': 'Blacksteele',
        'url': 'https://foxhole.wiki.gg/wiki/Blacksteele',
        'keywords': 'lightwardenfrigateblacksteele',
    },
    {
        'name': 'Conqueror',
        'url': 'https://foxhole.wiki.gg/wiki/Conqueror',
        'keywords': 'colonialdddestroyerconqueror',
    },
    {
        'name': 'BMS - Longhook',
        'url': 'https://foxhole.wiki.gg/wiki/Base_Ship',
        'keywords': 'shipbmslonghookbaselh',
    },
    {
        'name': 'BMS - Bluefin',
        'url': 'https://foxhole.wiki.gg/wiki/Storage_Ship',
        'keywords': 'bmsstorageshipbluefin',
    },
    {
        'name': 'BMS - Bowhead',
        'url': 'https://foxhole.wiki.gg/wiki/Resource_Ship',
        'keywords': 'resourcebmsbowheadship',
    },
    {
        'name': 'Callahan (Battleship)',
        'url': 'https://foxhole.wiki.gg/wiki/Callahan_(Battleship)',
        'keywords': 'callahanwardenbsbattleship',
    },
    {
        'name': 'Titan',
        'url': 'https://foxhole.wiki.gg/wiki/Titan',
        'keywords': 'colonialtitanbsbattleship',
    },
    {
        'name': 'BMS Railtruck',
        'url': 'https://foxhole.wiki.gg/wiki/Small_Container_Car',
        'keywords': 'railtruckbmscarsmallcontainer',
    },
    {
        'name': 'BMS Linerunner',
        'url': 'https://foxhole.wiki.gg/wiki/Small_Flatbed_Car',
        'keywords': 'linerunnerflatbedbmscarsmall',
    },
    {
        'name': 'BMS Tinderbox',
        'url': 'https://foxhole.wiki.gg/wiki/Small_Liquid_Container_Car',
        'keywords': 'tinderboxbmsliquidcarsmallcontainer',
    },
    {
        'name': 'BMS Stowheel',
        'url': 'https://foxhole.wiki.gg/wiki/Small_Box_Car',
        'keywords': 'boxstowheelbmscarsmallcontainer',
    },
    {
        'name': 'BMS Mineseeker',
        'url': 'https://foxhole.wiki.gg/wiki/Small_Train_Locomotive',
        'keywords': 'mineseekerbmstrainlocomotivesmall',
    },
    {
        'name': 'BMS Rockhold',
        'url': 'https://foxhole.wiki.gg/wiki/Container_Car',
        'keywords': 'bmslargetraincarrockholdcontainer',
    },
    {
        'name': 'BMS Roadhouse',
        'url': 'https://foxhole.wiki.gg/wiki/Caboose',
        'keywords': 'largecaboosetrainbmsroadhouse',
    },
    {
        'name': 'BMS Longrider',
        'url': 'https://foxhole.wiki.gg/wiki/Flatbed_Car',
        'keywords': 'flatbedlongriderlargetraincarbms',
    },
    {
        'name': 'BMS Holdout',
        'url': 'https://foxhole.wiki.gg/wiki/Infantry_Car',
        'keywords': 'infantrylargetraincarbmsholdout',
    },
    {
        'name': 'BMS Black Bolt',
        'url': 'https://foxhole.wiki.gg/wiki/Locomotive',
        'keywords': 'locomotivelargetrainboltbmsblack',
    },
    {
        'name': "O'Brien Warsmith v.215",
        'url': 'https://foxhole.wiki.gg/wiki/O%27Brien_Warsmith_v.215',
        'keywords': 'wardenv215combatcarwarsmithobrien',
    },
    {
        'name': 'Aegis Steelbreaker K5a',
        'url': 'https://foxhole.wiki.gg/wiki/Aegis_Steelbreaker_K5a',
        'keywords': 'aegiscolonialcombatsteelbreakerk5acar',
    },
    {
        'name': 'Tempest Cannon RA-2',
        'url': 'https://foxhole.wiki.gg/wiki/Long-Range_Artillery_Car',
        'keywords': 'rscartillerycannoncarrangetempestlong',
    },
    {
        'name': 'Armoured Fighting Tractor',
        'url': 'https://foxhole.wiki.gg/wiki/Armoured_Fighting_Tractor',
        'keywords': 'relicarmouredfightingvehicletractoramored',
    },
    {
        'name': 'PL-1 “Phalanx”',
        'url': 'https://foxhole.wiki.gg/wiki/Relic_Assault_Tank',
        'keywords': 'tankassaultrelicvehiclephalanxpl1',
    },
    {
        'name': 'Storm Tank',
        'url': 'https://foxhole.wiki.gg/wiki/Storm_Tank',
        'keywords': 'tankstormrelicvehicle',
    },
    {
        'name': 'Staff Car',
        'url': 'https://foxhole.wiki.gg/wiki/Staff_Car',
        'keywords': 'carvehiclerelicstaff',
    },
    {
        'name': 'Repurposed Truck',
        'url': 'https://foxhole.wiki.gg/wiki/Repurposed_Truck',
        'keywords': 'repurposedtruckrelicvehicle',
    },
]


STRUCTURES_WIKI_ENTRIES = [
    {
        'name': 'Border Base',
        'url': 'https://foxhole.wiki.gg/wiki/Border_Base',
        'keywords': 'borderbobbbbase',
    },
    {
        'name': 'Relic Base',
        'url': 'https://foxhole.wiki.gg/wiki/Relic_Base',
        'keywords': 'relicbase',
    },
    {
        'name': 'Town Base (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Town_Base#Tier_1-0',
        'keywords': 't1townbase',
    },
    {
        'name': 'Town Base (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Town_Base#Tier_2-0',
        'keywords': 't2townbase',
    },
    {
        'name': 'Town Base (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Town_Base#Tier_3-0',
        'keywords': 't3townbase',
    },
    {
        'name': 'Bunker Base (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Bunker_Base#Tier_1-0',
        'keywords': 'bunkert1basebbbob',
    },
    {
        'name': 'Bunker Base (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Bunker_Base#Tier_2-0',
        'keywords': 'bunkerbasebbcoret2bob',
    },
    {
        'name': 'Bunker Base (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Bunker_Base#Tier_3-0',
        'keywords': 'bunkerbasebbconcretecoret3bob',
    },
    {
        'name': 'Encampment',
        'url': 'https://foxhole.wiki.gg/wiki/Encampment',
        'keywords': 'encampment',
    },
    {
        'name': 'Keep',
        'url': 'https://foxhole.wiki.gg/wiki/Keep',
        'keywords': 'keep',
    },
    {
        'name': 'Safe House (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Safe_House#Tier_1-0',
        'keywords': 'safet1house',
    },
    {
        'name': 'Safe House (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Safe_House#Tier_2-0',
        'keywords': 'safet2house',
    },
    {
        'name': 'Safe House (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Safe_House#Tier_3-0',
        'keywords': 'safet3house',
    },
    {
        'name': 'Seaport',
        'url': 'https://foxhole.wiki.gg/wiki/Seaport',
        'keywords': 'seaport',
    },
    {
        'name': 'Storage Depot',
        'url': 'https://foxhole.wiki.gg/wiki/Storage_Depot',
        'keywords': 'depotstorage',
    },
    {
        'name': 'Liquid Container',
        'url': 'https://foxhole.wiki.gg/wiki/Liquid_Container',
        'keywords': 'containerliquid',
    },
    {
        'name': 'Liquid Transfer Station',
        'url': 'https://foxhole.wiki.gg/wiki/Liquid_Transfer_Station',
        'keywords': 'stationtransferliquidlts',
    },
    {
        'name': 'Material Pallet',
        'url': 'https://foxhole.wiki.gg/wiki/Material_Pallet',
        'keywords': 'palletmaterial',
    },
    {
        'name': 'Material Transfer Station',
        'url': 'https://foxhole.wiki.gg/wiki/Material_Transfer_Station',
        'keywords': 'mtstransfermaterialstation',
    },
    {
        'name': 'Resource Container',
        'url': 'https://foxhole.wiki.gg/wiki/Resource_Container',
        'keywords': 'containerresource',
    },
    {
        'name': 'Resource Transfer Station',
        'url': 'https://foxhole.wiki.gg/wiki/Resource_Transfer_Station',
        'keywords': 'transferresourcertsstation',
    },
    {
        'name': 'Infantry Arms Factory',
        'url': 'https://foxhole.wiki.gg/wiki/Infantry_Arms_Factory',
        'keywords': 'infantryarmsfactory',
    },
    {
        'name': 'Crate Transfer Station',
        'url': 'https://foxhole.wiki.gg/wiki/Crate_Transfer_Station',
        'keywords': 'transfercratestation',
    },
    {
        'name': 'Shippable Crate',
        'url': 'https://foxhole.wiki.gg/wiki/Shippable_Crate',
        'keywords': 'crateshippable',
    },
    {
        'name': 'Shipping Container',
        'url': 'https://foxhole.wiki.gg/wiki/Shipping_Container',
        'keywords': 'containershipping',
    },
    {
        'name': 'Storage Box',
        'url': 'https://foxhole.wiki.gg/wiki/Storage_Box',
        'keywords': 'boxstorage',
    },
    {
        'name': 'Medical Room (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Medical_Room',
        'keywords': 'bunkert1medicalroom',
    },
    {
        'name': 'Medical Room (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Medical_Room#Tier_2-0',
        'keywords': 'bunkert2medicalroom',
    },
    {
        'name': 'Medical Room (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Medical_Room#Tier_3-0',
        'keywords': 'bunkert3medicalroom',
    },
    {
        'name': 'Storage Room (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Storage_Room#Tier_2-0',
        'keywords': 'bunkert2roomstorage',
    },
    {
        'name': 'Storage Room (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Storage_Room#Tier_3-0',
        'keywords': 'bunkert3roomstorage',
    },
    {
        'name': 'Coastal Gun',
        'url': 'https://foxhole.wiki.gg/wiki/Coastal_Gun',
        'keywords': 'coastalgun',
    },
    {
        'name': 'Garrisoned House (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Garrisoned_House#Tier_1-0',
        'keywords': 'ghousegarrisonedhousetier1',
    },
    {
        'name': 'Garrisoned House (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Garrisoned_House#Tier_2-0',
        'keywords': 'ghousegarrisonedhousetier2',
    },
    {
        'name': 'Garrisoned House (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Garrisoned_House#Tier_3-0',
        'keywords': 'ghousegarrisonedhousetier3',
    },
    {
        'name': 'Observation Tower',
        'url': 'https://foxhole.wiki.gg/wiki/Observation_Tower',
        'keywords': 'towerobsobservation',
    },
    {
        'name': 'Anti-Tank Pillbox',
        'url': 'https://foxhole.wiki.gg/wiki/Anti-Tank_Pillbox',
        'keywords': 'attankantipillbox',
    },
    {
        'name': 'AT Gun Garrison (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/AT_Gun_Garrison#Tier_2-0',
        'keywords': 'bunkeratatggunt2garrison',
    },
    {
        'name': 'AT Gun Garrison (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/AT_Gun_Garrison#Tier_3-0',
        'keywords': 'bunkeratatggunconcretet3garrison',
    },
    {
        'name': 'Howitzer Garrison',
        'url': 'https://foxhole.wiki.gg/wiki/Howitzer_Garrison',
        'keywords': 'bunkerhowieshowitzerconcretegarrison',
    },
    {
        'name': 'Machine Gun Garrison (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Machine_Gun_Garrison#Tier_1-0',
        'keywords': 'bunkert1mgmgggunmachinegarrison',
    },
    {
        'name': 'Machine Gun Garrison (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Machine_Gun_Garrison#Tier_2-0',
        'keywords': 'bunkermgmgggunmachinet2garrison',
    },
    {
        'name': 'Machine Gun Garrison (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Machine_Gun_Garrison#Tier_3-0',
        'keywords': 'bunkermgconcretemgggunmachinet3garrison',
    },
    {
        'name': 'Machine Gun Pillbox',
        'url': 'https://foxhole.wiki.gg/wiki/Machine_Gun_Pillbox',
        'keywords': 'mgpillboxmachinegun',
    },
    {
        'name': 'Observation Bunker (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Observation_Bunker#Tier_2-0',
        'keywords': 'bunkert2obsobservation',
    },
    {
        'name': 'Observation Bunker (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Observation_Bunker#Tier_3-0',
        'keywords': 'bunkerobsconcretet3observation',
    },
    {
        'name': 'Rifle Garrison (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Rifle_Garrison#Tier_1-0',
        'keywords': 'bunkert1riflerggarrison',
    },
    {
        'name': 'Rifle Garrison (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Rifle_Garrison#Tier_2-0',
        'keywords': 'bunkerriflergt2garrison',
    },
    {
        'name': 'Rifle Garrison (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Rifle_Garrison#Tier_3-0',
        'keywords': 'bunkerriflergconcretet3garrison',
    },
    {
        'name': 'Rifle Pillbox',
        'url': 'https://foxhole.wiki.gg/wiki/Rifle_Pillbox',
        'keywords': 'riflepillbox',
    },
    {
        'name': 'Watch Tower',
        'url': 'https://foxhole.wiki.gg/wiki/Watch_Tower',
        'keywords': 'wtwatchtower',
    },
    {
        'name': 'Emplacement House',
        'url': 'https://foxhole.wiki.gg/wiki/Emplacement_House',
        'keywords': 'emplacementmhousemortar',
    },
    {
        'name': '50-500 “Thunderbolt” Cannon',
        'url': 'https://foxhole.wiki.gg/wiki/50-500_%E2%80%9CThunderbolt%E2%80%9D_Cannon',
        'keywords': 'cannonthunderboltartilleryarty150mmcolonial',
    },
    {
        'name': 'DAE 1b-2 “Serra”',
        'url': 'https://foxhole.wiki.gg/wiki/DAE_1b-2_%E2%80%9CSerra%E2%80%9D',
        'keywords': 'gunemplacedmachinecolonialserraemg',
    },
    {
        'name': 'DAE 1o-3 “Polybolos”',
        'url': 'https://foxhole.wiki.gg/wiki/DAE_1o-3_%E2%80%9CPolybolos%E2%80%9D',
        'keywords': 'atpolybolosemplacedgunbeatcolonial',
    },
    {
        'name': 'DAE 2a-1 “Ruptura”',
        'url': 'https://foxhole.wiki.gg/wiki/DAE_2a-1_%E2%80%9CRuptura%E2%80%9D',
        'keywords': 'colonialruptura',
    },
    {
        'name': "DAE 3b-2 “Hades' Net”",
        'url': 'https://foxhole.wiki.gg/wiki/DAE_3b-2_%E2%80%9CHades%27_Net%E2%80%9D',
        'keywords': 'artilleryemplacednethadescolonialrocket',
    },
    {
        'name': 'Huber Exalt 150mm',
        'url': 'https://foxhole.wiki.gg/wiki/Huber_Exalt_150mm',
        'keywords': 'wardenexaltartilleryarty150mmhubert',
    },
    {
        'name': 'Huber Lariat 120mm',
        'url': 'https://foxhole.wiki.gg/wiki/Light_Artillery',
        'keywords': 'wardenartillerylariatartyhuber',
    },
    {
        'name': 'Huber Starbreaker 94.5mm',
        'url': 'https://foxhole.wiki.gg/wiki/Huber_Starbreaker_94.5mm',
        'keywords': '945mmwardenhuberstarbreaker',
    },
    {
        'name': 'Intelligence Center',
        'url': 'https://foxhole.wiki.gg/wiki/Intelligence_Center',
        'keywords': 'centerintelligenceic',
    },
    {
        'name': 'Leary Shellbore 68mm',
        'url': 'https://foxhole.wiki.gg/wiki/Leary_Shellbore_68mm',
        'keywords': '68mmatwardenshellboreemplacedeatlearygun',
    },
    {
        'name': 'Leary Snare Trap 127',
        'url': 'https://foxhole.wiki.gg/wiki/Leary_Snare_Trap_127',
        'keywords': 'snarewarden127emplacedlearyguntrapmachineemg',
    },
    {
        'name': 'Storm Cannon',
        'url': 'https://foxhole.wiki.gg/wiki/Storm_Cannon',
        'keywords': 'cannonscstorm',
    },
    {
        'name': 'Barbed Wire',
        'url': 'https://foxhole.wiki.gg/wiki/Barbed_Wire_(Structure)',
        'keywords': 'barbedwire',
    },
    {
        'name': 'Barbed Wire Fence',
        'url': 'https://foxhole.wiki.gg/wiki/Barbed_Wire_Fence',
        'keywords': 'barbedfencewire',
    },
    {
        'name': 'Prepared Minefield',
        'url': 'https://foxhole.wiki.gg/wiki/Prepared_Minefield',
        'keywords': 'minefieldprepared',
    },
    {
        'name': "Crow's Foot Minefield",
        'url': 'https://foxhole.wiki.gg/wiki/Crow%27s_Foot_Minefield',
        'keywords': 'infantrycrowsfootantiminefieldpersonal',
    },
    {
        'name': 'Abisme AT-99 Minefield',
        'url': 'https://foxhole.wiki.gg/wiki/Abisme_AT-99_Minefield',
        'keywords': 'atabismetankantiminefield',
    },
    {
        'name': 'Bunker (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Bunker#Tier_1-0',
        'keywords': 'bunkert1',
    },
    {
        'name': 'Bunker (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Bunker#Tier_2-0',
        'keywords': 'bunkert2',
    },
    {
        'name': 'Bunker (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Bunker#Tier_3-0',
        'keywords': 'bunkert3',
    },
    {
        'name': 'Bunker Corner (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Bunker_Corner#Tier_1-0',
        'keywords': 'bunkert1corner',
    },
    {
        'name': 'Bunker Corner (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Bunker_Corner#Tier_2-0',
        'keywords': 'bunkert2corner',
    },
    {
        'name': 'Bunker Corner (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Bunker_Corner#Tier_3-0',
        'keywords': 'bunkert3corner',
    },
    {
        'name': 'Bunker Ramp (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Bunker_Ramp#Tier_1-0',
        'keywords': 'bunkert1ramp',
    },
    {
        'name': 'Bunker Ramp (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Bunker_Ramp#Tier_2-0',
        'keywords': 'bunkert2ramp',
    },
    {
        'name': 'Bunker Ramp (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Bunker_Ramp#Tier_3-0',
        'keywords': 'bunkert3ramp',
    },
    {
        'name': "Dragon's Teeth",
        'url': 'https://foxhole.wiki.gg/wiki/Dragon%27s_Teeth',
        'keywords': 'dragonteeth',
    },
    {
        'name': 'Foxhole',
        'url': 'https://foxhole.wiki.gg/wiki/Foxhole_(Structure)',
        'keywords': 'foxholedug',
    },
    {
        'name': 'Gate (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Gate#Tier_1-0',
        'keywords': 'gatet1',
    },
    {
        'name': 'Gate (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Gate#Tier_2-0',
        'keywords': 'gatet2',
    },
    {
        'name': 'Gate (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Gate#Tier_3-0',
        'keywords': 'gatet3concrete',
    },
    {
        'name': 'Sandbag Cover',
        'url': 'https://foxhole.wiki.gg/wiki/Sandbag_Cover#Sandbag_Cover_(Tier_1)-0',
        'keywords': 'sandbagscover',
    },
    {
        'name': 'Sandbag Wall',
        'url': 'https://foxhole.wiki.gg/wiki/Sandbag_Cover#Sandbag_Wall_(Tier_2)-0',
        'keywords': 'sandbagswall',
    },
    {
        'name': 'Tank Trap',
        'url': 'https://foxhole.wiki.gg/wiki/Tank_Trap',
        'keywords': 'tanktrap',
    },
    {
        'name': 'Trench (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Trench#Tier_1-0',
        'keywords': 't1trench',
    },
    {
        'name': 'Trench (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Trench#Tier_2-0',
        'keywords': 'trencht2',
    },
    {
        'name': 'Trench (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Trench#Tier_3-0',
        'keywords': 'trencht3',
    },
    {
        'name': 'Trench Connector (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Trench_Connector#Tier_1-0',
        'keywords': 't1trenchconnector',
    },
    {
        'name': 'Trench Connector (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Trench_Connector#Tier_2-0',
        'keywords': 'trencht2connector',
    },
    {
        'name': 'Trench Connector (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Trench_Connector#Tier_3-0',
        'keywords': 'concretetrencht3connector',
    },
    {
        'name': 'Trench Emplacement (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Trench_Emplacement#Tier_1-0',
        'keywords': 'emplacementt1trenchpit',
    },
    {
        'name': 'Trench Emplacement (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Trench_Emplacement#Tier_2-0',
        'keywords': 'emplacementpittrencht2',
    },
    {
        'name': 'Trench Emplacement (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Trench_Emplacement#Tier_3-0',
        'keywords': 'concreteemplacementpittrencht3',
    },
    {
        'name': 'Wall (Tier 1)',
        'url': 'https://foxhole.wiki.gg/wiki/Wall#Tier_1-0',
        'keywords': 't1wall',
    },
    {
        'name': 'Wall (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Wall#Tier_2-0',
        'keywords': 't2wall',
    },
    {
        'name': 'Wall (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Wall#Tier_3-0',
        'keywords': 'concretet3wall',
    },
    {
        'name': 'Construction Yard',
        'url': 'https://foxhole.wiki.gg/wiki/Construction_Yard',
        'keywords': 'yardconstruction',
    },
    {
        'name': 'Engineering Center',
        'url': 'https://foxhole.wiki.gg/wiki/Engineering_Center',
        'keywords': 'centertechengineering',
    },
    {
        'name': 'Factory',
        'url': 'https://foxhole.wiki.gg/wiki/Factory',
        'keywords': 'factory',
    },
    {
        'name': 'Garage',
        'url': 'https://foxhole.wiki.gg/wiki/Garage',
        'keywords': 'garage',
    },
    {
        'name': 'Hospital',
        'url': 'https://foxhole.wiki.gg/wiki/Hospital',
        'keywords': 'hospital',
    },
    {
        'name': 'Mass Production Factory',
        'url': 'https://foxhole.wiki.gg/wiki/Mass_Production_Factory',
        'keywords': 'productionfactorympfmass',
    },
    {
        'name': 'Refinery',
        'url': 'https://foxhole.wiki.gg/wiki/Refinery',
        'keywords': 'rafrefinery',
    },
    {
        'name': 'Shipyard',
        'url': 'https://foxhole.wiki.gg/wiki/Shipyard',
        'keywords': 'shipyard',
    },
    {
        'name': 'Ammunition Factory',
        'url': 'https://foxhole.wiki.gg/wiki/Ammunition_Factory',
        'keywords': 'factoryammoammunition',
    },
    {
        'name': 'Coal Refinery',
        'url': 'https://foxhole.wiki.gg/wiki/Coal_Refinery',
        'keywords': 'coalrefinery',
    },
    {
        'name': 'Concrete Mixer',
        'url': 'https://foxhole.wiki.gg/wiki/Concrete_Mixer',
        'keywords': 'concretemixer',
    },
    {
        'name': 'Dry Dock',
        'url': 'https://foxhole.wiki.gg/wiki/Dry_Dock',
        'keywords': 'drydock',
    },
    {
        'name': 'Field Hospital',
        'url': 'https://foxhole.wiki.gg/wiki/Field_Hospital',
        'keywords': 'hospitalfield',
    },
    {
        'name': 'Field Modification Center',
        'url': 'https://foxhole.wiki.gg/wiki/Field_Modification_Center',
        'keywords': 'centermodificationfield',
    },
    {
        'name': 'Large Assembly Station',
        'url': 'https://foxhole.wiki.gg/wiki/Large_Assembly_Station',
        'keywords': 'stationassemblyupgradepadlarge',
    },
    {
        'name': 'Materials Factory',
        'url': 'https://foxhole.wiki.gg/wiki/Materials_Factory',
        'keywords': 'factorymaterials',
    },
    {
        'name': 'Metalworks Factory',
        'url': 'https://foxhole.wiki.gg/wiki/Metalworks_Factory',
        'keywords': 'factorymetalworks',
    },
    {
        'name': 'Oil Refinery',
        'url': 'https://foxhole.wiki.gg/wiki/Oil_Refinery',
        'keywords': 'oilrefinery',
    },
    {
        'name': 'Small Assembly Station',
        'url': 'https://foxhole.wiki.gg/wiki/Small_Assembly_Station',
        'keywords': 'assemblysmallupgradepadstation',
    },
    {
        'name': 'Salvage Mine',
        'url': 'https://foxhole.wiki.gg/wiki/Salvage_Mine',
        'keywords': 'scrapsalvagemine',
    },
    {
        'name': 'Sulfur Mine',
        'url': 'https://foxhole.wiki.gg/wiki/Sulfur_Mine',
        'keywords': 'sulfurmine',
    },
    {
        'name': 'Component Mine',
        'url': 'https://foxhole.wiki.gg/wiki/Component_Mine',
        'keywords': 'componentmine',
    },
    {
        'name': 'Offshore Platform',
        'url': 'https://foxhole.wiki.gg/wiki/Offshore_Platform',
        'keywords': 'offshoreplatform',
    },
    {
        'name': 'Oil Well',
        'url': 'https://foxhole.wiki.gg/wiki/Oil_Well',
        'keywords': 'oilwell',
    },
    {
        'name': 'Stationary Harvester (Coal)',
        'url': 'https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Coal)',
        'keywords': 'coalharvesterstationary',
    },
    {
        'name': 'Stationary Harvester (Components)',
        'url': 'https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Components)',
        'keywords': 'harvesterstationarycomponents',
    },
    {
        'name': 'Stationary Harvester (Salvage)',
        'url': 'https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Salvage)',
        'keywords': 'harvesterstationarysalvage',
    },
    {
        'name': 'Stationary Harvester (Sulfur)',
        'url': 'https://foxhole.wiki.gg/wiki/Stationary_Harvester_(Sulfur)',
        'keywords': 'sulfurharvesterstationary',
    },
    {
        'name': 'Water Pump',
        'url': 'https://foxhole.wiki.gg/wiki/Water_Pump',
        'keywords': 'pumpwater',
    },
    {
        'name': 'Stone Bridge',
        'url': 'https://foxhole.wiki.gg/wiki/Stone_Bridge',
        'keywords': 'stonebridge',
    },
    {
        'name': 'Two Tier Bridge',
        'url': 'https://foxhole.wiki.gg/wiki/Two_Tier_Bridge',
        'keywords': 'twobridgetier',
    },
    {
        'name': 'Double Bridge',
        'url': 'https://foxhole.wiki.gg/wiki/Double_Bridge',
        'keywords': 'bridgedouble',
    },
    {
        'name': 'Long Bridge',
        'url': 'https://foxhole.wiki.gg/wiki/Long_Bridge',
        'keywords': 'longbridge',
    },
    {
        'name': 'Train Bridge',
        'url': 'https://foxhole.wiki.gg/wiki/Train_Bridge',
        'keywords': 'trainbridge',
    },
    {
        'name': 'Field Bridge',
        'url': 'https://foxhole.wiki.gg/wiki/Field_Bridge',
        'keywords': 'fieldbridge',
    },
    {
        'name': 'Dock',
        'url': 'https://foxhole.wiki.gg/wiki/Dock',
        'keywords': 'docksdock',
    },
    {
        'name': 'Stationary Crane',
        'url': 'https://foxhole.wiki.gg/wiki/Stationary_Crane',
        'keywords': 'stationarycrane',
    },
    {
        'name': 'A0E-9 Rocket',
        'url': 'https://foxhole.wiki.gg/wiki/A0E-9_Rocket',
        'keywords': 'nukerocket',
    },
    {
        'name': 'BMS Foreman Stacker',
        'url': 'https://foxhole.wiki.gg/wiki/Facility_Crane',
        'keywords': 'bmsstackercraneforemanfacility',
    },
    {
        'name': 'Catwalk Bridge',
        'url': 'https://foxhole.wiki.gg/wiki/Catwalk_Bridge',
        'keywords': 'catwalkbridge',
    },
    {
        'name': 'Catwalk Platform',
        'url': 'https://foxhole.wiki.gg/wiki/Catwalk_Platform',
        'keywords': 'catwalkplatform',
    },
    {
        'name': 'Catwalk Stairs',
        'url': 'https://foxhole.wiki.gg/wiki/Catwalk_Stairs',
        'keywords': 'catwalkstairs',
    },
    {
        'name': 'Crane Railway Track',
        'url': 'https://foxhole.wiki.gg/wiki/Crane_Railway_Track',
        'keywords': 'trackrailwaycrane',
    },
    {
        'name': 'Engine Room (Tier 2)',
        'url': 'https://foxhole.wiki.gg/wiki/Engine_Room#Tier_2-0',
        'keywords': 'bunkert2roomengine',
    },
    {
        'name': 'Engine Room (Tier 3)',
        'url': 'https://foxhole.wiki.gg/wiki/Engine_Room#Tier_3-0',
        'keywords': 'bunkerroomengineconcretet3',
    },
    {
        'name': 'Fire Pit',
        'url': 'https://foxhole.wiki.gg/wiki/Fire_Pit',
        'keywords': 'pitfirecampfire',
    },
    {
        'name': 'Foundation (1x1)',
        'url': 'https://foxhole.wiki.gg/wiki/Foundation#1x1-0',
        'keywords': 'foundation',
    },
    {
        'name': 'Concrete Foundation (1x1)',
        'url': 'https://foxhole.wiki.gg/wiki/Foundation#1x1_Concrete-0',
        'keywords': 'foundationconcrete',
    },
    {
        'name': 'Foundation Corner (1x1)',
        'url': 'https://foxhole.wiki.gg/wiki/Foundation#Corner_1x1-0',
        'keywords': 'foundation',
    },
    {
        'name': 'Concrete Foundation Corner (1x1)',
        'url': 'https://foxhole.wiki.gg/wiki/Foundation#Corner_1x1_Concrete-0',
        'keywords': 'foundationconcrete',
    },
    {
        'name': 'Foundation (1x2)',
        'url': 'https://foxhole.wiki.gg/wiki/Foundation#1x2-0',
        'keywords': 'foundation',
    },
    {
        'name': 'Concrete Foundation (1x2)',
        'url': 'https://foxhole.wiki.gg/wiki/Foundation#1x2_Concrete-0',
        'keywords': 'foundationconcrete',
    },
    {
        'name': 'Foundation (2x2)',
        'url': 'https://foxhole.wiki.gg/wiki/Foundation#2x2-0',
        'keywords': 'foundation',
    },
    {
        'name': 'Concrete Foundation (2x2)',
        'url': 'https://foxhole.wiki.gg/wiki/Foundation#2x2_Concrete-0',
        'keywords': 'foundationconcrete',
    },
    {
        'name': 'Fuel Silo',
        'url': 'https://foxhole.wiki.gg/wiki/Fuel_Silo',
        'keywords': 'fuelsilo',
    },
    {
        'name': 'Maintenance Tunnel',
        'url': 'https://foxhole.wiki.gg/wiki/Maintenance_Tunnel',
        'keywords': 'tunnelmaintenance',
    },
    {
        'name': 'Navy Pier',
        'url': 'https://foxhole.wiki.gg/wiki/Navy_Pier',
        'keywords': 'navypier',
    },
    {
        'name': 'Pipeline',
        'url': 'https://foxhole.wiki.gg/wiki/Pipeline',
        'keywords': 'pipeline',
    },
    {
        'name': 'Pipeline (Overhead)',
        'url': 'https://foxhole.wiki.gg/wiki/Pipeline_(Overhead)',
        'keywords': 'overheadpipeline',
    },
    {
        'name': 'Pipeline (Underground)',
        'url': 'https://foxhole.wiki.gg/wiki/Pipeline_(Underground)',
        'keywords': 'pipelineunderground',
    },
    {
        'name': 'Pipeline Valve',
        'url': 'https://foxhole.wiki.gg/wiki/Pipeline_Valve',
        'keywords': 'pipelinevalve',
    },
    {
        'name': 'Power Pole',
        'url': 'https://foxhole.wiki.gg/wiki/Power_Pole',
        'keywords': 'polepower',
    },
    {
        'name': 'Power Switch',
        'url': 'https://foxhole.wiki.gg/wiki/Power_Switch',
        'keywords': 'powerswitch',
    },
    {
        'name': 'Provisional Road',
        'url': 'https://foxhole.wiki.gg/wiki/Provisional_Road',
        'keywords': 'provisionalroad',
    },
    {
        'name': 'Railway Track',
        'url': 'https://foxhole.wiki.gg/wiki/Railway_Track',
        'keywords': 'trackrailwaylarge',
    },
    {
        'name': 'Railway Track (Biarc)',
        'url': 'https://foxhole.wiki.gg/wiki/Railway_Track_(Biarc)',
        'keywords': 'trackrailwaybiarclarge',
    },
    {
        'name': 'Railway Track (Foundation)',
        'url': 'https://foxhole.wiki.gg/wiki/Railway_Track_(Foundation)',
        'keywords': 'foundationtrackrailwaylarge',
    },
    {
        'name': 'Small Gauge Railway Track',
        'url': 'https://foxhole.wiki.gg/wiki/Small_Gauge_Railway_Track',
        'keywords': 'smallrailwaytrackgauge',
    },
    {
        'name': 'Small Gauge Railway Track (Biarc)',
        'url': 'https://foxhole.wiki.gg/wiki/Small_Gauge_Railway_Track_(Biarc)',
        'keywords': 'railwaysmalltrackbiarcgauge',
    },
    {
        'name': 'Small Gauge Railway Track (Foundation)',
        'url': 'https://foxhole.wiki.gg/wiki/Small_Gauge_Railway_Track_(Foundation)',
        'keywords': 'foundationrailwaysmalltrackgauge',
    },
    {
        'name': 'Deployed Tripod',
        'url': 'https://foxhole.wiki.gg/wiki/Deployed_Tripod',
        'keywords': 'deployedtripod',
    },
    {
        'name': 'Field Range',
        'url': 'https://foxhole.wiki.gg/wiki/Field_Range',
        'keywords': 'rangefield',
    },
]


ALL_WIKI_ENTRIES = ITEMS_WIKI_ENTRIES + VEHICLES_WIKI_ENTRIES + STRUCTURES_WIKI_ENTRIES + FACILITY_MATERIAL_ENTRIES + PLACEHOLDER_ENTRIES
PRODUCTION_ENTRIES = ITEMS_WIKI_ENTRIES + FACILITY_MATERIAL_ENTRIES + VEHICLES_WIKI_ENTRIES
