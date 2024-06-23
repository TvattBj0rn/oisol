import discord
import os
import pathlib
import uuid
from discord import app_commands
from discord.ext import commands
from src.utils.functions import update_json_file
from src.modules.todolist.TodolistViewMenu import TodolistViewMenu


class ModuleTodolist(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot

    @app_commands.command(name='todolist_generate')
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

    ):
        print(f'> todolist_generate command by {interaction.user.name} on {interaction.guild.name}')
        embed_uuid = uuid.uuid4().hex
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

        update_json_file(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild_id), 'todolists', f'{embed_uuid}.json'),
            {'access': permissions, 'tasks': {'high': [], 'medium': [], 'low': []}}
        )

        todolist_embed = discord.Embed(title=f'☑️️ **|** {title}')
        todolist_embed.add_field(name='🔴 **|** Priorité Haute', value='')
        todolist_embed.add_field(name='🟡 **|** Priorité Moyenne', value='')
        todolist_embed.add_field(name='🟢 **|** Priorité Basse', value='')
        todolist_embed.set_footer(text=embed_uuid)

        todolist_view = TodolistViewMenu(
            todolist_embed=todolist_embed,
            guild_id=str(interaction.guild_id),
            access=permissions
        )

        await interaction.response.send_message(view=todolist_view, embed=todolist_view.embed)
