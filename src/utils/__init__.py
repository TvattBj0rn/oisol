from .functions import *
from .oisol_enums import *
from .resources import *
from .foxhole_api_handler import FoxholeAsyncAPIWrapper
from .oisol_logger import OisolLogger, OisolFormatter

# Ensure Home folder is properly created
Path(OISOL_HOME_PATH).mkdir(parents=True, exist_ok=True)
OISOL_LOGGER = OisolLogger()
