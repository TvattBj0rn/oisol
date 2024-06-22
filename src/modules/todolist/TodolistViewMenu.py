import json
import discord
import os
from more_itertools.recipes import consume
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
    for test_case in [data_dict['high'], data_dict['medium'], data_dict['low']]:
        if len(test_case) and isinstance(test_case[0], str):
            data_dict = {
                'high': [{'content': task, 'priority': 'high'} for task in data_dict['high']],
                'medium': [{'content': task, 'priority': 'medium'} for task in data_dict['medium']],
                'low': [{'content': task, 'priority': 'low'} for task in data_dict['low']]
            }
            break

    total_len = len(data_dict['high']) + len(data_dict['medium']) + len(data_dict['low'])
    if total_len < 24:
        return data_dict, list()
    all_tasks = data_dict['high'] + data_dict['medium'] + data_dict['low']
    all_tasks_list_refitted, overflowing_tasks = all_tasks[:24], [x['content'] for x in all_tasks[24:len(all_tasks)]]
    updated_dict = {'high': [], 'medium': [], 'low': []}
    for task in all_tasks_list_refitted:
        updated_dict[task['priority']].append(task)
    return updated_dict, overflowing_tasks


class TodolistViewMenu(discord.ui.View):
    def __init__(
            self,
            message_embed: dict = None,
            updated_data: dict = None,
            embed_uuid: str = None,
            guild_id: str = None
    ):
        super().__init__(timeout=None)
        self.csv_keys = MODULES_CSV_KEYS['todolist']
        self.interface_embed = None
        self.message_embed = message_embed if message_embed else {}
        self.data_dict = updated_data if updated_data else {}
        self.embed_uuid = embed_uuid if embed_uuid else ''
        self.guild_id = guild_id if guild_id else ''
        self.data_list = []
        self.buttons_list = []

    def refresh_interface(self, updated_data: dict = None) -> Self:
        self.data_list = []
        data_dict, _ = refit_data(
            updated_data if updated_data else CsvHandler(self.csv_keys).csv_get_all_data(
                os.path.join(pathlib.Path('/'), 'oisol', self.guild_id, 'todolists', f'{self.embed_uuid}.csv'),
                Modules.TODOLIST
            )
        )
        self.data_dict = {
                'high': [task['content'] for task in data_dict['high']],
                'medium': [task['content'] for task in data_dict['medium']],
                'low': [task['content'] for task in data_dict['low']]
            }

        # Clear all task buttons
        consume(self.remove_item(x) for x in self.buttons_list)

        for key in self.data_dict.keys():
            for elem in self.data_dict[key]:
                self.data_list.append([elem, key])

        self.buttons_list = [TodolistButtonCheckmark(self, emote, EMOTES_CUSTOM_ID[emote]) for emote in '🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿']
        self.interface_embed = self.generate_interface_embed()
        for index in range(len(self.data_list)):
            try:
                self.add_item(self.buttons_list[index])
            except ValueError:
                break
        return self

    def generate_interface_embed(self) -> discord.Embed:
        generated_embed = discord.Embed(title=self.message_embed['title'])
        priority_tasks_dict, _ = refit_data(self.data_dict)

        enumerated_tasks = {'high': '', 'medium': '', 'low': ''}
        for i, task in enumerate((priority_tasks_dict['high'] + priority_tasks_dict['medium'] + priority_tasks_dict['low'])[:24]):
            enumerated_tasks[task['priority']] += f":regional_indicator_{'abcdefghijklmnopqrstuvwxyz'[i]}: **|** {task['content']}\n"

        generated_embed.set_footer(text=self.message_embed['footer']['text'])
        for priority, tasks in [
            ('🔴 **|** Priorité Haute', enumerated_tasks['high']),
            ('🟡 **|** Priorité Moyenne', enumerated_tasks['medium']),
            ('🟢 **|** Priorité Basse', enumerated_tasks['low'])
        ]:
            generated_embed.add_field(
                name=priority,
                value=tasks
            )

        return generated_embed

    @discord.ui.button(style=discord.ButtonStyle.green, custom_id='Todolist:Add', emoji='➕')
    async def add_tasks(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            with open(
                    os.path.join(pathlib.Path('/'), 'oisol', self.guild_id, 'todolists', f'{self.embed_uuid}.json'),
                    'r'
            ) as file:
                permissions: dict = json.load(file)
        except OSError:
            print(f'Error opening todolist file on {interaction.guild.name} for {self.embed_uuid}')
        if 'roles' in permissions.keys() and 'members' in permissions.keys() and not has_permissions(interaction, permissions):
            await interaction.response.send_message('> Forbidden', ephemeral=True)
            return
        await interaction.response.send_modal(TodolistModalAdd(self.embed_uuid, self))


class TodolistModalAdd(discord.ui.Modal, title='Todolist Add'):
    def __init__(self, embed_uuid: str, view: TodolistViewMenu):
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
        if bypassed_tasks:
            await interaction.followup.send(f"> Tasks that were not put in the todolist: `{','.join([x for x in bypassed_tasks])}`", ephemeral=True)

        # Find todolist message
        async for message in interaction.channel.history():
            if message.embeds:
                message_embed = discord.Embed.to_dict(message.embeds[0])
                if 'footer' in message_embed.keys() and message_embed['footer']['text'] == self.embed_uuid:
                    self.todolist_view.refresh_interface()
                    await message.edit(view=self.todolist_view, embed=self.todolist_view.generate_interface_embed())
                    await interaction.followup.send('> La todolist a été mise à jour', ephemeral=True)
                    return
        await interaction.followup.send('> Error car ça a fini la boucle')


class TodolistButtonCheckmark(discord.ui.Button):
    def __init__(self, todolist_interface: TodolistViewMenu, emote: str, custom_id: str):
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
        self.todolist_interface.refresh_interface(data_dict)
        await interaction.message.edit(view=self.todolist_interface, embed=self.todolist_interface.generate_interface_embed())
        await interaction.response.defer()
