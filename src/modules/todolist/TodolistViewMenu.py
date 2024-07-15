import discord
import os
import pathlib
import re
from more_itertools.recipes import consume
from typing_extensions import Tuple
from src.utils.oisol_enums import PriorityType
from src.utils.resources import EMOTES_CUSTOM_ID
from src.utils.functions import load_json_file, update_json_file


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


def refit_data(data_dict: dict) -> Tuple[dict, list]:
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
        self.title = todolist_title
        self.guild_id = guild_id
        self.embed_uuid = embed_uuid
        self.data_list = []
        self.data_dict, _ = refit_data(updated_data)

        update_json_file(
            os.path.join(pathlib.Path('/'), 'oisol', self.guild_id, 'todolists', f'{self.embed_uuid}.json'),
            self.data_dict
        )

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
        if not self.embed:
            self.embed = discord.Embed(title=f'☑️️ **|** {self.title}')
            self.embed.add_field(name='🔴 **|** Priorité Haute', value='')
            self.embed.add_field(name='🟡 **|** Priorité Moyenne', value='')
            self.embed.add_field(name='🟢 **|** Priorité Basse', value='')
            self.embed.set_footer(text=self.embed_uuid)
        self.embed.clear_fields()
        tmp_dict, _ = refit_data(self.data_dict)
        tmp_dict = tmp_dict['tasks']
        priority_tasks_dict = {'high': [], 'medium': [], 'low': []}
        for k, v in tmp_dict.items():
            for task in v:
                priority_tasks_dict[k].append({'content': task, 'priority': k})

        enumerated_tasks = {'high': '', 'medium': '', 'low': ''}
        for i, task in enumerate(
                (priority_tasks_dict['high'] + priority_tasks_dict['medium'] + priority_tasks_dict['low'])[:24]
        ):
            enumerated_tasks[
                task['priority']
            ] += f":regional_indicator_{'abcdefghijklmnopqrstuvwxyz'[i]}: **|** {task['content']}\n"

        for priority, tasks in [
            ('🔴 **|** Priorité Haute', enumerated_tasks['high']),
            ('🟡 **|** Priorité Moyenne', enumerated_tasks['medium']),
            ('🟢 **|** Priorité Basse', enumerated_tasks['low'])
        ]:
            self.embed.add_field(
                name=priority,
                value=tasks
            )

    @discord.ui.button(style=discord.ButtonStyle.green, custom_id='Todolist:Add', emoji='➕')
    async def add_tasks(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embed_uuid = interaction.message.embeds[0].footer.text
        try:
            permissions = load_json_file(
                os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild_id), 'todolists', f'{self.embed_uuid}.json')
            )['access']
        except OSError:
            print(f'Error opening todolist file on {interaction.guild.name} for {self.embed_uuid}')
            await interaction.response.send_message('> Unexpected Error (`TodolistViewMenu.add_tasks`)', ephemeral=True)
            return
        if 'roles' in permissions.keys() and 'members' in permissions.keys() and not has_permissions(interaction, permissions):
            await interaction.response.send_message('> Forbidden', ephemeral=True)
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
        label='🔴 | Priorité Haute',
        style=discord.TextStyle.long,
        required=False,
        placeholder='Use `,` for more than one item ...'
    )
    medium_priority = discord.ui.TextInput(
        label='🟡 | Priorité Moyenne',
        style=discord.TextStyle.long,
        required=False,
        placeholder='Use `,` for more than one item ...'
    )
    low_priority = discord.ui.TextInput(
        label='🟢 | Priorité Basse',
        style=discord.TextStyle.long,
        required=False,
        placeholder='Use `,` for more than one item ...'
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        full_dict = load_json_file(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild_id), 'todolists', f'{self.embed_uuid}.json')
        )
        data_dict = full_dict['tasks']
        if len(data_dict['high']) + len(data_dict['medium']) + len(data_dict['low']) >= 24:
            await interaction.followup.send('> The todolist is already full', ephemeral=True)
            return

        for priority, input_field in [
            (PriorityType.HAUTE.value, self.high_priority),
            (PriorityType.MOYENNE.value, self.medium_priority),
            (PriorityType.BASSE.value, self.low_priority)
        ]:
            for task in input_field.value.split(','):
                if task:
                    data_dict[priority].append(task)

        data_dict, bypassed_tasks = refit_data(
            {'access': full_dict['access'], 'tasks': data_dict}
        )
        if bypassed_tasks:
            await interaction.followup.send(
                f"> Tasks that were not put in the todolist: `{','.join([x for x in bypassed_tasks])}`",
                ephemeral=True
            )

        updated_todolist_view = TodolistViewMenu()
        updated_todolist_view.refresh_view(data_dict, self.todolist_title, str(interaction.guild_id), self.embed_uuid)
        await interaction.message.edit(view=updated_todolist_view, embed=updated_todolist_view.embed)
        await interaction.followup.send('> La todolist a été mise à jour', ephemeral=True)


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
    async def from_custom_id(cls, interaction: discord.Interaction, item: discord.ui.Button, match: re.Match[str]):
        return cls(match.string)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        message = await interaction.original_response()
        embed_uuid = message.embeds[0].footer.text
        try:
            full_dict = load_json_file(
                os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild_id), 'todolists', f'{embed_uuid}.json')
            )
        except OSError:
            print(f'Error opening todolist file on {interaction.guild.name} for {embed_uuid}')
            await interaction.response.send_message('> Unexpected Error (`TodolistButtonCheckmark.callback`)')
            return
        if 'roles' in full_dict['access'].keys() and 'members' in full_dict['access'].keys() and not has_permissions(interaction, full_dict['access']):
            await interaction.response.send_message('> Forbidden', ephemeral=True)
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
