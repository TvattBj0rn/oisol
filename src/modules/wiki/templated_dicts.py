import abc

from src.utils import EMOJIS_FROM_DICT
from src.utils.oisol_enums import Faction


class WikiTemplate(abc.ABC):
    def __init__(self, data_dict: dict):
        self._raw_data = data_dict

    @abc.abstractmethod
    def _process_categories(self) -> list:
        pass

    @abc.abstractmethod
    def generate_embed_data(self) -> dict:
        pass


class VehicleTemplate(WikiTemplate):
    def __init__(self, data_dict: dict):
        super().__init__(data_dict)
        self._categories_attributes = {
            'SURVIVABILITY': [
                {'name': 'Health', 'value': f'{vic_hp} HP' if (vic_hp := self._raw_data.get('vehicle hp')) else '', 'inline': True},  # Health
                {'name': 'Disable Threshold', 'value': f'{disable}%' if (disable := self._raw_data.get('disable')) else '', 'inline': True},  # Disable
                {'name': 'Subsystems disable chance', 'value': f'{
                (f'- Tracks (<:tracked:1239349968767291454>): {tracks_chance}%\n' if (tracks_chance := self._raw_data.get('disable chance tracks')) else '') +
                (f'- Fuel Tank (<:fuel_leak:1239349986471313499>): {fuel_chance}%\n' if (fuel_chance := self._raw_data.get('disable chance fueltank')) else '') +
                (f'- Main Turret (<:turret:1239349978170921060>): {turret_1_chance}%\n' if (turret_1_chance := self._raw_data.get('disable chance turret')) else '') +
                (f'- Secondary Turret (<:secondary_turret_cannon:1239616804184264818>): {turret_2_chance}%\n' if (turret_2_chance := self._raw_data.get('disable chance turret2')) else '')
                }', 'inline': True},  # Subsystems disable chance
                {'name': f'Armor type: *{self._raw_data.get('armour type')}*', 'value': f'{
                ''.join(f'- {attribute_name} ({EMOJIS_FROM_DICT.get(attribute_name)}): -{float(attribute_value) * 100}%\n' for attribute_name, attribute_value in self._raw_data.get('armour_attributes').items())
                }', 'inline': True}, # Vic Armor and damage reductions
                {'name': 'Armor HP', 'value': f'{armor_hp} HP' if (armor_hp := self._raw_data.get('armour hp')) else '', 'inline': True} # Armor HP / Penetration chances
            ],
            'MISC': [
                {'name': 'Class', 'value': str(vic_type) if (vic_type := self._raw_data.get('vehicle type')) is not None else '', 'inline': True}, # Vic Class
                {'name': 'Crew', 'value': str(crew) if (crew := self._raw_data.get('crew')) is not None else '', 'inline': True}, # Crew number
                {'name': 'Passengers', 'value': str(passengers) if (passengers := self._raw_data.get('passengers')) is not None else '', 'inline': True}, # Passengers
                {'name': 'Inventory slots', 'value': str(slots) if (slots := self._raw_data.get('slots')) is not None else '', 'inline': True}, # Inventory slots
            ],
            'ENGINE': [
                {'name': 'Fuel Capacity', 'value': f'{fuel_cap}{'U' if self._raw_data.get('fueltype') == 'Coal' else 'L'}{f', {f'Diesel ({EMOJIS_FROM_DICT.get('Diesel')}) / Petrol ({EMOJIS_FROM_DICT.get('Petrol')})' if (fuel_type := self._raw_data.get('fueltype')) is None else f'{fuel_type} ({EMOJIS_FROM_DICT.get(fuel_type)})'}'}' if (fuel_cap := self._raw_data.get('fuelcap')) is not None else '', 'inline': True}, # Fuel type + capacity
                {'name': 'Speed', 'value': f'{
                f'{f'- On road: {speed} m/s\n' if (speed := self._raw_data.get('speed')) else ''}' +
                f'{f'- On road (boost): {speed_boost} m/s\n' if (speed_boost := self._raw_data.get('boostspeed')) else ''}' +
                f'{f'- Off road: {offspeed} m/s\n' if (offspeed := self._raw_data.get('offspeed')) else ''}' +
                f'{f'- Off road (boost): {offspeed_boost} m/s\n' if (offspeed_boost := self._raw_data.get('boostspeed off')) else ''}' +
                f'{f'- On water: {water} m/s\n' if (water := self._raw_data.get('waterspeed')) else ''}' +
                f'{f'- On water (boost): {water_boost} m/s\n' if (water_boost := self._raw_data.get('boostspeed water')) else ''}'
                }', 'inline': True}, # All speeds (Road / Offroad / Water / Boost)
            ],
            'ARMAMENT': [
                {'name': '', 'value': f'{
                ''.join(f'- {gun_attribute} ({EMOJIS_FROM_DICT.get(self._raw_data.get(f'A{i} AmmoName'))}), range of {self._raw_data.get(f'A{i} RangeMax')}m\n' for i in range(1, 5) if (gun_attribute := self._raw_data.get(f'A{i} ArmamentName')) is not None)
                }', 'inplace': True} # All guns
            ],
        }

    def _process_categories(self) -> list:
        filled_categories = []
        for category_name, category_attributes in self._categories_attributes.items():
            category_attributes = [attribute for attribute in category_attributes if attribute.get('value')]
            if len(category_attributes) > 0:
                filled_categories += [{'name': category_name, 'value': ''}] + category_attributes
        return filled_categories

    def generate_embed_data(self) -> dict:
        print(self._raw_data)
        embeded_dict = {
            'title': self._raw_data.get('name'),
            'description': '',
            'color': Faction.COLONIAL.value if self._raw_data.get('faction') == 'Col' else Faction.WARDEN.value if self._raw_data.get('faction') == 'War' else Faction.NEUTRAL.value,
            'thumbnail': {'url': self._raw_data.get('image_url')},
            'fields': self._process_categories(),
        }
        return embeded_dict


