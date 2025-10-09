import datetime
import math

from src.utils import Faction, EMOJIS_FROM_DICT


class ProductionTemplate:
    def __init__(self, data: list[dict], name: str):
        self.__raw_data = data
        self.__name = name
        self.__color = Faction[self.__raw_data[0].get('Faction', 'NEUTRAL').replace('Both', 'NEUTRAL').upper()].value
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

    def __process_mpf(self, mpf_parameters: dict[str, str]):
        mpf_embed = {
            'title': 'Mass Production Factory',
            'description': '',
            'color': self.__color,
            'fields': [],
        }
        is_short_mpf = False

        # For vics, base cost depend on the number of vics per output crate
        if 'MPFOutputAmount' in mpf_parameters:
            is_short_mpf = True
            cost_multiplier = 5 if mpf_parameters['MPFOutputAmount'] == '5' else 3
            for i in range(1, 7):
                if mpf_parameters[f'InputItem{i}'] is None:
                    break
                mpf_parameters[f'InputItem{i}Amount'] = str(int(mpf_parameters[f'InputItem{i}Amount']) * cost_multiplier)

        production_costs = {}
        for i in range(1, 7):
            if mpf_parameters[f'InputItem{i}'] is None:
                break
            production_costs[mpf_parameters[f'InputItem{i}']] = [f'x{cost}  {EMOJIS_FROM_DICT.get(mpf_parameters[f'InputItem{i}'], '')}' for cost in self.__apply_mpf_formula(int(mpf_parameters[f'InputItem{i}Amount']), is_short_mpf)]

        for i in range(len(list(production_costs.values())[0])):
            mpf_embed['fields'].append({
                'name': f'{i + 1} Crate' if i + 1 == 1 else f'{i + 1} Crates',
                'value': '\n'.join(cost_type[i] for cost_type in production_costs.values()),
                'inline': True,
            })

        self.__output.append(mpf_embed)

    def __prepare_embeds_data(self):
        for production_method in self.__raw_data:
            structure_embed = {
                'title': production_method['StructureName'],
                'description': '',
                'color': self.__color,
                'fields': [],
            }
            # Max input item is 6
            for i in range(1, 7):
                # production & productionmerged tables do not have the same amount of input items
                if (input_item_title := f'InputItem{i}') in production_method and production_method[input_item_title] is not None:
                    structure_embed['fields'].append({
                        'name': 'Input',
                        'value': f'x{production_method[f'{input_item_title}Amount']} {EMOJIS_FROM_DICT.get(production_method[input_item_title], production_method[input_item_title])}',
                        'inline': True,
                    })
                else:
                    break
            for category_name, display_name, action in [
                ('InputVehicle', 'Chassis', lambda value: value),
                ('InputPower', 'Power', lambda value: f'{value}  {EMOJIS_FROM_DICT.get('MW of power', '')}'),
                ('ProductionTime', 'Time', lambda value: f'{datetime.timedelta(seconds=float(value))}'),
                ('Output', 'Output', lambda value: value)
            ]:
                if category_name in production_method and production_method[category_name] is not None:
                    structure_embed['fields'].append({
                        'name': display_name,
                        'value': action(production_method[category_name]),
                        'inline': True,
                    })

            if 'Output' not in production_method:
                for i in range(1, 4):
                    if (output_item_title := f'OutputItem{i}') in production_method and production_method[output_item_title] is not None:
                        structure_embed['fields'].append({
                            'name': 'Output',
                            'value': f'x{production_method[f'{output_item_title}Amount']} {production_method[output_item_title]}  {EMOJIS_FROM_DICT.get(production_method[output_item_title], '')}',
                            'inline': True,
                        })
                    else:
                        break

            self.__output.append(structure_embed)
            if (mpf_flag := production_method.get('IsMPFable', False)) and mpf_flag == '1' and production_method['StructureName'] in ['Garage', 'Factory']:
                self.__process_mpf(production_method.copy())


    def get_generated_embeds(self):
        self.__prepare_embeds_data()
        return self.__output
