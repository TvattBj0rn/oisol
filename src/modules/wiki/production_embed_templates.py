import datetime
import math

from src.utils import EMOJIS_FROM_DICT, Faction


class ProductionTemplate:
    def __init__(self, data: list[dict], name: str, img_link: str, bot_emojis: dict):
        self.__raw_data = data
        self.__bot_emojis = bot_emojis
        self.__name = name
        self.__img_link = img_link
        self.__color = Faction[self.__raw_data[0].get('Faction', 'NEUTRAL').replace('Both', 'NEUTRAL').replace('War', 'WARDEN').replace('Col', 'COLONIAL')].value
        self.__output = []

    @staticmethod
    def __apply_mpf_formula(default_cost: int, is_short_mpf: bool) -> list[int]:
        """
        Apply foxhole MPF formula, from a default resource cost. See https://foxhole.wiki.gg/wiki/Mass_Production_Factory for formula.
        :param is_short_mpf: number to iterate to
        :param default_cost: default cost of an item
        :return: price reduction for each mpf tier
        """
        increase_costs = [0.1, 0.2, 0.3, 0.4, 0.5] if is_short_mpf else [0.1, 0.2, 0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5]
        return [sum(default_cost - math.ceil(default_cost * increase_costs[j]) for j in range(i)) for i in range(1, len(increase_costs) + 1)]

    def __process_mpf(self, mpf_parameters: dict[str, str]) -> None:
        mpf_embed = {
            'title': 'Mass Production Factory',
            'description': '',
            'color': self.__color,
            'fields': [],
        }
        is_short_mpf = False

        # For vics, base cost depend on the number of vics per output crate
        if mpf_parameters.get('Source', '') == 'Garage':
            is_short_mpf = True
            cost_multiplier = 5 if mpf_parameters['CrateCapacity'] == '5' else 3
            for i in range(1, 7):
                if not mpf_parameters[f'InputItem{i}']:
                    break
                mpf_parameters[f'InputItem{i}Amount'] = str(int(mpf_parameters[f'InputItem{i}Amount']) * cost_multiplier)

        production_costs = {}
        for i in range(1, 7):
            if not mpf_parameters[f'InputItem{i}']:
                break

            production_costs[mpf_parameters[f'InputItem{i}']] = [f'x{cost}  {self.__bot_emojis.get(EMOJIS_FROM_DICT.get(mpf_parameters[f'InputItem{i}']), self.__bot_emojis.get('missing_texture'))}' for cost in self.__apply_mpf_formula(int(mpf_parameters[f'InputItem{i}Amount']), is_short_mpf)]

        for i in range(len(next(iter(production_costs.values())))):
            mpf_embed['fields'].append({
                'name': f'{i + 1} Crate' if i + 1 == 1 else f'{i + 1} Crates',
                'value': '\n'.join(cost_type[i] for cost_type in production_costs.values()),
                'inline': True,
            })

        self.__output.append(mpf_embed)

    def __prepare_embeds_data(self) -> None:
        available_structs = set()  # This is used for header embed
        for production_method in self.__raw_data:
            available_structs.add(production_method['Source'])
            structure_embed = {
                'title': production_method['Source'],
                'description': '',
                'color': self.__color,
                'fields': [],
            }
            # Add any inputs that are not null (there can be null inputs between non-null inputs -> the loop must check all iterations)
            structure_embed['fields'].extend({
                'name': 'Input',
                'value': f'x{production_method[f'{input_item_title}Amount']} {self.__bot_emojis.get(EMOJIS_FROM_DICT.get(production_method[input_item_title]), self.__bot_emojis.get('missing_texture'))}',
                'inline': True,
            } for i in range(1, 7) if production_method[input_item_title := f'InputItem{i}'])

            for category_name, display_name, action in [
                ('InputVehicle', 'Chassis', lambda value: value),
                ('InputPower', 'Power', lambda value: f'{value}  {self.__bot_emojis.get(EMOJIS_FROM_DICT.get('MW of power'), self.__bot_emojis.get('missing_texture'))}'),
                ('ProductionTime', 'Time', lambda value: f'{datetime.timedelta(seconds=float(value))}'),
                ('Output', 'Output', lambda value: value),
            ]:
                if production_method.get(category_name):
                    structure_embed['fields'].append({
                        'name': display_name,
                        'value': action(production_method[category_name]),
                        'inline': True,
                    })

            if 'Output' not in production_method:
                for i in range(1, 4):
                    if (output_item_title := f'OutputItem{i}') in production_method and production_method[output_item_title]:
                        structure_embed['fields'].append({
                            'name': 'Output',
                            'value': f'x{production_method[f'{output_item_title}Amount']} {production_method[output_item_title]}  {self.__bot_emojis.get(EMOJIS_FROM_DICT.get(production_method[output_item_title]), self.__bot_emojis.get('missing_texture'))}',
                            'inline': True,
                        })
                    else:
                        break

            self.__output.append(structure_embed)
            if production_method.get('IsMPFable', False) == '1' and production_method['Source'] in ['Garage', 'Factory']:
                available_structs.add('Mass Production Factory')
                self.__process_mpf(production_method.copy())

        # Insert embed, after all available productions structs were retrieved
        self.__output.insert(
            0,
            {
                'title': self.__name,
                'description': f'Available structures:\n- {'\n- '.join(available_structs)}',
                'thumbnail': {'url': self.__img_link},
                'color': self.__color,
            })


    def get_generated_embeds(self) -> list[dict[str, str | list]]:
        self.__prepare_embeds_data()
        return self.__output
