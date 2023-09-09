import uuid
import discord
from discord import app_commands
from discord.ext import commands
from modules.todolist.TodolistEnums import PriorityType
from modules.todolist.TodolistInterface import TodolistInterface
from modules.todolist.CsvHandlerTodolist import CsvHandlerTodolist
from modules.utils.path import generate_path



class ModuleTodolist(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.csv_keys = ['content', 'priority']
    
    @app_commands.command(name='todolist_generate')
    async def todolist_generate(self, interaction: discord.Interaction, title: str):
        embed_uuid = uuid.uuid4().hex
        todolist_embed = discord.Embed(title=f'☑️️ **|** {title}', description='Classée par ordre de priorité')
        todolist_embed.add_field(name='🔴 **|** Priorité Haute', value='')
        todolist_embed.add_field(name='🟡 **|** Priorité Moyenne', value='')
        todolist_embed.add_field(name='🟢 **|** Priorité Basse', value='')
        todolist_embed.set_footer(text=embed_uuid)

        CsvHandlerTodolist(self.csv_keys).csv_try_create_file(generate_path(interaction.guild.id, f'todolists/{embed_uuid}.csv'))

        await interaction.response.send_message(embed=todolist_embed)
    
    
    @app_commands.command(name='todolist_add')
    async def todolist_add(self, interaction: discord.Interaction, embed_uuid: str, content: str, priority: PriorityType):
        task_dict = {
            'content': content,
            'priority': priority.value
        }

        CsvHandlerTodolist(self.csv_keys).csv_append_data(generate_path(interaction.guild.id, f'todolists/{embed_uuid}.csv'), task_dict)
        async for message in interaction.channel.history():
            if message.embeds:
                message_embed = discord.Embed.to_dict(message.embeds[0])
                if 'footer' in message_embed.keys() and message_embed['footer']['text'] == embed_uuid:
                    todolist_view = TodolistInterface(message, message_embed, self.csv_keys, embed_uuid)
                    await message.edit(view=todolist_view, embed=todolist_view.generateInterfaceEmbed())
                    await interaction.response.send_message('> La todolist a été mise à jour', ephemeral=True)
                    return
        await interaction.response.send_message('> Ce channel ne contient pas la todolist demandée', ephemeral=True)
