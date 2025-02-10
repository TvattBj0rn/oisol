from __future__ import annotations

import logging
import uuid
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import DiscordIdType, InterfaceType

from .todolist_view_menu import TodolistViewMenu

if TYPE_CHECKING:
    from main import Oisol


class ModuleTodolist(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot

    @app_commands.command(name='todolist-generate')
    async def todolist_generate(
            self,
            interaction: discord.Interaction,
            title: str,
            role_1: discord.Role = None,
            role_2: discord.Role = None,
            role_3: discord.Role = None,
            role_4: discord.Role = None,
            role_5: discord.Role = None,
            member_1: discord.Member = None,
            member_2: discord.Member = None,
            member_3: discord.Member = None,
            member_4: discord.Member = None,
            member_5: discord.Member = None,
    ) -> None:

        logging.info(f'[COMMAND] todolist-generate command by {interaction.user.name} on {interaction.guild.name}')
        todolist_id = uuid.uuid4().hex
        todolist_access_list = []

        if role_1:
            todolist_access_list.append((interaction.guild_id, todolist_id, role_1.id, DiscordIdType.ROLE.name))
        if role_2:
            todolist_access_list.append((interaction.guild_id, todolist_id, role_2.id, DiscordIdType.ROLE.name))
        if role_3:
            todolist_access_list.append((interaction.guild_id, todolist_id, role_3.id, DiscordIdType.ROLE.name))
        if role_4:
            todolist_access_list.append((interaction.guild_id, todolist_id, role_4.id, DiscordIdType.ROLE.name))
        if role_5:
            todolist_access_list.append((interaction.guild_id, todolist_id, role_5.id, DiscordIdType.ROLE.name))
        if member_1:
            todolist_access_list.append((interaction.guild_id, todolist_id, member_1.id, DiscordIdType.USER.name))
        if member_2:
            todolist_access_list.append((interaction.guild_id, todolist_id, member_2.id, DiscordIdType.USER.name))
        if member_3:
            todolist_access_list.append((interaction.guild_id, todolist_id, member_3.id, DiscordIdType.USER.name))
        if member_4:
            todolist_access_list.append((interaction.guild_id, todolist_id, member_4.id, DiscordIdType.USER.name))
        if member_5:
            todolist_access_list.append((interaction.guild_id, todolist_id, member_5.id, DiscordIdType.USER.name))

        if todolist_access_list:
            self.bot.cursor.executemany(
                'INSERT INTO GroupsTodolistsAccess (GroupId, TodolistId, DiscordId, DiscordIdType) VALUES (?, ?, ?, ?)',
                todolist_access_list,
            )
            self.bot.connection.commit()

        todolist_view = TodolistViewMenu()
        todolist_view.refresh_view(title, str(interaction.guild_id), todolist_id)

        await interaction.response.send_message(view=todolist_view, embed=todolist_view.embed)
        interaction_response_message = await interaction.original_response()
        self.bot.cursor.execute(
            f'INSERT INTO AllInterfacesReferences (ChannelId, MessageId, InterfaceType, InterfaceReference) VALUES (?, ?, ?, ?)',
            (interaction.channel_id, interaction_response_message.id, InterfaceType.TODOLIST_VIEW.name, todolist_id)
        )
        self.bot.connection.commit()
