import copy
import discord
import json
import os
import pathlib
import re
from more_itertools.recipes import consume
from src.utils.oisol_enums import PriorityType
from src.utils.resources import EMOTES_CUSTOM_ID


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


def priority_dict_to_list(data_dict: dict) -> list:
    tasks_list = []
    for k, v in data_dict.items():
        for task in v:
            tasks_list.append([task, k])
    return tasks_list


def refit_data(data_dict: dict) -> tuple[dict, list]:
    """
    Refit existing data to conform with the discord API requirements.
    :param data_dict: data to refit.
    :return: tuple of the refitted data and the overflowing tasks.
    """
    data_dict_tasks = data_dict['tasks']
    removed_tasks = []
    tasks_to_remove = len(data_dict_tasks['high']) + len(data_dict_tasks['medium']) + len(data_dict_tasks['low']) - 24
    if tasks_to_remove <= 0:
        return data_dict, list()
    for k in ['low', 'medium', 'high']:
        if not data_dict_tasks[k]:
            continue
        if tasks_to_remove <= 0:
            break
        buf = len(data_dict_tasks[k][-tasks_to_remove:])
        removed_tasks += data_dict_tasks[k][-tasks_to_remove:]
        data_dict_tasks[k] = data_dict_tasks[k][:-tasks_to_remove]
        tasks_to_remove -= buf

    data_dict['tasks'] = data_dict_tasks
    return data_dict, removed_tasks


class TodolistViewMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.data_dict = {}
        self.data_list = []
        self.buttons_list = []
        self.embed_uuid = ''
        self.guild_id = ''
        self.title = ''
        self.embed = None

    def refresh_view(
            self,
            updated_data: dict,
            todolist_title: str,
            guild_id: str,
            embed_uuid: str
    ):
        self.data_dict, _ = refit_data(updated_data)
        # The ternary is temporary to prevent regression on existing interfaces
        self.title = self.data_dict['title'] if 'title' in self.data_dict.keys() else todolist_title
        self.guild_id = guild_id
        self.embed_uuid = embed_uuid
        self.data_list = []

        with open(os.path.join(pathlib.Path('/'), 'oisol', self.guild_id, 'todolists', f'{self.embed_uuid}.json'), 'w') as file:
            json.dump(self.data_dict, file)

        for k in self.data_dict['tasks'].keys():
            for elem in self.data_dict['tasks'][k]:
                self.data_list.append([elem, k])

        # Clear all task buttons
        consume(self.remove_item(button) for button in self.buttons_list)

        self.buttons_list = [TodolistButtonCheckmark(f'todolist:button:{emote}') for emote in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
        self._refresh_view_embed()
        data_list = self.data_dict['tasks']['high'] + self.data_dict['tasks']['medium'] + self.data_dict['tasks']['low']
        for i in range(len(data_list)):
            self.add_item(self.buttons_list[i])

    def _refresh_view_embed(self):
        # Retrieval of existing tasks and deepcopy for display purposes
        current_tasks = refit_data(self.data_dict)[0]['tasks']
        display_tasks = copy.deepcopy(current_tasks)

        # k is priority, v tasks list of k and i regional_indicator to use (unique)
        i = 0
        for k, v in display_tasks.items():
            display_tasks[k] = ''
            for task in v:
                display_tasks[k] += f":regional_indicator_{'abcdefghijklmnopqrstuvwxyz'[i]}: **|** {task}\n"
                i += 1

        # Update with a single call from dict instead of multiple through the method
        self.embed = discord.Embed().from_dict(
            {
                'title': f'☑️️ **|** {self.title}',
                'footer': {'text': self.embed_uuid},
                'fields': [
                    {'name': '🔴 **|** High Priority', 'inline': True, 'value': display_tasks['high']},
                    {'name': '🟡 **|** Medium Priority', 'inline': True, 'value': display_tasks['medium']},
                    {'name': '🟢 **|** Low Priority', 'inline': True, 'value': display_tasks['low']}
                ]
            }
        )

    @discord.ui.button(style=discord.ButtonStyle.green, custom_id='Todolist:Add', emoji='➕')
    async def add_tasks(self, interaction: discord.Interaction, _button: discord.ui.Button):
        self.embed_uuid = interaction.message.embeds[0].footer.text
        try:
            with open(os.path.join(pathlib.Path('/'), 'oisol',str(interaction.guild_id), 'todolists', f'{self.embed_uuid}.json'), 'r') as file:
                permissions = json.load(file)['access']
        except OSError:
            await interaction.response.send_message('> Unexpected Error (`TodolistViewMenu.add_tasks`)', ephemeral=True)
            return
        if (
                'roles' in permissions.keys() and 'members' in permissions.keys()
                and not has_permissions(interaction, permissions)
        ):
            await interaction.response.send_message('> You do not have the permission to click on this button', ephemeral=True)
            return
        await interaction.response.send_modal(
            TodolistModalAdd(self.embed_uuid, self.title)
        )


class TodolistModalAdd(discord.ui.Modal, title='Todolist Add'):
    def __init__(self, embed_uuid: str, title: str):
        super().__init__()
        self.embed_uuid = embed_uuid
        self.todolist_title = title

    high_priority = discord.ui.TextInput(
        label='🔴 | High Priority',
        style=discord.TextStyle.long,
        required=False,
        placeholder='Use `,` for more than one item ...'
    )
    medium_priority = discord.ui.TextInput(
        label='🟡 | Medium Priority',
        style=discord.TextStyle.long,
        required=False,
        placeholder='Use `,` for more than one item ...'
    )
    low_priority = discord.ui.TextInput(
        label='🟢 | Low Priority',
        style=discord.TextStyle.long,
        required=False,
        placeholder='Use `,` for more than one item ...'
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        with open(os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild_id), 'todolists', f'{self.embed_uuid}.json'), 'r') as file:
            full_dict = json.load(file)
        data_dict = full_dict['tasks']
        if len(data_dict['high']) + len(data_dict['medium']) + len(data_dict['low']) >= 24:
            await interaction.followup.send('> The todolist is already full', ephemeral=True)
            return

        for priority, input_field in [
            (PriorityType.HIGH.value, self.high_priority),
            (PriorityType.MEDIUM.value, self.medium_priority),
            (PriorityType.LOW.value, self.low_priority)
        ]:
            for task in input_field.value.split(','):
                if task:
                    data_dict[priority].append(task)

        data_dict, bypassed_tasks = refit_data(
            {'title': self.todolist_title, 'access': full_dict['access'], 'tasks': data_dict}
        )
        if bypassed_tasks:
            await interaction.followup.send(
                f"> Tasks that were not put in the todolist: `{','.join([x for x in bypassed_tasks])}`",
                ephemeral=True
            )

        updated_todolist_view = TodolistViewMenu()
        updated_todolist_view.refresh_view(data_dict, self.todolist_title, str(interaction.guild_id), self.embed_uuid)
        await interaction.message.edit(view=updated_todolist_view, embed=updated_todolist_view.embed)


class TodolistButtonCheckmark(discord.ui.DynamicItem[discord.ui.Button], template=r'todolist:button:[A-Z]'):
    def __init__(self, custom_id: str):
        super().__init__(
            discord.ui.Button(
                style=discord.ButtonStyle.blurple,
                custom_id=custom_id,
                emoji=list(EMOTES_CUSTOM_ID.keys())[list(EMOTES_CUSTOM_ID.values()).index(f'TodoButton{custom_id[-1]}')],
            )
        )
        self.data_list = []
        self.emoji = list(EMOTES_CUSTOM_ID.keys())[list(EMOTES_CUSTOM_ID.values()).index(f'TodoButton{custom_id[-1]}')]

    @classmethod
    async def from_custom_id(cls, _interaction: discord.Interaction, _item: discord.ui.Button, match: re.Match[str]):
        return cls(match.string)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        message = await interaction.original_response()
        embed_uuid = message.embeds[0].footer.text
        try:
            with open(os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild_id), 'todolists', f'{embed_uuid}.json'), 'r') as file:
                full_dict = json.load(file)
        except OSError:
            print(f'Error opening todolist file on {interaction.guild.name} for {embed_uuid}')
            await interaction.followup.send('> Unexpected Error (`TodolistButtonCheckmark.callback`)', ephemeral=True)
            return
        if (
                'roles' in full_dict['access'].keys() and 'members' in full_dict['access'].keys()
                and not has_permissions(interaction, full_dict['access'])
        ):
            await interaction.followup.send('> You do not have the permission to click on this button', ephemeral=True)
            return
        self.data_list = priority_dict_to_list(full_dict['tasks'])
        self.data_list.pop(list(EMOTES_CUSTOM_ID.keys()).index(self.emoji))

        updated_todolist_view = TodolistViewMenu()
        updated_todolist_view.refresh_view(
            {'access': full_dict['access'], 'tasks': list_to_priority_dict(self.data_list)},
            message.embeds[0].title.removeprefix('☑️️ **|** '),
            str(interaction.guild_id),
            embed_uuid
        )
        await interaction.message.edit(view=updated_todolist_view, embed=updated_todolist_view.embed)
