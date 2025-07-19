from __future__ import annotations

import configparser
import functools
import pathlib
import random
import sqlite3
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.modules.stockpile_viewer.stockpile_interface_handling import get_stockpile_info
from src.utils import (
    OISOL_HOME_PATH,
    DataFilesPath,
    DiscordIdType,
    InterfacesTypes,
    Shard,
)

if TYPE_CHECKING:
    from main import Oisol


@functools.lru_cache
def get_shard_stockpiles_subregions(shard_name: str, _code: str) -> list[str]:
    """
    :param shard_name: Shard to pull the data from, either ABLE, BAKER or CHARLIE
    :param _code: Arbitrary value to detect new command run (new code means new stock means need to rerun the full func)
    :return: List of all available stockpiles in a given shard
    """

    with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
        stockpiles_subregions = conn.cursor().execute(
            f"SELECT Region, Subregion FROM StockpilesZones WHERE Shard == '{shard_name}'",
        ).fetchall()
    return [' | '.join(subregion) for subregion in stockpiles_subregions]


@functools.lru_cache
def get_current_shard(path: pathlib.Path, _code: str) -> str:
    """
    :param path: path to read the config from
    :param _code: Arbitrary value to detect new command run (new code means new stock means need to rerun the full func)
    :return: Current shard of the guild from the config file (Able as default value)
    """
    config = configparser.ConfigParser()
    config.read(path)
    return config.get('default', 'shard', fallback=Shard.ABLE.name)


class ModuleStockpiles(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot

    @app_commands.command(name='stockpile-interface-create', description='Create a new stockpile interface')
    async def stockpile_interface_create(
            self,
            interaction: discord.Interaction,
            name: str,
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
        self.bot.logger.command(f'stockpile-interface-create command by {interaction.user.name} on {interaction.guild.name}')

        # Send an empty stockpile interface
        await interaction.response.send_message(
            embed=discord.Embed().from_dict(get_stockpile_info(interaction.guild_id, interface_name=name)),
        )
        # Retrieve the interface message id
        message_id = (await interaction.original_response()).id

        access_list = []

        # Get all non-nulls roles & access as permission list
        if role_1:
            access_list.append((interaction.guild_id, message_id, role_1.id, DiscordIdType.ROLE.name))
        if role_2:
            access_list.append((interaction.guild_id, message_id, role_2.id, DiscordIdType.ROLE.name))
        if role_3:
            access_list.append((interaction.guild_id, message_id, role_3.id, DiscordIdType.ROLE.name))
        if role_4:
            access_list.append((interaction.guild_id, message_id, role_4.id, DiscordIdType.ROLE.name))
        if role_5:
            access_list.append((interaction.guild_id, message_id, role_5.id, DiscordIdType.ROLE.name))
        if member_1:
            access_list.append((interaction.guild_id, message_id, member_1.id, DiscordIdType.USER.name))
        if member_2:
            access_list.append((interaction.guild_id, message_id, member_2.id, DiscordIdType.USER.name))
        if member_3:
            access_list.append((interaction.guild_id, message_id, member_3.id, DiscordIdType.USER.name))
        if member_4:
            access_list.append((interaction.guild_id, message_id, member_4.id, DiscordIdType.USER.name))
        if member_5:
            access_list.append((interaction.guild_id, message_id, member_5.id, DiscordIdType.USER.name))

        # Add current roles & members access to db
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            # Only update the access db if specific permissions were given
            if access_list:
                cursor.executemany(
                    'INSERT INTO GroupsInterfacesAccess (GroupId, InterfaceId, DiscordId, DiscordIdType) VALUES (?, ?, ?, ?)',
                    access_list,
                )
            cursor.execute(
                'INSERT INTO AllInterfacesReferences (GroupId, ChannelId, MessageId, InterfaceType, InterfaceReference, InterfaceName) VALUES (?, ?, ?, ?, ?, ?)',
                (interaction.guild_id, interaction.channel_id, message_id, InterfacesTypes.STOCKPILE.value, None, name),
            )
            conn.commit()

    @app_commands.command(name='stockpile-interface-clear', description='Clear a specific interface')
    async def clear_interface(self, interaction: discord.Interaction, interface_name: str) -> None:
        self.bot.logger.command(
            f'stockpile-interface-clear command by {interaction.user.name} on {interaction.guild.name}')
        # Case where the user did not select the interface from the provided options
        ids_list = interface_name.split('.')
        if len(ids_list) != 3 or not all(ids.isdigit() for ids in ids_list):
            await interaction.response.send_message(
                '> The provided interface name is not correct',
                ephemeral=True,
                delete_after=5,
            )
            return

        # Ensure use is authorized to interact with interface
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            conn.cursor().execute(
                f"DELETE FROM GroupsStockpilesList WHERE GroupId == {interaction.guild_id} AND InterfaceId == '{ids_list[2]}'",
            )
            conn.commit()

        await self.bot.refresh_interface(
            ids_list[0],
            ids_list[1],
            ids_list[2],
            discord.Embed().from_dict(get_stockpile_info(int(ids_list[0]), interface_id=int(ids_list[2]))),
        )

        await interaction.response.send_message(
            '> The interface was properly cleared',
            ephemeral=True,
            delete_after=5,
        )

    @app_commands.command(name='stockpile-interface-clear-all', description='Clear all server stockpiles interfaces')
    async def clear_all_interfaces(self, interaction: discord.Interaction) -> None:
        self.bot.logger.command(
            f'stockpile-interface-clear-all command by {interaction.user.name} on {interaction.guild.name}')

        # Ensure use is authorized to interact with interface
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            all_server_stockpiles_interfaces_raw = cursor.execute(
                f"SELECT GroupId, ChannelId, MessageId FROM AllInterfacesReferences WHERE GroupId == '{interaction.guild_id}' AND InterfaceType == '{InterfacesTypes.STOCKPILE.value}'",
            ).fetchall()
            cursor.executemany(
                'DELETE FROM GroupsStockpilesList WHERE GroupId == ? AND InterfaceId == ?',
                [(group_id, message_id) for group_id, _, message_id in all_server_stockpiles_interfaces_raw],  # channel id not required here
            )
            conn.commit()

        # Refresh all interfaces (next: ensure perf is ok here)
        for group_id, channel_id, message_id in all_server_stockpiles_interfaces_raw:
            await self.bot.refresh_interface(
                group_id,
                channel_id,
                message_id,
                discord.Embed().from_dict(get_stockpile_info(int(group_id), interface_id=int(message_id))),
            )

        await interaction.response.send_message(
            '> All stockpiles interfaces were properly cleared',
            ephemeral=True,
            delete_after=5,
        )

    @app_commands.command(name='stockpile-interface-get', description='Get an existing interface')
    async def stockpile_get_interface(self, interaction: discord.Interaction, interface_name: str) -> None:
        self.bot.logger.command(f'stockpile-interface-get command by {interaction.user.name} on {interaction.guild.name}')
        # Case where the user did not select the interface from the provided options
        ids_list = interface_name.split('.')
        if len(ids_list) != 3 or not all(ids.isdigit() for ids in ids_list):
            await interaction.response.send_message(
                '> The provided interface name is not correct',
                ephemeral=True,
                delete_after=5,
            )
            return

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            before_interface = cursor.execute(
                f"SELECT GroupId, ChannelId, MessageId, InterfaceType, InterfaceReference, InterfaceName FROM AllInterfacesReferences WHERE GroupId == '{interaction.guild_id}' AND MessageId == '{ids_list[2]}'",
            ).fetchone()

            # Send an empty stockpile interface
            await interaction.response.send_message(
                embed=discord.Embed().from_dict(get_stockpile_info(interaction.guild_id, interface_name=before_interface[5])),
            )
            # Retrieve the interface message id
            message_id = (await interaction.original_response()).id

            cursor.execute(
                f"UPDATE AllInterfacesReferences SET ChannelId = '{interaction.channel_id}', MessageId = '{message_id}' WHERE GroupId == '{interaction.guild_id}' AND MessageId == '{before_interface[2]}'",
            )
            cursor.execute(
                f"UPDATE GroupsStockpilesList SET InterfaceId = '{message_id}' WHERE GroupId == '{interaction.guild_id}' AND InterfaceId == '{before_interface[2]}'",
            )
            conn.commit()

        # Delete existing interface
        channel = self.bot.get_channel(int(before_interface[1]))
        if channel is not None:
            try:
                message = await channel.fetch_message(int(before_interface[2]))
                await message.delete()
            except discord.NotFound:
                pass

        await self.bot.refresh_interface(
            interaction.guild_id,
            interaction.channel_id,
            message_id,
            discord.Embed().from_dict(get_stockpile_info(int(interaction.guild_id), interface_id=int(message_id))),
        )

    @app_commands.command(name='stockpile-create', description='Create a new stockpile')
    async def stockpile_create(self, interaction: discord.Interaction, interface_name: str, code: str, localisation: str, stockpile_name: str) -> None:
        self.bot.logger.command(f'stockpile-create command by {interaction.user.name} on {interaction.guild.name}')
        # Case where a user entered an invalid sized code
        if len(code) != 6:
            await interaction.response.send_message('> The code must be a 6-digits code', ephemeral=True, delete_after=5)
            return
        # Case where a user entered a code without digits only
        if not code.isdigit():
            await interaction.response.send_message('> The code contains non digit characters', ephemeral=True, delete_after=5)
            return
        # Case where a user did not select a provided localisation
        if ' | ' not in localisation or localisation.startswith(' | '):
            await interaction.response.send_message(
                '> The localisation you entered is incorrect, displayed localisations are clickable',
                ephemeral=True,
                delete_after=5,
            )
            return
        # Case where the user did not select the interface from the provided options
        ids_list = interface_name.split('.')
        if len(ids_list) != 3 or not all(ids.isdigit() for ids in ids_list):
            await interaction.response.send_message(
                '> The provided interface name is not correct',
                ephemeral=True,
                delete_after=5,
            )
            return

        region, subregion = localisation.split(' | ')  # Only one '|' -> 2 splits
        shard_name = get_current_shard(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini', code)
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            # Retrieve zone entry with building type
            cursor = conn.cursor()
            stockpile_type = cursor.execute(
                'SELECT Type FROM StockpilesZones WHERE Shard == (?) AND Subregion == (?)',
                (shard_name, subregion),
            ).fetchone()[0]

            # Insert new stockpile to db
            cursor.execute(
                'INSERT INTO GroupsStockpilesList (GroupId, InterfaceId, Region, Subregion, Code, Name, Type) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (interaction.guild_id, ids_list[2], region, subregion, code, stockpile_name, stockpile_type),
            )
            conn.commit()

        await self.bot.refresh_interface(
            ids_list[0],
            ids_list[1],
            ids_list[2],
            discord.Embed().from_dict(get_stockpile_info(int(ids_list[0]), interface_id=int(ids_list[2]))),
        )

        await interaction.response.send_message('> Stockpile was properly added', ephemeral=True, delete_after=5)

    @app_commands.command(name='stockpile-delete', description='Delete an existing stockpile')
    async def stockpile_delete(self, interaction: discord.Interaction, interface_name: str, stockpile_code: str) -> None:
        self.bot.logger.command(f'stockpile-delete command by {interaction.user.name} on {interaction.guild.name}')
        # Case where a user entered an invalid sized code
        if len(stockpile_code) != 6:
            await interaction.response.send_message(
                '> The code must be a 6-digits code',
                ephemeral=True,
                delete_after=5,
            )
            return
        # Case where a user entered a code without digits only
        if not stockpile_code.isdigit():
            await interaction.response.send_message(
                '> The code contains non digit characters',
                ephemeral=True,
                delete_after=5,
            )
            return
        # Case where the user did not select the interface from the provided options
        ids_list = interface_name.split('.')
        if len(ids_list) != 3 or not all(ids.isdigit() for ids in ids_list):
            await interaction.response.send_message(
                '> The provided interface name is not correct',
                ephemeral=True,
                delete_after=5,
            )
            return

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            if not (deleted_stockpiles := cursor.execute(f"DELETE FROM GroupsStockpilesList WHERE GroupId == {interaction.guild_id} AND Code == '{stockpile_code}' RETURNING *").fetchall()):
                await interaction.response.send_message(
                    '> The stockpile code you provided does not exists.',
                    ephemeral=True,
                    delete_after=5,
                )
                return
            conn.commit()

        await self.bot.refresh_interface(
            ids_list[0],
            ids_list[1],
            ids_list[2],
            discord.Embed().from_dict(get_stockpile_info(int(ids_list[0]), interface_id=int(ids_list[2]))),
        )

        # Expected outcome
        if len(deleted_stockpiles) == 1:
            await interaction.response.send_message(
                f'> The stockpile (code: {stockpile_code}) was properly removed.',
                ephemeral=True,
                delete_after=5,
            )
        # This should cover the very unlikely case where a same group has multiple stockpiles with the same code (0.00000000010000020000%)
        else:
            self.bot.logger.warning(
                f'At least two stockpiles with the same code were deleted on {interaction.guild.name}')
            await interaction.response.send_message(
                f'The following stockpiles with code {stockpile_code} were deleted:\n{''.join(f'- {deleted_stockpile[4]}, {deleted_stockpile[2]} in {deleted_stockpile[1]}\n' for deleted_stockpile in deleted_stockpiles)}',
                ephemeral=True,  # No auto delete in case of a fuck-up
            )

    # AUTOCOMPLETE METHODS
    @stockpile_create.autocomplete('localisation')
    async def region_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        """
        :param interaction: discord command interaction object
        :param current: current input given by the user
        :return: list of possibles autocompletion results using the current input
        """
        code = next((opt['value'] for opt in interaction.data['options'] if opt.get('name', '') == 'code'), '0')
        current_shard = get_current_shard(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini', code)
        stockpiles = get_shard_stockpiles_subregions(current_shard, code)

        if not current:
            return [app_commands.Choice(name=city, value=city) for city in random.choices(stockpiles, k=10)]

        current_stockpiles = [stockpile for stockpile in stockpiles if current.lower() in stockpile.lower()][:25]
        return [app_commands.Choice(name=city, value=city) for city in current_stockpiles]

    @stockpile_get_interface.autocomplete('interface_name')
    @clear_interface.autocomplete('interface_name')
    @stockpile_delete.autocomplete('interface_name')
    @stockpile_create.autocomplete('interface_name')
    async def interface_name_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        """
        :param interaction: current interaction object
        :param current: current user input in command parameter
        :return: list of interfaces names matching with current input
        """
        # Retrieve all server interfaces of type 'STOCKPILE_VIEW'
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()

            # Get all guild stockpile interfaces
            all_guild_stockpiles_interfaces = cursor.execute(
                f"SELECT ChannelId, MessageId, InterfaceName FROM AllInterfacesReferences WHERE InterfaceType == '{InterfacesTypes.STOCKPILE.value}' AND GroupId == '{interaction.guild_id}'",
            ).fetchall()
            # Cast id to str for better interaction
            all_guild_stockpiles_interfaces = [
                (str(channel_id), str(message_id), interface_name) for channel_id, message_id, interface_name in all_guild_stockpiles_interfaces
            ]

            # Get associated permissions
            interfaces_id = [str(interface_id[1]) for interface_id in all_guild_stockpiles_interfaces]
            all_guild_stockpiles_interfaces_permissions = cursor.execute(
                f"SELECT InterfaceId, DiscordId FROM GroupsInterfacesAccess WHERE GroupId == '{interaction.guild_id}' AND InterfaceId IN ({','.join(interfaces_id)})",
            ).fetchall()

        user_access = [permission[0] for permission in all_guild_stockpiles_interfaces_permissions if str(interaction.user.id) in permission or any(str(user_role.id) in permission for user_role in interaction.user.roles)]

        # Public interfaces
        user_access += list({interface[1] for interface in all_guild_stockpiles_interfaces} - {permission[0] for permission in all_guild_stockpiles_interfaces_permissions})

        # Get only the interfaces the user has access to
        all_guild_stockpiles_interfaces_updated = [
            interface for interface in all_guild_stockpiles_interfaces if interface[1] in user_access
        ]

        # Sort by name in ascending order
        all_guild_stockpiles_interfaces_updated.sort(key=lambda tup: tup[2])

        return [
            app_commands.Choice(
                name=interface_name,
                value=f'{interaction.guild_id}.{channel_id}.{message_id}',
            ) for channel_id, message_id, interface_name in all_guild_stockpiles_interfaces_updated if current in interface_name
        ]
