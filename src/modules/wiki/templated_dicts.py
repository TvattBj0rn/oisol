from src.utils import EMOJIS_FROM_DICT, WikiTables, convert_time_to_readable_time, Faction, NUMBER_TO_EQUIPMENT_SLOT


class Damage:
    def __init__(self, raw_damage: str, damage_multiplier: str | None, damage_rng: str | None):
        self._raw_damage = int(raw_damage)
        self._damage_multiplier = float(damage_multiplier) if damage_multiplier is not None else 1.0
        self._net_damage = int(self._raw_damage * self._damage_multiplier)
        self._damage_rng = True if damage_rng == '1' else False
        self._net_damage_rng = int(self._net_damage * 1.5)

    def get(self) -> str:
        if self._damage_rng:
            return f'{self._net_damage}-{self._net_damage_rng}'
        return f'{self._net_damage}'


class WikiTemplate:
    def __init__(self, data_dict: dict):
        self._raw_data = data_dict
        self._categories_attributes = {}

    @staticmethod
    def _create_formatted_attribute(name: str, value: str, inline: bool = True):
        return {'name': name, 'value': value, 'inline': inline}

    def _add_armor_attribute(self, inplace: bool = True):
        return {
            'name': f'Armor type: *{self._raw_data.get('armour type')}*',
            'value': f'{''.join(f'- {attribute_name} ({EMOJIS_FROM_DICT.get(attribute_name)}): -{float(attribute_value) * 100}%\n' for attribute_name, attribute_value in self._raw_data.get('armour_attributes').items())}',
            'inplace': inplace,
        }

    def _generate_armament_value(self, armament_id: int) -> str:
        is_armament_valid = any((
            main_name := self._raw_data.get(f'A{armament_id} ArmamentName'),
            ammo_name := self._raw_data.get(f'A{armament_id} AmmoName'),
            velocity_mod := self._raw_data.get(f'A{armament_id} VelocityMod'),
            reload_time := self._raw_data.get(f'A{armament_id} ReloadTime'),
            gun_range := self._raw_data.get(f'A{armament_id} RangeMax'),
            effective_range := self._raw_data.get(f'A{armament_id} RangeEffective'),
            retaliation_range := self._raw_data.get('retaliation range'),
        ))
        if not is_armament_valid:
            return ''
        return (
            f'{main_name if main_name is not None else self._raw_data.get('name')}{f' ({EMOJIS_FROM_DICT.get(ammo_name)})' if ammo_name is not None else ''}\n'
            + (f'- Velocity of {velocity_mod}%\n' if velocity_mod is not None else '')
            + (f'- Reload time of {reload_time}s\n' if reload_time is not None else '')
            + (f'- Range of {gun_range}m' if gun_range is not None else '')
            + (f', effective range of {effective_range}m' if effective_range is not None else '')
            + (f', retaliates up to {retaliation_range}m' if retaliation_range is not None else '')
            + '\n'
        )

    def _process_categories(self) -> list[dict]:
        """
        This take all generated attributes and remove empty values one and add categories as section
        :return: category attribute in list of dicts following discord embed fields specifications (name / value / inline as keys)
        """
        filled_categories = []
        for category_name, category_attributes in self._categories_attributes.items():
            if len(filled_category_attributes := [attribute for attribute in category_attributes if attribute.get('value')]) > 0:
                filled_categories += [{'name': category_name, 'value': ''}] + filled_category_attributes
        return filled_categories

    def generate_embed_data(self) -> dict:
        return {
            'title': self._raw_data.get('name'),
            'description': '',
            'color': Faction.COLONIAL.value if self._raw_data.get('faction') == 'Col'
            else Faction.WARDEN.value if self._raw_data.get('faction') == 'War'
            else Faction.NEUTRAL.value,
            'thumbnail': {'url': self._raw_data.get('image_url')},
            'fields': self._process_categories(),
        }


class VehicleTemplate(WikiTemplate):
    def __init__(self, data_dict: dict):
        super().__init__(data_dict)
        self._categories_attributes = {
            'SURVIVABILITY': [
                self._create_formatted_attribute('Health', f'{vic_hp} HP' if (vic_hp := self._raw_data.get('vehicle hp')) else ''),
                self._create_formatted_attribute('Disable threshold', f'{disable}%' if (disable := self._raw_data.get('disable')) else ''),
                self._create_formatted_attribute('Subsystems disable chance', f'{
                (f'- Tracks (<:tracked:1239349968767291454>): {tracks_chance}%\n' if (tracks_chance := self._raw_data.get('disable chance tracks')) else '') +
                (f'- Fuel Tank (<:fuel_leak:1239349986471313499>): {fuel_chance}%\n' if (fuel_chance := self._raw_data.get('disable chance fueltank')) else '') +
                (f'- Main Turret (<:turret:1239349978170921060>): {turret_1_chance}%\n' if (turret_1_chance := self._raw_data.get('disable chance turret')) else '') +
                (f'- Secondary Turret (<:secondary_turret_cannon:1239616804184264818>): {turret_2_chance}%\n' if (turret_2_chance := self._raw_data.get('disable chance turret2')) else '')
                }'),
                self._add_armor_attribute(),
                self._create_formatted_attribute('Armor HP', f'{armor_hp} HP' if (armor_hp := self._raw_data.get('armour hp')) else ''),
            ],
            'MISC': [
                self._create_formatted_attribute('Class', str(vic_type) if (vic_type := self._raw_data.get('vehicle type')) is not None else ''),
                self._create_formatted_attribute('Crew', str(crew) if (crew := self._raw_data.get('crew')) is not None else ''),
                self._create_formatted_attribute('Passengers', str(passengers) if (passengers := self._raw_data.get('passengers')) is not None else ''),
                self._create_formatted_attribute('Inventory slots', str(slots) if (slots := self._raw_data.get('slots')) is not None else ''),
            ],
            'ENGINE': [
                self._create_formatted_attribute('Fuel Capacity', f'{fuel_cap}{'U' if self._raw_data.get('fueltype') == 'Coal' else 'L'}{f', {f'Diesel ({EMOJIS_FROM_DICT.get('Diesel')}) / Petrol ({EMOJIS_FROM_DICT.get('Petrol')})' if (fuel_type := self._raw_data.get('fueltype')) is None else f'{fuel_type} ({EMOJIS_FROM_DICT.get(fuel_type)})'}'}' if (fuel_cap := self._raw_data.get('fuelcap')) is not None else ''),
                self._create_formatted_attribute('Speed', f'{
                f'{f'- On road: {speed} m/s\n' if (speed := self._raw_data.get('speed')) else ''}' +
                f'{f'- On road (boost): {speed_boost} m/s\n' if (speed_boost := self._raw_data.get('boostspeed')) else ''}' +
                f'{f'- Off road: {offspeed} m/s\n' if (offspeed := self._raw_data.get('offspeed')) else ''}' +
                f'{f'- Off road (boost): {offspeed_boost} m/s\n' if (offspeed_boost := self._raw_data.get('boostspeed off')) else ''}' +
                f'{f'- On water: {water} m/s\n' if (water := self._raw_data.get('waterspeed')) else ''}' +
                f'{f'- On water (boost): {water_boost} m/s\n' if (water_boost := self._raw_data.get('boostspeed water')) else ''}'
                }'),
            ],
            'ARMAMENT': [
                self._create_formatted_attribute('', ''.join(self._generate_armament_value(i) for i in range(1, 5)))
            ],
        }


class StructureTemplate(WikiTemplate):
    def __init__(self, data_dict: dict):
        super().__init__(data_dict)
        self._categories_attributes = {
            'SURVIVABILITY': [
                self._create_formatted_attribute('Health', f'{f'{struct_hp} HP' if (struct_hp := self._raw_data.get('structure hp')) is not None else ''}{f'\nEntrenched: {entrenched_hp} HP' if (entrenched_hp := self._raw_data.get('structure hp entrenched')) is not None else ''}{
                f'\nDecay start after: {convert_time_to_readable_time(float(decay_start))}' if (decay_start := self._raw_data.get('decay start')) is not None else ''}{
                f'\nDecay duration: {convert_time_to_readable_time(float(decay_duration))}' if (decay_duration := self._raw_data.get('decay duration')) is not None else ''
                }'),
                self._create_formatted_attribute('Husk & Husk decay', f'{f'{husk_hp} HP' if (husk_hp := self._raw_data.get('husk hp')) is not None else ''}{
                f'\nDecay start after: {convert_time_to_readable_time(float(husk_decay_start))}' if (husk_decay_start := self._raw_data.get('husk decay start')) is not None else ''}{
                f'\nDecay duration: {convert_time_to_readable_time(float(husk_decay_duration))}' if (husk_decay_duration := self._raw_data.get('husk decay duration')) is not None else ''
                }'),
                self._add_armor_attribute(),
            ],
            'STRUCTURE SUPPORT': [
                self._create_formatted_attribute('Intel range', f'{intel_range}m' if (intel_range := self._raw_data.get('intel range')) is not None else ''),
                self._create_formatted_attribute('AI range', f'{ai_range}m' if (ai_range := self._raw_data.get('ai range')) is not None else ''),
                self._create_formatted_attribute('Construction', f'x{build_amount} {build_material}{f' {EMOJIS_FROM_DICT.get(build_material, '')} '} using {built_with}{f' {EMOJIS_FROM_DICT.get(built_with, '')}'}' if any(((build_amount := self._raw_data.get('build amount')), (build_material := self._raw_data.get('build material')), (built_with := self._raw_data.get('built with')))) else '')
            ],
            'ARMAMENT': [
                self._create_formatted_attribute('', self._generate_armament_value(1))
            ],
        }


class ItemTemplate(WikiTemplate):
    def __init__(self, data_dict: dict):
        super().__init__(data_dict)

        self._damage_range = lambda d, m: f'{int(d) * int(m)}-'
        self._categories_attributes = {
            'ITEM': [
                self._create_formatted_attribute('Category', f'{f'{item_category}{f' ({category_emoji})' if (category_emoji := EMOJIS_FROM_DICT.get(item_category)) is not None else ''}'}' if (item_category := self._raw_data.get('category')) is not None else ''),
                self._create_formatted_attribute('Class', f'{item_class}' if (item_class := self._raw_data.get('type')) is not None else ''),
                self._create_formatted_attribute('Equipment slot', f'{NUMBER_TO_EQUIPMENT_SLOT.get(slot)}' if (slot := self._raw_data.get('slot')) is not None else ''),
                self._create_formatted_attribute('Use', f'{uses}' if (uses := self._raw_data.get('uses')) is not None else ''),
                self._create_formatted_attribute('Amount per crate', f'{crate_amount}' if (crate_amount := self._raw_data.get('crate amount')) is not None else '')
            ],
            'ARMAMENT': [
                self._create_formatted_attribute('Firing mode', f'{firing_mode}' if (firing_mode := self._raw_data.get('firing mode')) is not None else ''),
                self._create_formatted_attribute(
                    'Damage',
                    f'{
                        f'{Damage(damage_info['damage'], self._raw_data.get('damage multiplier'), damage_info['damage rng']).get()}{f' ({EMOJIS_FROM_DICT.get(damage_info['damage type'])})'}'
                        f'{f'\nSemi automatic mode: {Damage(damage_info['damage'], self._raw_data.get('damage multiplier2'), damage_info['damage rng']).get()}{f' ({EMOJIS_FROM_DICT.get(damage_info['damage type'])})'}' if self._raw_data.get('firing mode') == 'Auto / Semi' else ''}'
                    }' if (damage_info := self._raw_data.get('ammo_info')) is not None else ''
                ),
                self._create_formatted_attribute(
                    'Range',
                    (f'- Effective range: {range_effective}m' if (range_effective := self._raw_data.get('range effective')) is not None else '')
                    + (f'\n- Maximum range: {range_max}m' if (range_max := self._raw_data.get('range max')) is not None else '')
                    + (f'\n- Effective range (semi automatic mode): {range_effective2}m' if (range_effective2 := self._raw_data.get('range effective2')) is not None else '')
                    + (f'\n- Maximum range (semi automatic mode): {range_max2}m' if (range_max2 := self._raw_data.get('range max2')) is not None else '')
                ),
                self._create_formatted_attribute(
                    'Ammunition',
                    (f'Shoots {all_ammo}' if (all_ammo := ', '.join(f'{v}{f' ({EMOJIS_FROM_DICT.get(self._raw_data[k])})'}' for k in ['ammo', 'ammo2', 'ammo3', 'ammo4'] if (v := self._raw_data[k]) is not None)) else '')
                    + (f'\n- Magazine size of {mag_size}' if (mag_size := self._raw_data.get('magazine')) is not None else '')
                    + (f'\n- Reload time of {reload_time}s' if (reload_time := self._raw_data.get('reload')) is not None else '')
                ),
                self._create_formatted_attribute('Damage', f'{Damage(self._raw_data.get('damage'), self._raw_data.get('damage multiplier'), self._raw_data.get('damage rng')).get()} ({EMOJIS_FROM_DICT.get(self._raw_data.get('damage type'))})' if self._raw_data.get('damage') is not None else ''),
            ],
        }



class WikiTemplateFactory:
    table_to_template_mapping = {
        WikiTables.VEHICLES: VehicleTemplate,
        WikiTables.STRUCTURES: StructureTemplate,
        WikiTables.ITEM_DATA: ItemTemplate,
    }

    def __init__(self, data_dict: dict):
        self._data_dict = data_dict

    def get(self, table: WikiTables) -> WikiTemplate:
        return self.table_to_template_mapping[table](self._data_dict)
