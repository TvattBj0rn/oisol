from __future__ import annotations

import configparser
import functools
import pathlib
import random
import sqlite3
import uuid
from sqlite3 import Connection
from typing import TYPE_CHECKING, Literal

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import (
    OISOL_HOME_PATH,
    DataFilesPath,
    DiscordIdType,
    Faction,
    InterfacesTypes,
    Shard,
    refresh_interface,
)

from .stockpile_interface_handling import get_stockpile_info
from .stockpile_view_menu import (
    StockpileBulkDeleteDropDownView,
    StockpileCreateModal,
    StockpileEditDropDownView,
    StockpilesViewMenu,
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

    @staticmethod
    def _get_user_access_level(
            conn: Connection,
            user_roles_ids: set[int],
            guild_id: str,
            channel_id: str,
            message_id: str,
    ) -> int:
        """
        Retrieve interface roles to compare the user's roles
        :param conn: Connection object from caller with context
        :param user_roles_ids: user discord roles ids
        :param guild_id: interaction guild id
        :param channel_id: interaction channel id
        :param message_id: interaction message id
        :return: an integer corresponding to the user's level of access on interface
        """
        all_interface_permissions = conn.cursor().execute(
            'SELECT DiscordId, Level FROM GroupsInterfacesAccess WHERE GroupId == ? AND ChannelId == ? AND MessageId = ?',
            (guild_id, int(channel_id), message_id),
        ).fetchall()

        # Get user level of access on this interface
        user_level = 5
        for role_id, access_level in all_interface_permissions:
            if int(role_id) in user_roles_ids and access_level < user_level:
                user_level = access_level
            if user_level == 1:  # The user has the maximum level of access, no need to iterate further
                break
        return user_level

    def _get_user_available_stockpiles(
            self,
            user_roles_ids: set[int],
            guild_id: str,
            channel_id: str,
            message_id: str,
            association_id: str,
    ) -> list[tuple]:
        """
        Retrieve the stockpiles the user has access to based on its roles
        :param user_roles_ids: user roles on the server
        :param guild_id: guild id
        :param channel_id: channel id
        :param message_id: message id
        :return: list of stockpiles info that the user can access
        """
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            user_level = self._get_user_access_level(conn, user_roles_ids, guild_id, channel_id, message_id)

            # Retrieve the stockpiles the user has access to
            available_user_stockpiles = conn.execute(
                'SELECT Region, Subregion, Code, Name, Type, Level FROM GroupsStockpilesList WHERE AssociationId == ? AND Level >= ?',
                (association_id, user_level),
            ).fetchall()

        return available_user_stockpiles # noqa RET504

    @staticmethod
    def _get_guild_faction(guild_id: int) -> str:
        """
        Retrieve the faction of a given guild using its configuration file
        :param guild_id: id of the guild to retrieve the faction from
        :return: Faction name
        """
        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{guild_id}.ini')
        return config.get('regiment', 'faction', fallback='NEUTRAL')

    @commands.Cog.listener(name='on_raw_message_delete')
    async def delete_listener(self, payload: discord.RawMessageDeleteEvent) -> None:
        # Convert interface_name to a readable text
        ids_list = [str(payload.guild_id), str(payload.channel_id), str(payload.message_id)]

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            potential_association_id_as_list = conn.cursor().execute(
                'SELECT AssociationId FROM AllInterfacesReferences WHERE GroupId == ? AND ChannelId == ? AND MessageId == ? AND InterfaceType IN (?, ?)',
                (ids_list[0], ids_list[1], ids_list[2], InterfacesTypes.STOCKPILE.value, InterfacesTypes.MULTISERVER_STOCKPILE.value),
            ).fetchall()

        if not potential_association_id_as_list:
            return

        # Add association id to the list to simulate an interaction parameter
        ids_list += potential_association_id_as_list[0]
        if self._validate_stockpile_ids(ids_list) is not None:
            return

        # Log only once it is certain the target message is a stockpile interface
        self.bot.logger.task('stockpile-interface-delete event triggered')

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()

            # Delete embed's message from db
            cursor.execute(
                'DELETE FROM AllInterfacesReferences WHERE AssociationId == ? AND GroupId == ? AND ChannelId == ? AND MessageId == ?',
                (ids_list[3], ids_list[0], ids_list[1], ids_list[2]),
            )

            # Check if another group was using the stockpiles
            potential_groups = cursor.execute(
                'SELECT AssociationId FROM AllInterfacesReferences WHERE AssociationId == ?',
                (ids_list[3],),
            ).fetchall()
            if not potential_groups:
                # No other group was using the stockpiles, delete them from db too
                cursor.execute(
                    'DELETE FROM AllInterfacesReferences WHERE AssociationId == ?',
                    (ids_list[3],),
                )

            conn.commit()

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
    ) -> None:
        self.bot.logger.command(f'stockpile-interface-create command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.defer(ephemeral=True)

        # Create interface association id
        association_id = uuid.uuid4().hex

        # Retrieve guild faction, for embed color
        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')
        guild_faction = config.get('regiment', 'faction', fallback='NEUTRAL')

        # Send default interface
        interface_message = await interaction.channel.send(
            embed=discord.Embed.from_dict({
                'title': f'<:region:1130915923704946758> | Stockpiles | {name}',
                'color': Faction[guild_faction].value,
                'description': '- **View Stockpiles**: will display more or less stockpiles to the user depending on its level of access to the interface (1-5)\n'
                               '- **Share ID**: available only to the creator of the interface, get the association ID of the interface to share with other server(s)',
                'footer': {'text': interaction.user.name, 'icon_url': interaction.user.avatar.url},
            }),
            view=StockpilesViewMenu(),
        )

        # Create the stockpile interface on the table
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            # Retrieve and set potential permission
            if any(permissions_list := [(param_name.split('_')[-1], param_value.id) for param_name, param_value in locals().items() if param_value is not None and param_name.startswith('role_')]):
                cursor.executemany(
                    'INSERT INTO GroupsInterfacesAccess (GroupId, ChannelId, MessageId, DiscordId, DiscordIdType, Level) VALUES (?, ?, ?, ?, ?, ?)',
                    [
                        (interaction.guild_id, interaction.channel_id, interface_message.id, discord_id, DiscordIdType.ROLE.name, level)
                        for level, discord_id in permissions_list
                    ],
                )
            # Add joined interface to existing interfaces
            cursor.execute(
                'INSERT INTO AllInterfacesReferences (AssociationId, GroupId, ChannelId, MessageId, InterfaceType, InterfaceReference, InterfaceName) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (association_id, interaction.guild_id, interaction.channel_id, interface_message.id, InterfacesTypes.STOCKPILE.value, None, name),
            )
            conn.commit()

        await interaction.followup.send('> The interface was properly created', ephemeral=True)

    @app_commands.command(name='stockpile-interface-join', description='Join an existing stockpile interface shared between multiple servers')
    async def multiserver_join_interface(
            self,
            interaction: discord.Interaction,
            interface_name: str,
            interface_id: str,
    ) -> None:
        self.bot.logger.command(f'stockpile-interface-join command by {interaction.user.name} on {interaction.guild.name}')

        # Convert interface_name to a readable text
        ids_list = interface_name.split('.')

        if (error_msg := self._validate_stockpile_ids(ids_list)) is not None:
            await interaction.response.send_message(
                error_msg,
                ephemeral=True,
                delete_after=5,
            )
            return

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()

            # Retrieve the provided association_id from the db
            user_association_id = cursor.execute(
                'SELECT AssociationId FROM AllInterfacesReferences WHERE AssociationId == ?',
                (interface_id,),
            ).fetchone()

            # Ensure the user provided association_id exists
            if not all(user_association_id):
                await interaction.response.send_message('> The provided interface id is invalid', ephemeral=True, delete_after=5)
                return

            guild_id, channel_id, message_id, association_id = ids_list

            # Update current interface association_id with user provided association_id
            cursor.execute(
                'UPDATE AllInterfacesReferences SET AssociationId = ? WHERE GroupId == ? AND ChannelId == ? AND MessageId == ? and InterfaceType == ?',
                (user_association_id[0], guild_id, channel_id, message_id, InterfacesTypes.STOCKPILE.value),
            )
            conn.commit()

        await interaction.response.send_message('> The interface was successfully joined', ephemeral=True, delete_after=5)

    @app_commands.command(name='stockpile-refresh-codes', description='Update up to 5 stockpiles codes from a list')
    async def refresh_codes(self, interaction: discord.Interaction, interface_name: str) -> None:
        self.bot.logger.command(f'stockpile-refresh-codes command by {interaction.user.name} on {interaction.guild.name}')

        # Convert interface_name to a readable text
        ids_list = interface_name.split('.')

        if (error_msg := self._validate_stockpile_ids(ids_list)) is not None:
            await interaction.response.send_message(
                error_msg,
                ephemeral=True,
                delete_after=5,
            )
            return
        interface_guild_id, interface_channel_id, interface_message_id, interface_association_id = ids_list

        user_role_ids = {role.id for role in interaction.user.roles}

        available_user_stockpiles = self._get_user_available_stockpiles(
            user_role_ids,
            interface_guild_id,
            interface_channel_id,
            interface_message_id,
            interface_association_id,
        )

        # Case where there is no stockpiles to refresh or no stockpiles the user has access to available for deletion
        if len(available_user_stockpiles) == 0:
            await interaction.response.send_message('> There are currently no stockpiles available for refresh', ephemeral=True, delete_after=5)
            return

        guild_faction = self._get_guild_faction(interaction.guild_id)

        await interaction.response.send_message(
            view=StockpileEditDropDownView(available_user_stockpiles, guild_faction, interface_association_id),
            ephemeral=True,
        )

    @app_commands.command(name='stockpile-interface-clear', description='Clear a specific interface')
    async def clear_interface(self, interaction: discord.Interaction, interface_name: str) -> None:
        self.bot.logger.command(f'stockpile-interface-clear command by {interaction.user.name} on {interaction.guild.name}')

        # Convert interface_name to a readable text
        ids_list = interface_name.split('.')

        if (error_msg := self._validate_stockpile_ids(ids_list)) is not None:
            await interaction.response.send_message(
                error_msg,
                ephemeral=True,
                delete_after=5,
            )
            return

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            conn.cursor().execute(
                'DELETE FROM GroupsStockpilesList WHERE AssociationId == ?',
                (ids_list[3],),
            )
            conn.commit()

        await interaction.response.send_message(
            '> The interface was properly cleared',
            ephemeral=True,
            delete_after=5,
        )

    @app_commands.command(name='stockpile-create', description='Create a new stockpile')
    async def stockpile_create(self, interaction: discord.Interaction, interface_name: str, code: str, localisation: str, stockpile_name: str, level: Literal['1', '2', '3', '4', '5'] = '5') -> None:
        self.bot.logger.command(f'stockpile-create command by {interaction.user.name} on {interaction.guild.name}')

        # Convert interface_name to a readable text
        ids_list = interface_name.split('.')

        if any(validations := (
                self._validate_stockpile_code(code),
                self._validate_stockpile_localisation(localisation),
                self._validate_stockpile_ids(ids_list),
                'Access level is invalid' if str(level) not in ['1', '2', '3', '4', '5'] else None,
        )):
            await interaction.response.send_message(
                next(v for v in validations if v is not None),
                ephemeral=True,
                delete_after=5,
            )
            return

        interface_guild_id, interface_channel_id, interface_message_id, interface_association_id = ids_list

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            user_access_level = self._get_user_access_level(
                conn,
                {role.id for role in interaction.user.roles},
                interface_guild_id,
                interface_channel_id,
                interface_message_id,
            )

        # Ensure the user is creating an appropriately leveled stockpile
        if user_access_level > int(level):
            await interaction.response.send_message(
                f'> Your level ({user_access_level}) does not have the permission to create this stockpile (stockpile level: {level})',
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
                'SELECT Type FROM StockpilesZones WHERE Shard == ? AND Subregion == ?',
                (shard_name, subregion),
            ).fetchone()[0]

            # Insert new stockpile to db
            cursor.execute(
                'INSERT INTO GroupsStockpilesList (AssociationId, Region, Subregion, Code, Name, Type, Level) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (ids_list[3], region, subregion, code, stockpile_name, stockpile_type, str(level)),
            )
            conn.commit()

        await interaction.response.send_message('> Stockpile was properly added', ephemeral=True, delete_after=5)

    @app_commands.command(name='stockpile-bulk-create', description='Create multiple stockpiles from a selected interface')
    async def stockpile_bulk_create(self, interaction: discord.Interaction, interface_name: str) -> None:
        self.bot.logger.command(f'stockpile-bulk-create command by {interaction.user.name} on {interaction.guild.name}')

        # Convert interface_name to a readable text
        ids_list = interface_name.split('.')

        if error_msg := self._validate_stockpile_ids(ids_list):
            await interaction.response.send_message(
                error_msg,
                ephemeral=True,
                delete_after=5,
            )
            return
        interface_guild_id, interface_channel_id, interface_message_id, interface_association_id = ids_list

        user_role_ids = {role.id for role in interaction.user.roles}

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            # Retrieve interface permissions
            all_interface_permissions = cursor.execute(
                'SELECT DiscordId, Level FROM GroupsInterfacesAccess WHERE GroupId == ? AND ChannelId == ? AND MessageId == ?',
                (interface_guild_id, int(interface_channel_id), interface_message_id),
            ).fetchall()

            # Get user level of access on this interface
            user_level = 5
            for role_id, access_level in all_interface_permissions:
                if int(role_id) in user_role_ids and int(access_level) < user_level:
                    user_level = access_level
                if user_level == 1:  # The user has the maximum level of access, no need to iterate further
                    break

        await interaction.response.send_modal(StockpileCreateModal(user_level, interface_association_id))

    @app_commands.command(name='stockpile-delete', description='Delete an existing stockpile')
    async def stockpile_delete(self, interaction: discord.Interaction, interface_name: str, stockpile_code: str) -> None:
        self.bot.logger.command(f'stockpile-delete command by {interaction.user.name} on {interaction.guild.name}')

        # Convert interface_name to a readable text
        ids_list = interface_name.split('.')

        if any(validations := (
            self._validate_stockpile_code(stockpile_code),
            self._validate_stockpile_ids(ids_list),
        )):
            await interaction.response.send_message(
                next(v for v in validations if v is not None),
                ephemeral=True,
                delete_after=5,
            )
            return

        interface_guild_id, interface_channel_id, interface_message_id, interface_association_id = ids_list

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            # Retrieve the user access level
            user_access_level = self._get_user_access_level(
                conn,
                {role.id for role in interaction.user.roles},
                interface_guild_id,
                interface_channel_id,
                interface_message_id,
            )
            if not (deleted_stockpiles := cursor.execute(
                    'DELETE FROM GroupsStockpilesList WHERE AssociationId == ? AND Code == ? AND Level >= ? RETURNING *',
                    (ids_list[3], stockpile_code, user_access_level),
            ).fetchall()):
                await interaction.response.send_message(
                    '> The stockpile code you provided does not exists.',
                    ephemeral=True,
                    delete_after=5,
                )
                return
            conn.commit()

        # Expected outcome
        if len(deleted_stockpiles) == 1:
            await interaction.response.send_message(
                f'> The stockpile (code: {stockpile_code}) was properly removed.',
                ephemeral=True,
                delete_after=5,
            )
        # This should cover the very unlikely case where a same group has multiple stockpiles with the same code
        else:
            self.bot.logger.warning(f'At least two stockpiles with the same code were deleted on {interaction.guild.name}')
            await interaction.response.send_message(
                f'The following stockpiles with code {stockpile_code} were deleted:\n{''.join(f'- {deleted_stockpile[4]}, {deleted_stockpile[2]} in {deleted_stockpile[1]}\n' for deleted_stockpile in deleted_stockpiles)}',
                ephemeral=True,  # No auto delete in case of a fuck-up
            )

    @app_commands.command(name='stockpile-bulk-delete', description='Delete multiple existing stockpiles from a selected interface')
    async def stockpile_bulk_delete(self, interaction: discord.Interaction, interface_name: str) -> None:
        self.bot.logger.command(f'stockpile-bulk-delete command by {interaction.user.name} on {interaction.guild.name}')

        # Convert interface_name to a readable text
        ids_list = interface_name.split('.')

        if error_msg := self._validate_stockpile_ids(ids_list):
            await interaction.response.send_message(
                error_msg,
                ephemeral=True,
                delete_after=5,
            )
            return
        interface_guild_id, interface_channel_id, interface_message_id, interface_association_id = ids_list

        user_role_ids = {role.id for role in interaction.user.roles}

        # Retrieve the stockpiles the user has access to
        available_user_stockpiles = self._get_user_available_stockpiles(
            user_role_ids,
            interface_guild_id,
            interface_channel_id,
            interface_message_id,
            interface_association_id,
        )

        # Case where there is no stockpiles to delete or no stockpiles the user has access to available for deletion
        if len(available_user_stockpiles) == 0:
            await interaction.response.send_message('> There are currently no stockpiles available for deletion', ephemeral=True, delete_after=5)
            return

        # Get the faction name
        guild_faction = self._get_guild_faction(interaction.guild_id)

        await interaction.response.send_message(view=StockpileBulkDeleteDropDownView(available_user_stockpiles, guild_faction, interface_association_id), ephemeral=True)

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

    @clear_interface.autocomplete('interface_name')
    @stockpile_delete.autocomplete('interface_name')
    @stockpile_bulk_delete.autocomplete('interface_name')
    @stockpile_create.autocomplete('interface_name')
    @stockpile_bulk_create.autocomplete('interface_name')
    @multiserver_join_interface.autocomplete('interface_name')
    @refresh_codes.autocomplete('interface_name')
    async def interface_name_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice]:
        """
        :param interaction: current interaction object
        :param current: current user input in command parameter
        :return: list of interfaces names matching with current input
        """
        # Retrieve all server interfaces of types 'STOCKPILE_VIEW', 'MULTISERVER_STOCKPILE_VIEW'
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()

            # Get all guild stockpile interfaces
            all_guild_stockpiles_interfaces = cursor.execute(
                'SELECT ChannelId, MessageId, InterfaceName, AssociationId FROM AllInterfacesReferences WHERE InterfaceType IN (?, ?) AND GroupId == ?',
                (InterfacesTypes.STOCKPILE.value, InterfacesTypes.MULTISERVER_STOCKPILE.value, interaction.guild_id),
            ).fetchall()

            # Get associated permissions
            interfaces_id = [interface_id[1] for interface_id in all_guild_stockpiles_interfaces]
            all_guild_stockpiles_interfaces_permissions = cursor.execute(
                f'SELECT MessageId, DiscordId FROM GroupsInterfacesAccess WHERE GroupId == ? AND MessageId IN ({', '.join('?' * len(interfaces_id))})',
                (interaction.guild_id, *interfaces_id),
            ).fetchall()

        # Get server interfaces the user has access to
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
                value=f'{interaction.guild_id}.{channel_id}.{message_id}.{association_id}',
            )
            for channel_id, message_id, interface_name, association_id in all_guild_stockpiles_interfaces_updated
            if current in interface_name
        ]

    @staticmethod
    def _validate_stockpile_code(code: str) -> str | None:
        """
        Ensure the validity of a Foxhole stockpile code by checking its length and its content (all digits is expected).
        :param code: The code to test
        :return: None if valid, the error message to send back to the user otherwise.
        """
        # Case where a user entered an invalid sized code
        if len(code) != 6:
            return '> The code must be a 6-digits code'

        # Case where a user entered a code without digits only
        if not code.isdigit():
            return '> The code contains non digit characters'

        return None

    @staticmethod
    def _validate_stockpile_localisation(localisation: str) -> str | None:
        """
        Ensure the validity of a stockpile localization by checking if it is splittable.
        :param localisation: The localization to test.
        :return: None if valid, the error message to send back to the user otherwise.
        """
        # Case where a user did not select a provided localisation
        if ' | ' not in localisation or localisation.startswith(' | '):
            return '> The localisation you entered is incorrect, displayed localisations are clickable'
        return None

    @staticmethod
    def _validate_stockpile_ids(ids_list: list[str]) -> str | None:
        """
        Ensure ids list validity by checking the length of the list and validate all element are str typed digits.
        :param ids_list:
        :return: None if valid, the error message to send back to the user otherwise.
        """
        # Case where the user did not select the interface from the provided options
        if len(ids_list) != 4 or not all(ids.isdigit() for ids in ids_list[0:-1]):
            return '> The provided interface name is not correct'
        return None

    @staticmethod
    def _generate_access_list(**kwargs) -> list:
        """
        Get all non-nulls roles & access as permission list
        """
        return [
            # Tuple of either member.id or role.id and discord id type
            (v.id, DiscordIdType.ROLE.name if k.startswith('role_') else DiscordIdType.USER.name)
            for k, v in kwargs.items()
            # Make sure we use appropriate non-null parameters
            if k.startswith(('role_', 'member_')) and v is not None
        ]

    async def _create_stockpile_interface(
            self,
            interaction: discord.Interaction,
            association_id: str,
            interface_name: str,
            permissions: dict,
            do_interface_update: bool = False,
    ) -> None:
        """
        Create a new stockpile in the db and send back an empty embed (do_interface_update False) or an embed with the
        existing data (do_interface_update True)
        :param interaction: discord interaction
        :param association_id: stockpile group id
        :param interface_name: interface name
        :param permissions: users / roles authorized on this interface
        :param do_interface_update: whether to refresh the empty embed with existing data (for /stockpile-interface-join cases)
        """
        # Send an empty stockpile interface as a separate message to hide association id on discord clients
        msg = await interaction.channel.send(embed=discord.Embed().from_dict(
            get_stockpile_info(
                interaction.guild_id, association_id, interface_name=interface_name,
            ),
        ))

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            # Only update the access db if specific permissions were given
            if any(raw_access_list := self._generate_access_list(**permissions)):
                cursor.executemany(
                    'INSERT INTO GroupsInterfacesAccess (GroupId, ChannelId, MessageId, DiscordId, DiscordIdType) VALUES (?, ?, ?, ?, ?)',
                    [
                        (interaction.guild_id, interaction.channel_id, msg.id, discord_id, discord_id_type)
                        for discord_id, discord_id_type in raw_access_list
                    ],
                )

            # Add joined interface to existing interfaces
            cursor.execute(
                'INSERT INTO AllInterfacesReferences (AssociationId, GroupId, ChannelId, MessageId, InterfaceType, InterfaceReference, InterfaceName) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (association_id, interaction.guild_id, interaction.channel_id, msg.id, InterfacesTypes.STOCKPILE.value,None, interface_name),
            )
            conn.commit()

        if do_interface_update:
            # Update the interface
            await refresh_interface(
                self.bot,
                interaction.channel_id,
                msg.id,
                discord.Embed().from_dict(get_stockpile_info(
                    interaction.guild_id,
                    association_id,
                    message_id=msg.id,
                    interface_name=interface_name,
                )),
            )
