import re
import sqlite3
import string
import time
from typing import Self

import discord

from src.utils import (
    EMOTES_CUSTOM_ID,
    OISOL_HOME_PATH,
    TODOLIST_MAXIMUM_TASKS_ON_INTERFACE,
    OisolLogger,
    PriorityType,
)


class TodolistViewMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.embed_uuid = ''
        self.guild_id = ''
        self.title = ''
        self.embed = None

    def refresh_view(self, todolist_title: str, guild_id: str, embed_uuid: str) -> None:
        self.title = todolist_title
        self.guild_id = guild_id
        self.embed_uuid = embed_uuid

        # Clear buttons and update embed
        self.clear_items()
        buttons_to_add = self._refresh_view_embed()

        # Re-add add button & tasks buttons
        self.add_item(self.add_tasks)
        for i in range(buttons_to_add):
            self.add_item(TodolistButtonCheckmark(f'todolist:button:{string.ascii_uppercase[i]}'))

    def _refresh_view_embed(self) -> int:
        """
        Update existing embed and return the number of buttons to be on the view
        :return: number of buttons on the interface
        """

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            current_tasks = conn.cursor().execute(
                f"SELECT TaskContent, TaskPriority FROM GroupsTodolistsTasks WHERE GroupId == {self.guild_id} AND TodolistId == '{self.embed_uuid}'",
            ).fetchall()

        # Sort tasks by priority
        current_tasks = [
            *[task for task in current_tasks if task[1] == PriorityType.HIGH.name],
            *[task for task in current_tasks if task[1] == PriorityType.MEDIUM.name],
            *[task for task in current_tasks if task[1] == PriorityType.LOW.name],
        ]
        self.embed = discord.Embed().from_dict({
            'title': f'☑️️ **|** {self.title}',
            'footer': {'text': self.embed_uuid},
            'fields': [{'name': f':regional_indicator_{string.ascii_lowercase[i]}: **|** {PriorityType[task[1]].value}', 'value': task[0], 'inline': True} for i, task in enumerate(current_tasks)],
        })
        return len(current_tasks)

    @discord.ui.button(style=discord.ButtonStyle.green, custom_id='Todolist:Add', emoji='➕')
    async def add_tasks(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        self.embed_uuid = interaction.message.embeds[0].footer.text
        self.title = interaction.message.embeds[0].title.removeprefix('☑️️ **|** ')

        # Retrieve all permissions for the todolist
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            todolist_permissions = conn.cursor().execute(
                f"SELECT DiscordId, DiscordIdType FROM GroupsInterfacesAccess WHERE GroupId == {interaction.guild_id} AND InterfaceId == '{self.embed_uuid}'",
            ).fetchall()

        # Check whether the user id or its roles id are in todolist permissions
        can_access = bool(next((permission for permission in todolist_permissions if interaction.user.id == permission[0] or permission[0] in [role.id for role in interaction.user.roles]), False)) or not todolist_permissions

        if not can_access:
            await interaction.response.send_message(
                '> You do not have the permission to click on this button',
                ephemeral=True,
                delete_after=5,
            )
            return

        await interaction.response.send_modal(TodolistModalAdd(self.embed_uuid, self.title))


class TodolistModalAdd(discord.ui.Modal, title='Todolist Add'):
    def __init__(self, embed_uuid: str, title: str):
        super().__init__()
        self.embed_uuid = embed_uuid
        self.todolist_title = title
        self.logger = OisolLogger('oisol')

    high_priority = discord.ui.TextInput(
        label=f'{PriorityType.HIGH.value} | High Priority',
        style=discord.TextStyle.long,
        required=False,
        placeholder='Use `,` for more than one item ...',
    )
    medium_priority = discord.ui.TextInput(
        label=f'{PriorityType.MEDIUM.value} | Medium Priority',
        style=discord.TextStyle.long,
        required=False,
        placeholder='Use `,` for more than one item ...',
    )
    low_priority = discord.ui.TextInput(
        label=f'{PriorityType.LOW.value} | Low Priority',
        style=discord.TextStyle.long,
        required=False,
        placeholder='Use `,` for more than one item ...',
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.logger.interface(f'todolist tasks added by {interaction.user.name} on {interaction.guild.name}')

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            # Get current tasks from db
            current_tasks = cursor.execute(
                f"SELECT GroupId, TodolistId, TaskContent, TaskPriority, LastUpdated FROM GroupsTodolistsTasks WHERE GroupId == {interaction.guild_id} AND TodolistId == '{self.embed_uuid}'",
            ).fetchall()
            if len(current_tasks) >= TODOLIST_MAXIMUM_TASKS_ON_INTERFACE:
                await interaction.response.send_message('> The todolist is at full capacity', ephemeral=True)
                return
            update_time = int(time.time())
            user_new_tasks = [
                *[(interaction.guild_id, self.embed_uuid, task_content.strip(), PriorityType.HIGH.name, update_time) for task_content in self.high_priority.value.split(',') if task_content.strip()],
                *[(interaction.guild_id, self.embed_uuid, task_content.strip(), PriorityType.MEDIUM.name, update_time) for task_content in self.medium_priority.value.split(',') if task_content.strip()],
                *[(interaction.guild_id, self.embed_uuid, task_content.strip(), PriorityType.LOW.name, update_time) for task_content in self.low_priority.value.split(',') if task_content.strip()],
            ]
            if (available_task_slots := TODOLIST_MAXIMUM_TASKS_ON_INTERFACE - len(current_tasks)) <= 0:
                possible_new_tasks = current_tasks
                rejected_new_tasks = user_new_tasks
            else:
                possible_new_tasks = current_tasks + user_new_tasks[:available_task_slots]
                rejected_new_tasks = user_new_tasks[available_task_slots:]
            cursor.execute(f"DELETE FROM GroupsTodolistsTasks WHERE GroupId == {interaction.guild_id} AND TodolistId == '{self.embed_uuid}'")
            cursor.executemany(
                'INSERT INTO GroupsTodolistsTasks (GroupId, TodolistId, TaskContent, TaskPriority, LastUpdated) VALUES (?, ?, ?, ?, ?)',
                possible_new_tasks,
            )
            conn.commit()

        # Recreate the view with the updated tasks
        updated_todolist_view = TodolistViewMenu()
        updated_todolist_view.refresh_view(self.todolist_title, str(interaction.guild_id), self.embed_uuid)

        # Defer is needed to edit the todolist & send potential message of bypassed tasks
        await interaction.response.defer()
        await interaction.edit_original_response(view=updated_todolist_view, embed=updated_todolist_view.embed)

        # Send the tasks that could not be added to the user with a format that makes it easier to copy / paste
        if rejected_new_tasks:
            await interaction.followup.send(
                f'> Tasks that were not put in the todolist: `{','.join(content[2] for content in rejected_new_tasks)}`',
                ephemeral=True,
            )


class TodolistButtonCheckmark(discord.ui.DynamicItem[discord.ui.Button], template=r'todolist:button:[A-Z]'):
    def __init__(self, custom_id: str):
        super().__init__(
            discord.ui.Button(
                style=discord.ButtonStyle.blurple,
                custom_id=custom_id,
                emoji=list(EMOTES_CUSTOM_ID.keys())[list(EMOTES_CUSTOM_ID.values()).index(f'TodoButton{custom_id[-1]}')],
            ),
        )
        self.emoji = list(EMOTES_CUSTOM_ID.keys())[list(EMOTES_CUSTOM_ID.values()).index(f'TodoButton{custom_id[-1]}')]
        self.logger = OisolLogger('oisol')

    @classmethod
    async def from_custom_id(cls, _interaction: discord.Interaction, _item: discord.ui.Button, match: re.Match[str]) -> Self:
        return cls(match.string)

    async def callback(self, interaction: discord.Interaction) -> None:
        self.logger.interface(f'todolist button checked by {interaction.user.name} on {interaction.guild.name}')
        embed_uuid = interaction.message.embeds[0].footer.text
        title = interaction.message.embeds[0].title.removeprefix('☑️️ **|** ')
        guild_id = str(interaction.guild_id)

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            # Retrieve all permissions for the todolist
            todolist_permissions = cursor.execute(
                f"SELECT DiscordId, DiscordIdType FROM GroupsInterfacesAccess WHERE GroupId == {interaction.guild_id} AND InterfaceId == '{embed_uuid}'",
            ).fetchall()

            # Check whether the user id or its roles id are in todolist permissions
            can_access = bool(next((permission for permission in todolist_permissions if interaction.user.id == permission[0] or permission[0] in [role.id for role in interaction.user.roles]), False)) or not todolist_permissions
            if not can_access:
                await interaction.response.send_message(
                    '> You do not have the permission to click on this button',
                    ephemeral=True,
                    delete_after=5,
                )
                return

            current_time = int(time.time())
            current_tasks = cursor.execute(
                f"SELECT GroupId, TodolistId, TaskContent, TaskPriority, LastUpdated FROM GroupsTodolistsTasks WHERE GroupId == {interaction.guild_id} AND TodolistId == '{embed_uuid}'",
            ).fetchall()
            current_tasks = [
                *[(task[0], task[1], task[2], task[3], current_time) for task in current_tasks if task[3] == PriorityType.HIGH.name],
                *[(task[0], task[1], task[2], task[3], current_time) for task in current_tasks if task[3] == PriorityType.MEDIUM.name],
                *[(task[0], task[1], task[2], task[3], current_time) for task in current_tasks if task[3] == PriorityType.LOW.name],
            ]
            current_tasks.pop(list(EMOTES_CUSTOM_ID).index(self.emoji))
            cursor.execute(
                f"DELETE FROM GroupsTodolistsTasks WHERE GroupId == {interaction.guild_id} AND TodolistId == '{embed_uuid}'",
            )
            # This could be reworked by using LIMIT in the previous DELETE request
            cursor.executemany(
                'INSERT INTO GroupsTodolistsTasks (GroupId, TodolistId, TaskContent, TaskPriority, LastUpdated) VALUES (?, ?, ?, ?, ?)',
                current_tasks,
            )
            conn.commit()

        updated_todolist_view = TodolistViewMenu()
        updated_todolist_view.refresh_view(title, guild_id, embed_uuid)
        await interaction.response.edit_message(view=updated_todolist_view, embed=updated_todolist_view.embed)
