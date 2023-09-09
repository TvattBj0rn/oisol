import platform
from enum import Enum


def generate_path(server_id: int, file: str) -> str:
    if platform.node() == 'fedora':
        return f'./oisol/{server_id}/{file}'
    return f'/oisol/{server_id}/{file}'


def get_root_path() -> str:
    if platform.node() == 'fedora':
        return f'./oisol/'
    return f'/oisol/'


class DataFilesPath(Enum):
    REGISTER = 'register.csv'
    STOCKPILES = 'stockpiles.csv'
    CONFIG = 'config.ini'