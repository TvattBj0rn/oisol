import math


def apply_mpf_formula(default_cost: int) -> [int]:
    """
    Apply foxhole MPF formula, from a default resource cost. See https://foxhole.wiki.gg/wiki/Mass_Production_Factory for formula.
    :param default_cost: default cost of an item
    :return: price reduction for each mpf tier
    """
    return [sum(default_cost - math.ceil(default_cost * [0.1, 0.2, 0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.5][j]) for j in range(i)) for i in range(1, 10)]


def generate_mpf_data(production_costs: list[str]) -> dict:
    """
    Convert each production cost ot a list of price reduction
    :param production_costs: list of resource(s) number / name from a raw str format
    :return: dict of price reduction list for each given resource
    """
    mpf_costs = {}
    for pc in production_costs:
        resource_cost, resource_name = pc.split(' x ')
        mpf_costs[resource_name] = apply_mpf_formula(int(resource_cost))
    return mpf_costs
