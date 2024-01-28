import discord
import os
import pathlib
import uuid
from discord import app_commands
from discord.ext import commands
from modules.todolist.config import TODOLIST_CSV_KEYS
from modules.todolist.TodolistEnums import PriorityType
from modules.todolist.TodolistInterface import TodolistInterface
from modules.todolist.CsvHandlerTodolist import CsvHandlerTodolist


class ModuleTodolist(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.csv_keys = TODOLIST_CSV_KEYS
    
    @app_commands.command(name='todolist_generate')
    async def todolist_generate(self, interaction: discord.Interaction, title: str):
        embed_uuid = uuid.uuid4().hex
        todolist_embed = discord.Embed(title=f'☑️️ **|** {title}', description='Classée par ordre de priorité')
        todolist_embed.add_field(name='🔴 **|** Priorité Haute', value='')
        todolist_embed.add_field(name='🟡 **|** Priorité Moyenne', value='')
        todolist_embed.add_field(name='🟢 **|** Priorité Basse', value='')
        todolist_embed.set_footer(text=embed_uuid)

        CsvHandlerTodolist(self.csv_keys).csv_try_create_file(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), 'todolists', f'{embed_uuid}.csv')
        )

        await interaction.response.send_message(embed=todolist_embed)

    @app_commands.command(name='todolist_add')
    async def todolist_add(self, interaction: discord.Interaction, embed_uuid: str, content: str, priority: PriorityType):
        await interaction.response.defer(ephemeral=True)
        for task in content.split(sep=','):
            task_dict = {
                'content': task,
                'priority': priority.value
            }
            CsvHandlerTodolist(self.csv_keys).csv_append_data(
                os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), 'todolists', f'{embed_uuid}.csv'),
                task_dict
            )

        # Find todolist message
        async for message in interaction.channel.history():
            if message.embeds:
                message_embed = discord.Embed.to_dict(message.embeds[0])
                if 'footer' in message_embed.keys() and message_embed['footer']['text'] == embed_uuid:
                    todolist_view = TodolistInterface(message, message_embed, self.csv_keys, embed_uuid, str(interaction.guild.id))
                    self.oisol.add_view(todolist_view)
                    await message.edit(view=todolist_view, embed=todolist_view.generateInterfaceEmbed())
                    await interaction.followup.send('> La todolist a été mise à jour')
                    return
        await interaction.followup.send('> Ce salon ne contient pas la todolist demandée')
