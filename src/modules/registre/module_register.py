from __future__ import annotations

import configparser
import logging
import time
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import (
    DataFilesPath,
    safeguarded_nickname, OISOL_HOME_PATH,
)

from .register_view_menu import RegisterViewMenu

if TYPE_CHECKING:
    from main import Oisol


class ModuleRegister(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot

    @app_commands.command(name='register-view', description='Command to display the current list of recruit with the date the got the recruit role')
    async def register_view(self, interaction: discord.Interaction) -> None:
        logging.info(f'[COMMAND] register-view command by {interaction.user.name} on {interaction.guild.name}')

        # Retrieve config and channel ID if it exists, take the channel the command was executed from otherwise
        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{str(interaction.guild_id)}.ini')
        if not config.has_section('register'):
            config.add_section('register')
        config.set('register', 'channel', str(interaction.channel_id))

        # Create and send register view at page index 0
        register_view_instance = RegisterViewMenu()
        register_view_instance.refresh_register_embed(interaction.guild_id)
        await interaction.response.send_message(view=register_view_instance, embed=register_view_instance.embeds[0])

        # Update config
        sent_msg = await interaction.original_response()
        config.set('register', 'message_id', str(sent_msg.id))
        with open(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{str(interaction.guild_id)}.ini', 'w', newline='') as configfile:
            config.write(configfile)

    def validate_all_members(self, members: list, server_id: int, recruit_id: int) -> list:
        """
        This function ensure that all members are unique, part of the server and recruit
        :param members: members list to process
        :param server_id: guild id
        :param recruit_id: recruit role id
        :return: list of processed members
        """
        guild = self.bot.get_guild(server_id)
        return [t for t in members if t[2] in [m.id for m in guild.members] and guild.get_member(t[2]).get_role(recruit_id)]

    async def update_register(self, guild_id: int) -> None:
        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{str(guild_id)}.ini')

        # Get group data from db and validate it
        all_members = self.validate_all_members(
            self.bot.cursor.execute(
                f'SELECT GroupId, RegistrationDate, MemberId FROM GroupsRegister WHERE GroupId == {guild_id}',
            ).fetchall(),
            guild_id,
            config.getint('register', 'recruit_id'),
        )

        # Update register data
        self.bot.cursor.execute(f'DELETE FROM GroupsRegister WHERE GroupId == {guild_id}')
        self.bot.cursor.executemany(
            'INSERT INTO GroupsRegister (GroupId, RegistrationDate, MemberId) VALUES (?, ?, ?)',
            all_members,
        )
        self.bot.connection.commit()

        if not config.has_option('register', 'channel'):
            return

        guild = self.bot.get_guild(guild_id)
        channel = guild.get_channel(config.getint('register', 'channel'))
        try:
            message = await channel.fetch_message(config.getint('register', 'message_id'))
        except discord.NotFound:
            return

        # Update existing register
        register_view = RegisterViewMenu()
        register_view.refresh_register_embed(guild_id)
        await message.edit(view=register_view, embed=register_view.get_current_embed())

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        if before.id == before.guild.owner.id:
            return

        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{str(before.guild.id)}.ini')

        # In some cases, there might be an update of any members roles before the init command is executed.
        # As such this ensures there are no errors on the bot side when this case happens.
        if (
                not config.has_section('register') or not config.has_option('register', 'recruit_id')
                or not bool(config.get('register', 'recruit_id'))
        ):
            return

        # Member is now a recruit
        if (
                config.getint('register', 'recruit_id') in [role.id for role in after.roles]
                and config.getint('register', 'recruit_id') not in [role.id for role in before.roles]
        ):
            self.bot.cursor.execute(
                'INSERT INTO GroupsRegister (GroupId, RegistrationDate, MemberId) VALUES (?, ?, ?)',
                (before.guild.id, int(time.time()), before.id),
            )
            self.bot.connection.commit()
            await self.update_register(before.guild.id)

        # Member is now a promoted recruit
        elif (
                config.getint('register', 'recruit_id') in [role.id for role in before.roles]
                and config.getint('register', 'recruit_id') not in [role.id for role in after.roles]
        ):
            member_name = after.display_name
            # For this case, no need to handle trailing spaces at string start since it is handled on Discord part
            if config.has_option('register', 'input'):
                member_name = member_name.replace(config.get('register', 'input'), '')
            if config.has_option('register', 'output'):
                member_name = f'{config.get('register', 'output')} {member_name}'
            if config.has_option('register', 'promoted_get_tag') and config.getboolean('register', 'promoted_get_tag'):
                member_name = f'[{config.get('regiment', 'tag')}] {member_name}'

            await after.edit(nick=safeguarded_nickname(member_name))

            self.bot.cursor.execute(
                f'DELETE FROM GroupsRegister WHERE GroupId == {before.guild.id} AND MemberId == {before.id}',
            )
            self.bot.connection.commit()
            await self.update_register(before.guild.id)
