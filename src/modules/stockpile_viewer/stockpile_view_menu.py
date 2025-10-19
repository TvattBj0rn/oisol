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
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='Stockpile:View', label='View Stockpiles', emoji='📥')
    async def display_stockpiles(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        pass

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='Stockpile:Permissions', label='Configure Permissions', emoji='🔑')
    async def edit_interface_permissions(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        pass

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='Stockpile:Share', label='Share ID', emoji='🔗')
    async def get_stockpile_association_id(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        if interaction.user.name != interaction.message.interaction_metadata.user.name:
            await interaction.response.send_message('> Only the creator of the interface can do this action', ephemeral=True)
        else:
            with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
                potential_association_id_as_list = conn.cursor().execute(
                    'SELECT AssociationId FROM AllInterfacesReferences WHERE GroupId == ? AND ChannelId == ? AND MessageId == ? AND InterfaceType IN (?, ?)',
                    (interaction.guild_id, interaction.channel_id, interaction.message.id, InterfacesTypes.STOCKPILE.value, InterfacesTypes.MULTISERVER_STOCKPILE.value),
                ).fetchall()
            await interaction.response.send_message('> The association id is: ``', ephemeral=True)
