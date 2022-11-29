import json
import os


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
