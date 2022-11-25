import json
import os.path

from Base import Base


def get_base_consumption(base: Base) -> (str, int):
    consumption_rate = base.get_maintenance_consumption()
    if not any(consumption_rate):
        return "> La base ne nécessite aucune maintenance.", -1
    result = "> __Consommation actuelle__:\n\t"
    result += f"> _Bsup_: **{consumption_rate[0]}** {'unité' if consumption_rate[0] <= 1 else 'unités'} par heure (**{consumption_rate[0] * 24}** par jour).\n\t"
    result += f"> _Gsup_: **{consumption_rate[1]}** {'unité' if consumption_rate[1] <= 1 else 'unités'} par heure (**{consumption_rate[1] * 24}** par jour).\n"
    return result, 1


def get_base_time_left(base: Base) -> str:
    consumption_rate = base.get_maintenance_consumption()
    stockpile = base.get_maintenance_stockpile()

    result = "> __Temps restant__:\n\t"
    if consumption_rate[0] > 0:
        time_left_bsup = stockpile[0] / consumption_rate[0]
        result += f"> _Gsup_: " + f"{int(time_left_bsup)}h." if time_left_bsup > 0 else f"> _Gsup_: Le stockpile est vide !"
    if consumption_rate[1] > 0:
        time_left_gsup = stockpile[1] / consumption_rate[1]
        result += f"> _Gsup_: " + f"{int(time_left_gsup)}h." if time_left_gsup > 0 else f"> _Gsup_: Le stockpile est vide !"
    return result


def get_base_maintenance_status(base: Base) -> str:
    base_stockpile = base.get_maintenance_stockpile()
    result = f"> __Unité(s) en stock__:\n\t> _Bsup_: **{base_stockpile[0]}** {'unité' if base_stockpile[0] <= 1 else 'unités'}.\n\t> _Gsup_: **{base_stockpile[1]}** {'unité' if base_stockpile[1] <= 1 else 'unités'}.\n"
    consumption_rate = get_base_consumption(base)
    result += consumption_rate[0]
    if consumption_rate[1] > 0:
        result += get_base_time_left(base)
    return result + "\n"


def save_bases(bases: [Base]):
    with open("saves/bases.json", "w") as file:
        json.dump([bases[key].__dict__ for key in bases.keys()], file)


def load_bases() -> dict:
    if not os.path.isfile("saves/bases.json"):
        return dict()
    final_data = dict()
    try:
        with open("saves/bases.json", "r") as file:
            data = json.load(file)
        for elem in data:
            final_data[elem["name"]] = Base(elem["name"])
    except json.decoder.JSONDecodeError:
        return dict()
    return final_data
