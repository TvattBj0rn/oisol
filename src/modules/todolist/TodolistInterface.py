import json
import discord
import os
import pathlib
from typing_extensions import Self, Tuple
from src.utils.CsvHandler import CsvHandler
from src.utils.oisol_enums import PriorityType, Modules
from src.utils.resources import EMOTES_CUSTOM_ID, MODULES_CSV_KEYS


def has_permissions(interaction: discord.Interaction, permissions: dict) -> bool:
    if not permissions['members'] and not permissions['roles']:
        return True
    if interaction.user.id in permissions['members']:
        return True
    for role_perm in permissions['roles']:
        if role_perm in [role.id for role in interaction.user.roles]:
            return True
    return False


def list_to_priority_dict(data_list: list) -> dict:
    data_dict = {
        'high': [],
        'medium': [],
        'low': []
    }
    for task in data_list:
        data_dict[task[1]].append(task[0])
    return data_dict


def refit_data(data_dict: dict) -> Tuple[dict, list]:
    total_len = len(data_dict['high']) + len(data_dict['medium']) + len(data_dict['low'])
    if total_len < 24:
        return data_dict, list()
    all_tasks = data_dict['high'] + data_dict['medium'] + data_dict['low']
    all_tasks_list_refitted, overflowing_tasks = all_tasks[:24], [x['content'] for x in all_tasks[24:len(all_tasks)]]
    updated_dict = {'high': [], 'medium': [], 'low': []}
    for task in all_tasks_list_refitted:
        updated_dict[task['priority']].append(task)
    return updated_dict, overflowing_tasks


class TodolistInterface(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.csv_keys = MODULES_CSV_KEYS['todolist']
        self.interface_embed = None
        self.message_embed = dict()
        self.data_dict = dict()
        self.embed_uuid = ''
        self.guild_id = ''
        self.data_list = []
        self.buttons_list = []

    def refresh_interface(self, message_embed: dict, embed_uuid: str, guild_id: str, updated_data: dict = None) -> Self:
        self.message_embed = message_embed
        self.embed_uuid = embed_uuid
        self.guild_id = guild_id
        self.data_list = []
        if updated_data:
            self.data_dict, _ = refit_data(updated_data)
        else:
            self.data_dict = CsvHandler(self.csv_keys).csv_get_all_data(
                os.path.join(pathlib.Path('/'), 'oisol', self.guild_id, 'todolists', f'{self.embed_uuid}.csv'), Modules.TODOLIST
            )
        for key in self.data_dict.keys():
            for elem in self.data_dict[key]:
                self.data_list.append([elem, key])
        self.buttons_list = [TodolistButtonCheckmark(self, emote, EMOTES_CUSTOM_ID[emote]) for emote in '🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿']

        self.clear_items()
        self.interface_embed = self.generate_interface_embed()
        self.add_item(TodolistButtonAdd(embed_uuid, self))
        for index in range(len(self.data_list)):
            try:
                self.add_item(self.buttons_list[index])
            except ValueError:
                break
        return self

    def generate_interface_embed(self) -> discord.Embed:
        generated_embed = discord.Embed(title=self.message_embed['title'])
        alphabet_list = [x for x in 'abcdefghijklmnopqrstuvwxyz']
        global_index = 0
        high_priority = ''
        medium_priority = ''
        low_priority = ''

        for order in self.data_dict[PriorityType.HAUTE.value]:
            if global_index == 24:
                break
            high_priority += f':regional_indicator_{alphabet_list[global_index]}: **|** {order}\n'
            global_index += 1

        for order in self.data_dict[PriorityType.MOYENNE.value]:
            if global_index == 24:
                break
            medium_priority += f':regional_indicator_{alphabet_list[global_index]}: **|** {order}\n'
            global_index += 1

        for order in self.data_dict[PriorityType.BASSE.value]:
            if global_index == 24:
                break
            low_priority += f':regional_indicator_{alphabet_list[global_index]}: **|** {order}\n'
            global_index += 1

        generated_embed.set_footer(text=self.message_embed['footer']['text'])
        generated_embed.add_field(
            name='🔴 **|** Priorité Haute',
            value=high_priority
        )
        generated_embed.add_field(
            name='🟡 **|** Priorité Moyenne',
            value=medium_priority
        )
        generated_embed.add_field(
            name='🟢 **|** Priorité Basse',
            value=low_priority
        )
        return generated_embed


class TodolistModalAdd(discord.ui.Modal, title='Todolist Add'):
    def __init__(self, embed_uuid: str, view: TodolistInterface):
        super().__init__()
        self.embed_uuid = embed_uuid
        self.todolist_view = view

    high_priority = discord.ui.TextInput(
        label='🔴 | Priorité Haute',
        style=discord.TextStyle.long,
        required=False
    )
    medium_priority = discord.ui.TextInput(
        label='🟡 | Priorité Moyenne',
        style=discord.TextStyle.long,
        required=False
    )
    low_priority = discord.ui.TextInput(
        label='🟢 | Priorité Basse',
        style=discord.TextStyle.long,
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        csv_handler = CsvHandler(MODULES_CSV_KEYS['todolist'])
        data_dict = {PriorityType.HAUTE.value: [], PriorityType.MOYENNE.value: [], PriorityType.BASSE.value: []}
        for task in self.high_priority.value.split(','):
            if task:
                csv_handler.csv_append_data(
                    os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), 'todolists', f'{self.embed_uuid}.csv'),
                    {'content': task, 'priority': PriorityType.HAUTE.value},
                    Modules.TODOLIST
                )
                data_dict[PriorityType.HAUTE.value].append({'content': task, 'priority': PriorityType.HAUTE.value})

        for task in self.medium_priority.value.split(','):
            if task:
                csv_handler.csv_append_data(
                    os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), 'todolists',
                                 f'{self.embed_uuid}.csv'),
                    {'content': task, 'priority': PriorityType.MOYENNE.value},
                    Modules.TODOLIST
                )
                data_dict[PriorityType.MOYENNE.value].append({'content': task, 'priority': PriorityType.MOYENNE.value})

        for task in self.low_priority.value.split(','):
            if task:
                csv_handler.csv_append_data(
                    os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), 'todolists',
                                 f'{self.embed_uuid}.csv'),
                    {'content': task, 'priority': PriorityType.BASSE.value},
                    Modules.TODOLIST
                )
                data_dict[PriorityType.BASSE.value].append({'content': task, 'priority': PriorityType.BASSE.value})
        self.todolist_view.data_dict, bypassed_tasks = refit_data(data_dict)
        await interaction.followup.send(f"> Tasks that were not put in the todolist: {','.join([x for x in bypassed_tasks])}")

        # Find todolist message
        async for message in interaction.channel.history():
            if message.embeds:
                message_embed = discord.Embed.to_dict(message.embeds[0])
                if 'footer' in message_embed.keys() and message_embed['footer']['text'] == self.embed_uuid:
                    self.todolist_view.refresh_interface(message_embed, self.embed_uuid, str(interaction.guild.id))
                    await message.edit(view=self.todolist_view, embed=self.todolist_view.generate_interface_embed())
                    await interaction.followup.send('> La todolist a été mise à jour', ephemeral=True)
                    return
        await interaction.followup.send('> Error car ça a fini la boucle')


class TodolistButtonAdd(discord.ui.Button):
    def __init__(self, embed_uuid: str, view: TodolistInterface):
        super().__init__()
        self.emoji = '➕'
        self.style = discord.ButtonStyle.green
        self.embed_uuid = embed_uuid
        self.todolist_view = view

    async def callback(self, interaction: discord.Interaction):
        try:
            with open(
                    os.path.join(pathlib.Path('/'), 'oisol', self.todolist_view.guild_id, 'todolists', f'{self.embed_uuid}.json'),
                    'r'
            ) as file:
                permissions: dict = json.load(file)
        except OSError:
            print(f'Error opening todolist file on {interaction.guild.name} for {self.embed_uuid}')
        if 'roles' in permissions.keys() and 'members' in permissions.keys() and not has_permissions(interaction, permissions):
            await interaction.response.send_message('Forbidden', ephemeral=True)
            return
        await interaction.response.send_modal(TodolistModalAdd(self.embed_uuid, self.todolist_view))


class TodolistButtonCheckmark(discord.ui.Button):
    def __init__(self, todolist_interface: TodolistInterface, emote: str, custom_id: str):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = emote
        self.style = discord.ButtonStyle.blurple
        self.guild_id = todolist_interface.guild_id
        self.embed_uuid = todolist_interface.embed_uuid
        self.original_embed = todolist_interface.message_embed
        self.data_list = todolist_interface.data_list
        self.custom_id = custom_id

    async def callback(self, interaction: discord.Interaction):
        try:
            with open(
                    os.path.join(pathlib.Path('/'), 'oisol', self.guild_id, 'todolists', f'{self.embed_uuid}.json'),
                    'r'
            ) as file:
                permissions: dict = json.load(file)
        except OSError:
            print(f'Error opening todolist file on {interaction.guild.name} for {self.embed_uuid}')
        if 'roles' in permissions.keys() and 'members' in permissions.keys() and not has_permissions(interaction, permissions):
            await interaction.response.send_message('Forbidden', ephemeral=True)
            return

        self.data_list.pop(list(EMOTES_CUSTOM_ID.keys()).index(str(self.emoji)))
        data_dict = list_to_priority_dict(self.data_list)
        CsvHandler(self.todolist_interface.csv_keys).csv_rewrite_file(
            os.path.join(pathlib.Path('/'), 'oisol', self.guild_id, 'todolists', f'{self.embed_uuid}.csv'),
            self.data_list,
            Modules.TODOLIST
        )
        self.todolist_interface.refresh_interface(self.original_embed, self.embed_uuid, self.guild_id, data_dict)
        await interaction.message.edit(view=self.todolist_interface, embed=self.todolist_interface.generate_interface_embed())
        await interaction.response.defer()
