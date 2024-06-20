import discord
import os
import pathlib
import uuid
import json
from discord import app_commands
from discord.ext import commands
from src.modules.todolist.TodolistInterface import TodolistInterface
from src.utils.CsvHandler import CsvHandler
from src.utils.oisol_enums import PriorityType, Modules
from src.utils.resources import MODULES_CSV_KEYS


class ModuleTodolist(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.csv_keys = MODULES_CSV_KEYS['todolist']
    
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
        todolist_embed = discord.Embed(title=f'☑️️ **|** {title}', description='Classée par ordre de priorité')
        todolist_embed.add_field(name='🔴 **|** Priorité Haute', value='')
        todolist_embed.add_field(name='🟡 **|** Priorité Moyenne', value='')
        todolist_embed.add_field(name='🟢 **|** Priorité Basse', value='')
        todolist_embed.set_footer(text=embed_uuid)

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

        CsvHandler(self.csv_keys).csv_try_create_file(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), 'todolists', f'{embed_uuid}.csv')
        )

        with open(
                os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), 'todolists', f'{embed_uuid}.json'),
                'w'
        ) as file:
            json.dump(permissions, file)

        await interaction.response.send_message(embed=todolist_embed)

    @app_commands.command(name='todolist_add')
    async def todolist_add(self, interaction: discord.Interaction, embed_uuid: str, content: str, priority: PriorityType):
        print(f'> todolist_add command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.defer(ephemeral=True)
        for task in content.split(sep=','):
            task_dict = {
                'content': task,
                'priority': priority.value
            }
            CsvHandler(self.csv_keys).csv_append_data(
                os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), 'todolists', f'{embed_uuid}.csv'),
                task_dict,
                Modules.TODOLIST
            )

        # Find todolist message
        async for message in interaction.channel.history():
            if message.embeds:
                message_embed = discord.Embed.to_dict(message.embeds[0])
                if 'footer' in message_embed.keys() and message_embed['footer']['text'] == embed_uuid:
                    todolist_view = TodolistInterface().refresh_interface(message_embed, embed_uuid, str(interaction.guild.id))
                    await message.edit(view=todolist_view, embed=todolist_view.generate_interface_embed())
                    await interaction.followup.send('> La todolist a été mise à jour')
                    return
        await interaction.followup.send('> Ce salon ne contient pas la todolist demandée')
