from enum import Enum


class Languages(Enum):
    FR = 'french'
    EN = 'english'
    DE = 'german'
    ES = 'spanish'


## Color ?
class Faction(Enum):
    WARDEN = 'warden'
    COLONIAL = 'colonial'
    NEUTRAL = 'neutral'