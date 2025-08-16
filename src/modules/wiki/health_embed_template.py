import math
import time

from src.utils import WikiTables, Faction, EMOJIS_FROM_DICT


class HealthEntryEngine:
    def __init__(self, process_data: dict):
        self.__raw_data = process_data

        self.__name = self.__raw_data['name']
        self.__image_url = self.__raw_data['image_url']
        self.__class = self.__raw_data['type']
        self.__case = WikiTables.VEHICLES.value if 'disable' in self.__raw_data else WikiTables.STRUCTURES.value

        if self.__raw_data['faction'] == 'Col':
            self.__faction_color = Faction.COLONIAL.value
        elif self.__raw_data['faction'] == 'War':
            self.__faction_color = Faction.WARDEN.value
        else:
            self.__faction_color = Faction.NEUTRAL.value

        self.__game_damages = self.__sort_damages(self.__raw_data['damages'])
        self.__armor_attributes = self.__raw_data['armor_attributes']

        # There are only two cases possible here, either a struct or a vehicle, each with their own specific attributes
        self.__hp = int(self.__raw_data['structure hp']) if 'structure hp' in self.__raw_data else int(self.__raw_data['vehicle hp'])
        self.__special_hp = (int(self.__raw_data['structure hp entrenched']) if self.__raw_data['structure hp entrenched'] is not None else -1) if 'structure hp entrenched' in self.__raw_data else int(self.__hp) - int(self.__raw_data['vehicle hp']) * (float(self.__raw_data['disable']) / 100)
        self.__embed = {}

    @staticmethod
    def __compute_damage(hp: int, damage: float, resistance: float) -> int:
        """
        :param hp: entry hp
        :param damage: raw damage value
        :param resistance: damage reduction
        :return: ceiled value of amount of nerfed damage required to get to hp
        """
        return math.ceil(hp / (damage - damage * resistance))

    @staticmethod
    def __sort_damages(raw_damages: list) -> dict[str, list]:
        """
        Convert raw data from a list of dict to a dict (k -> damage type & v -> list of damages)
        :param raw_damages: unsorted list of dict
        :return: dict of list damages sorted by category
        """
        sorted_damages = {}
        for damage in raw_damages:
            if (damage_type := damage['damage type']) not in sorted_damages:
                sorted_damages[damage_type] = []
            sorted_damages[damage_type].append(damage)

        return sorted_damages

    def __prepare_embed(self):
        """
        Format attributes to discord embed format
        """
        self.__embed['title'] = self.__name
        self.__embed['description'] = f'Class: {self.__class}'
        self.__embed['color'] = self.__faction_color
        self.__embed['thumbnail'] = {'url': self.__image_url}
        self.__embed['fields'] = []

    def get_generated_embed(self) -> dict:
        """
        Public entry point for the engine
        :return: dict ready to be used as a discord embed
        """
        start_time = time.time()
        self.__prepare_embed()
        self.__process_all_damages()
        print(time.time() - start_time)
        return self.__embed

    def __format_results(
            self,
            damage_name: str,
            main_value: int,
            special_value: int,
            main_value_rng: int | None = None,
            special_value_rng: int | None = None
    ) -> str:
        """
        Convert computed results to a string to add to the discord embed
        :param damage_name: self-explanatory (e.g. -> 40mm)
        :param main_value: amount to destroy
        :param special_value: amount to either disable or to destroy when entrenched, self.__case dependent
        :param main_value_rng: main_value * 1.5 when damage_dict[damage rng] is not None
        :param special_value_rng: special_value * 1.5 when damage_dict[damage rng] is not None
        :return: formatted string with discord emoji
        """
        damage_result = f'{EMOJIS_FROM_DICT.get(damage_name, damage_name)}: '

        if self.__case == WikiTables.VEHICLES.value:
            if main_value_rng is None:
                return  damage_result + f'{special_value} **|** {main_value}'
            return damage_result + f'{special_value_rng}-{special_value} **|** {main_value_rng}-{main_value}'

        ## Structure cases
        # Case where the struct has a single state
        if self.__special_hp == -1:
            if main_value_rng is not None:
                return damage_result + f'{main_value}-{main_value_rng}'
            return damage_result + f'{main_value}'

        # Case
        if main_value_rng is None:
            return damage_result + f'{main_value} **|** {special_value}'
        return damage_result + f'{main_value}-{main_value_rng} **|** {special_value}-{special_value_rng}'

    def __process_all_damages(self):
        """
        main engine method
        """
        for category_name, category_damages in self.__game_damages.items():
            category_field = {'name': f'{category_name.upper()}{f' ({emoji})' if (emoji := EMOJIS_FROM_DICT.get(category_name, '')) else ''}', 'value': ''}

            for i, damage_dict in enumerate(category_damages):
                armor_damage_reduction = float(self.__armor_attributes[damage_dict['damage type']])

                # Case where the damage reduction is at a 100%, thus no damage
                if armor_damage_reduction >= 1:
                    break
                damage_value = int(damage_dict['damage'])

                number_to_kill = self.__compute_damage(self.__hp, damage_value, armor_damage_reduction)
                # Case where the amount to destroy is too much
                if number_to_kill > 500:
                    break
                number_to_kill_special = self.__compute_damage(self.__special_hp, damage_value, armor_damage_reduction)

                if damage_dict['damage rng'] == '1':
                    damage_value_rng = damage_value * 1.5
                    number_to_kill_max = self.__compute_damage(self.__hp, damage_value_rng, armor_damage_reduction)

                    number_to_kill_special_max = self.__compute_damage(self.__special_hp, damage_value_rng, armor_damage_reduction)

                    string_res = self.__format_results(
                        damage_dict['name'],
                        number_to_kill,
                        number_to_kill_special,
                        number_to_kill_max,
                        number_to_kill_special_max
                    )
                else:
                    string_res = self.__format_results(damage_dict['name'], number_to_kill, number_to_kill_special)
                category_field['value'] += f'{string_res}{'\n' if i and not i % 3 else '   '}'

            # No need to add empty titles with no related damages
            if category_field['value']:
                self.__embed['fields'].append(category_field)
