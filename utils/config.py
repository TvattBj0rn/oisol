import json
import os


def create_config_file(server_id: str = ""):
    path = f"saves/{server_id}/config.json"
    default_config_dict = {"alert_channel": 0}
    if not os.path.isfile(path):
        with open(path, "w") as file:
            json.dump(default_config_dict, file)


def load_config(server_id: str = "") -> dict:
    path = f"saves/{server_id}/config.json"
    if not os.path.isfile(path):
        return dict()
    try:
        with open(path, "r") as file:
            config = json.load(file)
    except json.decoder.JSONDecodeError:
        return dict()
    return config


def update_config(server_id: str = "", new_config: dict = dict):
    path = f"saves/{server_id}/config.json"
    if not os.path.isfile(path):
        return
    with open(path, "w") as file:
        json.dump(new_config, file)
