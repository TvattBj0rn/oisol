import os

from dotenv import load_dotenv

from .functions import *
from .oisol_enums import *
from .resources import *
from .foxhole_api_handler import FoxholeAPIWrapper
from .oisol_logger import OisolLogger, OisolFormatter
from .oisol_encryption_system import AesGcm

load_dotenv()
if os.getenv('BOISOL') is not None:
    OISOL_HOME_PATH = pathlib.Path('/') / 'boisol'