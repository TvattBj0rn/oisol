import sys
sys.path.append('/modules/wiki/scraper/oisol_scraper.py')
from oisol_scraper import oisol_scraper
import unittest


class MyTestCase(unittest.TestCase):
    def test_t13_battery_rocket(self):
        URL = 'https://foxhole.wiki.gg/wiki/T13_%E2%80%9CDeioneus%E2%80%9D_Rocket_Battery'
        out = oisol_scraper(URL)

        expected = {'description': ['Initially intended to provide a mobile platform for '
                 'cumbersome field weapons, the T13 “Deioneus” Rocket Battery '
                 'is a lightweight tankette fitted with a nine-barrelled '
                 'rocket artillery. This unique battery is configured for '
                 'incendiary rockets to be launched at range while maintaining '
                 'high maneuverability between deployments.'],
            'img': 'https://foxhole.wiki.gg/images/8/8d/T13_Deioneus_Rocket_Battery_Icon.png',
            'infobox': {'Ammo': {'4C-Fire Rocket': '4C-Fire Rocket'},
                        'Armament': '4C-Fire Rockets Battery',
                        'Cost': {'Assembly Materials I': '15',
                        'Assembly Materials III': '3',
                        'Processed Construction Materials': '20',
                        'chassis': 'T12 “Actaeon” Tankette',
                        'chassis_link': 'https://foxhole.wiki.gg/wiki/T12_%E2%80%9CActaeon%E2%80%9D_Tankette'},
             'Crew': '2',
             'Disabled Under': '30% health',
             'Fuel Capacity': {'Diesel': 'Diesel',
                               'Petrol': 'Petrol',
                               'Vehicle Fuel Consumption': '150L'},
             'Health': {'Vehicle Health': '1350'},
             'Packaged Size': {'Shippable': 'Small'},
             'Production Site': {'Small Assembly Station': 'Battery Line'},
             'Repair Cost': {'Basic Materials': '150'},
             'Resistance (damage reduction)': {'Anti-Tank Explosive': '-00%',
                                               'Anti-Tank Kinetic': '-00%',
                                               'Armour Piercing': '-00%',
                                               'Damage Resistance': 'Heavy Armor',
                                               'Demolition': '-70%',
                                               'Explosive': '-15%',
                                               'Heavy Kinetic': '-99%',
                                               'High Explosive': '-70%',
                                               'Incendiary High Explosive': '-70%',
                                               'Light Kinetic': '-99%',
                                               'Shrapnel': '-99%'},
             'Subsystems disable chance': {'Tracks': '30%'},
             'Tank Armor': {'7200': '55-80%'},
             'Vehicle Type': {'Tankette': 'Tankette'}},
             'name': 'T13 “Deioneus” Rocket Battery',
             'url': 'https://foxhole.wiki.gg/wiki/T13_%E2%80%9CDeioneus%E2%80%9D_Rocket_Battery'}

        self.assertEqual(out, expected)  # add assertion here


if __name__ == '__main__':
    unittest.main()
