import logging



class OisolFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()
        _colors = {
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
        _log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
        self.FORMATS = {
            logging.DEBUG: f'{_colors.get('grey')}{_log_format}{_colors.get('reset')}',
            logging.INFO: f'{_colors.get('grey')}{_log_format}{_colors.get('reset')}',
            21: f'{_colors.get('blue')}{_log_format}{_colors.get('reset')}',
            22: f'{_colors.get('cyan')}{_log_format}{_colors.get('reset')}',
            23: f'{_colors.get('purple')}{_log_format}{_colors.get('reset')}',
            24: f'{_colors.get('green')}{_log_format}{_colors.get('reset')}',
            logging.WARNING: f'{_colors.get('yellow')}{_log_format}{_colors.get('reset')}',
            logging.ERROR: f'{_colors.get('red')}{_log_format}{_colors.get('reset')}',
            logging.CRITICAL: f'{_colors.get('bold_red')}{_log_format}{_colors.get('reset')}',
        }

    def format(self, record):
        return logging.Formatter(self.FORMATS.get(record.levelno), datefmt='%Y-%m-%d %H:%M:%S').format(record)


class OisolLogger(logging.Logger):
    def __init__(self, name: str):
        super().__init__(name)
        self.level = logging.DEBUG
        _stream_handler = logging.StreamHandler()
        _stream_handler.setFormatter(OisolFormatter())
        self.addHandler(_stream_handler)
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
