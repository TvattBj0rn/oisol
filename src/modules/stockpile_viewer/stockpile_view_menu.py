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
    DataFilesPath, InterfacesTypes,
)


class StockpilesViewMenu(discord.ui.View):
    """
    Main menu interface of the stockpiles module
    """
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='Stockpile:View', label='View Stockpiles', emoji='📥')
    async def display_stockpiles(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        pass

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='Stockpile:Share', label='Share ID', emoji='🔗')
    async def get_stockpile_association_id(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        if interaction.user.name != interaction.message.embeds[0].footer.text:
            await interaction.response.send_message('> Only the creator of the interface can do this action', ephemeral=True)
        else:
            with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
                association_id = conn.cursor().execute(
                    'SELECT AssociationId FROM AllInterfacesReferences WHERE GroupId == ? AND ChannelId == ? AND MessageId == ? AND InterfaceType == ?',
                    (interaction.guild_id, interaction.channel_id, interaction.message.id, InterfacesTypes.STOCKPILE.value),
                ).fetchone()
            await interaction.response.send_message(f'> The association id is: `{association_id[0]}`', ephemeral=True)
