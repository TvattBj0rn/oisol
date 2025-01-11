import math


def apply_mpf_formula(default_cost: int, is_short_mpf: bool) -> [int]:
    """
    Apply foxhole MPF formula, from a default resource cost. See https://foxhole.wiki.gg/wiki/Mass_Production_Factory for formula.
    :param is_short_mpf: number to iterate to
    :param default_cost: default cost of an item
    :return: price reduction for each mpf tier
    """
    increase_costs = [0.1, 0.2, 0.3, 0.4, 0.5] if is_short_mpf else [0.1, 0.2, 0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5]
    return [sum(default_cost - math.ceil(default_cost * increase_costs[j]) for j in range(i)) for i in range(1, len(increase_costs) + 1)]


def generate_mpf_data(production_costs: list[str], is_short_mpf: bool) -> dict:
    """
    Convert each production cost ot a list of price reduction
    :param is_short_mpf: if True 5, else 9
    :param production_costs: list of resource(s) number / name from a raw str format
    :return: dict of price reduction list for each given resource
    """
    mpf_costs = {}
    for pc in production_costs:
        resource_cost, resource_name = pc.split(' x ')
        mpf_costs[resource_name] = apply_mpf_formula(int(resource_cost), is_short_mpf)
    return mpf_costs
