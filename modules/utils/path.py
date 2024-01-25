import platform
from enum import Enum
from deprecated import deprecated


@deprecated(reason='This will be removed soon')
def generate_path(server_id: int, file: str) -> str:
    if platform.node() == 'fedora':
        return f'./oisol/{server_id}/{file}'
    return f'/oisol/{server_id}/{file}'


@deprecated(reason='This will be removed soon')
def get_root_path() -> str:
    if platform.node() == 'fedora':
        return f'./oisol/'
    return f'/oisol/'


@deprecated(reason='This will be removed soon')
class DataFilesPath(Enum):
    REGISTER = 'register.csv'
    STOCKPILES = 'stockpiles.csv'
    CONFIG = 'config.ini'
