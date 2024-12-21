import logging
import uuid

import discord
from discord import app_commands
from discord.ext import commands

from .TodolistViewMenu import TodolistViewMenu


class ModuleTodolist(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot

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
        permissions = {
            'roles': [],
            'members': []
        }
        if role_1:
            permissions['roles'].append(role_1.id)
        if role_2:
            permissions['roles'].append(role_2.id)
        if role_3:
            permissions['roles'].append(role_3.id)
        if role_4:
            permissions['roles'].append(role_4.id)
        if role_5:
            permissions['roles'].append(role_5.id)
        if member_1:
            permissions['members'].append(member_1.id)
        if member_2:
            permissions['members'].append(member_2.id)
        if member_3:
            permissions['members'].append(member_3.id)
        if member_4:
            permissions['members'].append(member_4.id)
        if member_5:
            permissions['members'].append(member_5.id)

        todolist_view = TodolistViewMenu()
        todolist_view.refresh_view(
            {'title': title, 'access': permissions, 'tasks': {'high': [], 'medium': [], 'low': []}},
            title,
            str(interaction.guild_id),
            uuid.uuid4().hex
        )

        await interaction.response.send_message(view=todolist_view, embed=todolist_view.embed)
