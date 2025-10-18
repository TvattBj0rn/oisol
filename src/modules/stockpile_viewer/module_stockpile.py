from __future__ import annotations

import configparser
import functools
import pathlib
import random
import sqlite3
import uuid
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import (
    OISOL_HOME_PATH,
    DataFilesPath,
    DiscordIdType,
    InterfacesTypes,
    Shard,
    refresh_interface, Faction,
)

from .stockpile_interface_handling import get_stockpile_info
from .stockpile_view_menu import StockpilesViewMenu

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


async def update_all_associated_stockpiles(bot: Oisol, association_id: str) -> None:
    with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
        all_interfaces_to_update = conn.cursor().execute(
            'SELECT GroupId, ChannelId, MessageId FROM AllInterfacesReferences WHERE AssociationId == ?',
            (association_id,),
        ).fetchall()

    for group_id, channel_id, message_id in all_interfaces_to_update:
        await refresh_interface(
            bot,
            channel_id,
            message_id,
            discord.Embed().from_dict(get_stockpile_info(int(group_id), association_id, message_id=int(message_id))),
        )


class ModuleStockpiles(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot

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
            member_1: discord.Member = None,
            member_2: discord.Member = None,
            member_3: discord.Member = None,
            member_4: discord.Member = None,
            member_5: discord.Member = None,
    ) -> None:
        self.bot.logger.command(f'stockpile-interface-create command by {interaction.user.name} on {interaction.guild.name}')
        # Create interface association id
        association_id = uuid.uuid4().hex

        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')
        guild_faction = config.get('regiment', 'faction', fallback='NEUTRAL')

        await interaction.response.send_message(
            embed=discord.Embed.from_dict({
                'title': f'<:region:1130915923704946758> | Stockpiles | {name}',
                'color': Faction[guild_faction].value,
                'description': '- **View Stockpiles** button: will display more or less stockpiles to the user depedning on its level of access to the interface (1-5)\n'
                               '- **Share ID** button: available only to the creator of the interface, get the association ID of the interface to share with other server(s)',
            }),
            view=StockpilesViewMenu(),
        )


    @app_commands.command(name='gfdsghf', description='Create a new stockpile interface')
    async def gdf(
            self,
            interaction: discord.Interaction,
            name: str,
            is_multiserver: bool = False,
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
        await interaction.response.defer(ephemeral=True)

        # Create interface association id
        association_id = uuid.uuid4().hex

        await self._create_stockpile_interface(
            interaction,
            association_id,
            name,
            locals(),
        )

        await interaction.followup.send('> The interface was properly created', ephemeral=True)
        if is_multiserver:
            await interaction.followup.send(f'> The id of your interface is: `{association_id}`, use it to connect to this interface from another server', ephemeral=True)

    @app_commands.command(name='stockpile-interface-join', description='Join an existing stockpile interface shared between multiple servers')
    async def multiserver_join_interface(
            self,
            interaction: discord.Interaction,
            interface_id: str,
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
        self.bot.logger.command(f'stockpile-interface-join command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.defer(ephemeral=True)

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            query_response = cursor.execute(
                'SELECT AssociationId, InterfaceName FROM AllInterfacesReferences WHERE AssociationId == ?',
                (interface_id,),
            ).fetchone()

            if not all(query_response):
                await interaction.followup.send('> The provided interface id is invalid', ephemeral=True)
                return

            await self._create_stockpile_interface(
                interaction,
                query_response[0],
                query_response[1],
                locals(),
                do_interface_update=True,
            )

            await interaction.followup.send('> The interface was successfully joined', ephemeral=True)

    @app_commands.command(name='stockpile-interface-get-pass', description='Get a password for a multiserver interface')
    async def get_interface_pass(self, interaction: discord.Interaction, interface_name: str) -> None:
        self.bot.logger.command(f'stockpile-interface-get-pass command by {interaction.user.name} on {interaction.guild.name}')

        # Convert interface_name to a readable text
        ids_list = interface_name.split('.')
        if (error_msg := self._validate_stockpile_ids(ids_list)) is not None:
            await interaction.response.send_message(
                error_msg,
                ephemeral=True,
                delete_after=5,
            )
            return
        await interaction.response.send_message(f'> The password of the selected interface is `{ids_list[-1]}`', ephemeral=True)


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

        await update_all_associated_stockpiles(self.bot, ids_list[3])

        await interaction.response.send_message(
            '> The interface was properly cleared',
            ephemeral=True,
            delete_after=5,
        )

    @app_commands.command(name='stockpile-create', description='Create a new stockpile')
    async def stockpile_create(self, interaction: discord.Interaction, interface_name: str, code: str, localisation: str, stockpile_name: str) -> None:
        self.bot.logger.command(f'stockpile-create command by {interaction.user.name} on {interaction.guild.name}')

        # Convert interface_name to a readable text
        ids_list = interface_name.split('.')

        if any(validations := (
                self._validate_stockpile_code(code),
                self._validate_stockpile_localisation(localisation),
                self._validate_stockpile_ids(ids_list),
        )):
            await interaction.response.send_message(
                next(v for v in validations if v is not None),
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
                'INSERT INTO GroupsStockpilesList (AssociationId, Region, Subregion, Code, Name, Type) VALUES (?, ?, ?, ?, ?, ?)',
                (ids_list[3], region, subregion, code, stockpile_name, stockpile_type),
            )
            conn.commit()

        await update_all_associated_stockpiles(self.bot, ids_list[3])
        await interaction.response.send_message('> Stockpile was properly added', ephemeral=True, delete_after=5)

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

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            if not (deleted_stockpiles := cursor.execute(
                    'DELETE FROM GroupsStockpilesList WHERE AssociationId == ? AND Code == ? RETURNING *',
                    (ids_list[3], stockpile_code),
            ).fetchall()):
                await interaction.response.send_message(
                    '> The stockpile code you provided does not exists.',
                    ephemeral=True,
                    delete_after=5,
                )
                return
            conn.commit()

        await update_all_associated_stockpiles(self.bot, ids_list[3])

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
    @stockpile_create.autocomplete('interface_name')
    @get_interface_pass.autocomplete('interface_name')
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
