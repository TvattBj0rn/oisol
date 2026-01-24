import logging
from logging import LogRecord

from src.utils import OISOL_HOME_PATH


class OisolFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        colors = {
            'red': '\x1b[31;20m',
            'bold_red': '\x1b[31;1m',
            'green': '\x1b[32;1m',
            'yellow': '\x1b[33;20m',
            'blue': '\x1b[34;20m',
            'purple': '\x1b[35;20m',
            'cyan': '\x1b[36;20m',
            'grey': '\x1b[38;20m',
            'reset': '\x1b[0m',
        }
        log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
        self.FORMATS = {
            logging.DEBUG: f'{colors.get('grey')}{log_format}{colors.get('reset')}',
            logging.INFO: f'{colors.get('grey')}{log_format}{colors.get('reset')}',
            21: f'{colors.get('blue')}{log_format}{colors.get('reset')}',
            22: f'{colors.get('cyan')}{log_format}{colors.get('reset')}',
            23: f'{colors.get('purple')}{log_format}{colors.get('reset')}',
            24: f'{colors.get('green')}{log_format}{colors.get('reset')}',
            logging.WARNING: f'{colors.get('yellow')}{log_format}{colors.get('reset')}',
            logging.ERROR: f'{colors.get('red')}{log_format}{colors.get('reset')}',
            logging.CRITICAL: f'{colors.get('bold_red')}{log_format}{colors.get('reset')}',
        }

    def format(self, record: LogRecord) -> str:
        return logging.Formatter(self.FORMATS.get(record.levelno), datefmt='%Y-%m-%d %H:%M:%S').format(record)


class OisolLogger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)
        self.level = logging.DEBUG

        # The logs displayed on the console
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(OisolFormatter())
        self.addHandler(stream_handler)

        # The logs saved on a dedicated file (append mode)
        file_handler = logging.FileHandler(OISOL_HOME_PATH / 'oisol.log', mode='a')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(OisolFormatter())
        self.addHandler(file_handler)

        logging.addLevelName(21, 'COMMAND')
        logging.addLevelName(22, 'INTERFACE')
        logging.addLevelName(23, 'TASK')
        logging.addLevelName(24, 'JOIN')

    def command(self, msg: str, *args, **kwargs) -> None:
        self.log(21, msg, *args, **kwargs)

    def interface(self, msg: str, *args, **kwargs) -> None:
        self.log(22, msg, *args, **kwargs)

    def task(self, msg: str, *args, **kwargs) -> None:
        self.log(23, msg, *args, *kwargs)

    def join(self, msg: str, *args, **kwargs) -> None:
        self.log(24, msg, *args, *kwargs)
