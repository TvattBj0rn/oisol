from __future__ import annotations

import sqlite3
import uuid
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import OISOL_HOME_PATH, DiscordIdType, InterfaceType

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

        self.bot.logger.command(f'todolist-generate command by {interaction.user.name} on {interaction.guild.name}')
        todolist_id = uuid.uuid4().hex
        todolist_access_list = []
        await interaction.response.defer(ephemeral=True)

        # Create temporary placeholder
        msg = await interaction.channel.send(embed=discord.Embed().from_dict({'title': title}))

        if role_1:
            todolist_access_list.append((interaction.guild_id, str(msg.channel.id), str(msg.id), role_1.id, DiscordIdType.ROLE.name))
        if role_2:
            todolist_access_list.append((interaction.guild_id, str(msg.channel.id), str(msg.id), role_2.id, DiscordIdType.ROLE.name))
        if role_3:
            todolist_access_list.append((interaction.guild_id, str(msg.channel.id), str(msg.id), role_3.id, DiscordIdType.ROLE.name))
        if role_4:
            todolist_access_list.append((interaction.guild_id, str(msg.channel.id), str(msg.id), role_4.id, DiscordIdType.ROLE.name))
        if role_5:
            todolist_access_list.append((interaction.guild_id, str(msg.channel.id), str(msg.id), role_5.id, DiscordIdType.ROLE.name))
        if member_1:
            todolist_access_list.append((interaction.guild_id, str(msg.channel.id), str(msg.id), member_1.id, DiscordIdType.USER.name))
        if member_2:
            todolist_access_list.append((interaction.guild_id, str(msg.channel.id), str(msg.id), member_2.id, DiscordIdType.USER.name))
        if member_3:
            todolist_access_list.append((interaction.guild_id, str(msg.channel.id), str(msg.id), member_3.id, DiscordIdType.USER.name))
        if member_4:
            todolist_access_list.append((interaction.guild_id, str(msg.channel.id), str(msg.id), member_4.id, DiscordIdType.USER.name))
        if member_5:
            todolist_access_list.append((interaction.guild_id, str(msg.channel.id), str(msg.id), member_5.id, DiscordIdType.USER.name))

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            if todolist_access_list:
                cursor.executemany(
                    'INSERT INTO GroupsInterfacesAccess (GroupId, ChannelId, MessageId, DiscordId, DiscordIdType) VALUES (?, ?, ?, ?, ?)',
                    todolist_access_list,
                )
                conn.commit()

            todolist_view = TodolistViewMenu()
            todolist_view.refresh_view(title, msg, todolist_id)
            await msg.edit(view=todolist_view, embed=todolist_view.embed)

            cursor.execute(
                'INSERT INTO AllInterfacesReferences (GroupId, ChannelId, MessageId, InterfaceType, InterfaceReference, InterfaceName) VALUES (?, ?, ?, ?, ?, ?)',
                (interaction.guild_id, interaction.channel_id, msg.id, InterfaceType.TODOLIST_VIEW.name, todolist_id, title),
            )
            conn.commit()

        await interaction.followup.send('> The todolist was properly created', ephemeral=True)
