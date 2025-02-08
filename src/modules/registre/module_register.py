from __future__ import annotations

import configparser
import logging
import os
import time
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import (
    MODULES_CSV_KEYS,
    CsvHandler,
    DataFilesPath,
    Modules,
    safeguarded_nickname,
)

from .register_view_menu import RegisterViewMenu

if TYPE_CHECKING:
    from main import Oisol


class ModuleRegister(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot
        self.CsvHandler = CsvHandler(MODULES_CSV_KEYS['register'])

    @app_commands.command(name='register-view', description='Command to display the current list of recruit with the date the got the recruit role')
    async def register_view(self, interaction: discord.Interaction) -> None:
        logging.info(f'[COMMAND] register-view command by {interaction.user.name} on {interaction.guild.name}')
        config = configparser.ConfigParser()
        config.read(self.bot.home_path / str(interaction.guild_id) / DataFilesPath.CONFIG.value)
        if not config.has_section('register'):
            config.add_section('register')
        config.set('register', 'channel', str(interaction.channel_id))

        register_view_instance = RegisterViewMenu()
        register_view_instance.refresh_register_embed(str(interaction.guild_id))

        await interaction.response.send_message(view=register_view_instance, embed=register_view_instance.embeds[0])

        sent_msg = await interaction.original_response()

        config.set('register', 'message_id', str(sent_msg.id))
        with open(self.bot.home_path / str(interaction.guild_id) / DataFilesPath.CONFIG.value, 'w', newline='') as configfile:
            config.write(configfile)

    def validate_all_members(self, members: list, server_id: int, recruit_id: int) -> list:
        """
        This function ensure that all members are unique, part of the server and recruit
        :param self:
        :param members: members list to process
        :param server_id: guild id
        :param recruit_id: recruit role id
        :return: list of processed members
        """
        guild = self.bot.get_guild(server_id)
        all_members = []
        all_members_id = []
        for member in members:
            if (
                    int(member['member']) in [m.id for m in guild.members]
                    and guild.get_member(int(member['member'])).get_role(recruit_id)
                    and member['member'] not in all_members_id
            ):
                all_members.append(member)
                all_members_id.append(member['member'])
        return all_members

    async def update_register(self, server_id: int, all_members: list) -> None:
        str_server_id = str(server_id)
        oisol_server_home_path = os.path.join('/', 'oisol', str_server_id)
        try:
            config = configparser.ConfigParser()
            config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        except FileNotFoundError:
            return
        csv_handler = CsvHandler(['member', 'timer'])
        all_members = self.validate_all_members(
            all_members,
            server_id,
            config.getint('register', 'recruit_id'),
        )
        csv_handler.csv_rewrite_file(
            os.path.join(oisol_server_home_path, DataFilesPath.REGISTER.value),
            all_members,
            Modules.REGISTER,
        )
        if not config.has_option('register', 'channel'):
            return

        guild = self.bot.get_guild(server_id)
        channel = guild.get_channel(config.getint('register', 'channel'))
        try:
            message = await channel.fetch_message(config.getint('register', 'message_id'))
        except discord.NotFound:
            return

        # Update existing register
        register_view = RegisterViewMenu()
        register_view.refresh_register_embed(str_server_id)
        await message.edit(view=register_view, embed=register_view.get_current_embed())

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        if before.id == before.guild.owner.id:
            return
        oisol_server_home_path = os.path.join('/', 'oisol', str(before.guild.id))
        config = configparser.ConfigParser()
        try:
            config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        except FileNotFoundError:
            return
        # In some cases, there might be an update of any members roles before the init command is executed.
        # As such this ensures there are no errors on the bot side when this case happens.
        if not config.has_section('register') or not config.has_option('register', 'recruit_id') or not bool(
                config.get('register', 'recruit_id')):
            return
        csv_handler = CsvHandler(['member', 'timer'])

        # Member is now a recruit
        if (
                config.getint('register', 'recruit_id') in [role.id for role in after.roles]
                and config.getint('register', 'recruit_id') not in [role.id for role in before.roles]
        ):
            all_members = csv_handler.csv_get_all_data(
                os.path.join(oisol_server_home_path, DataFilesPath.REGISTER.value),
            )
            if config.has_option('register', 'input'):
                await after.edit(nick=safeguarded_nickname(f'{config["register"]["input"]} {after.display_name}'))
            await self.update_register(
                before.guild.id, [*all_members, {'member': after.id, 'timer': int(time.time())}],
            )

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
            all_members = csv_handler.csv_get_all_data(
                os.path.join(oisol_server_home_path, DataFilesPath.REGISTER.value),
            )
            all_members = [member for member in all_members if member['member'] != str(after.id)]
            await self.update_register(before.guild.id, all_members)
