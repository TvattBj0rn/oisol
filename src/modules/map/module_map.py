from typing import TYPE_CHECKING

from discord.ext import commands

if TYPE_CHECKING:
    from main import Oisol


class ModuleNotifications(commands.Cog):
    """
    The idea of this module is to set an interface 
    """
    def __init__(self, bot: Oisol):
        self.bot = bot
