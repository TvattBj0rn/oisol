import configparser
import re
import sqlite3
import string
import time
from typing import Self

import discord

from src.utils import (
    EMOTES_CUSTOM_ID,
    OISOL_HOME_PATH,
    OisolLogger,
    PriorityType,
    DataFilesPath,
)


class StockpilesViewMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='Stockpile:View', label='View Stockpiles', emoji='📥')
    async def display_stockpiles(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        pass

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='Stockpile:Share', label='Share ID', emoji='🔗')
    async def get_stockpile_association_id(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        pass


