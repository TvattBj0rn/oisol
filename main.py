import configparser
import os
import pathlib
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

from src.modules.config.ConfigInterfaces import ConfigViewMenu
from src.modules.config.ModuleConfig import ModuleConfig
from src.modules.registre.ModuleRegister import ModuleRegister
from src.modules.registre.RegisterViewMenu import RegisterViewMenu
from src.modules.stockpile_viewer.ModuleStockpile import ModuleStockpiles
from src.modules.todolist.ModuleTodolist import ModuleTodolist
from src.modules.todolist.TodolistViewMenu import (
    TodolistButtonCheckmark,
    TodolistViewMenu,
)
from src.modules.wiki.ModuleWiki import ModuleWiki
from src.utils.CsvHandler import CsvHandler
from src.utils.functions import repair_default_config_dict, safeguarded_nickname
from src.utils.oisol_enums import DataFilesPath, Modules
from src.utils.resources import MODULES_CSV_KEYS


class Oisol(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(
            command_prefix='$',
            intents=intents,
            help_command=commands.DefaultHelpCommand(no_category='Commands')
        )
        self.config_servers = dict()

    def load_configs(self):
        oisol_server_home_path = os.path.join(pathlib.Path('/'), 'oisol')
        for server_folder in os.listdir(oisol_server_home_path):
            if not server_folder.isdigit():
                continue
            server_config = configparser.ConfigParser()
            server_config.read(
                os.path.join(oisol_server_home_path, server_folder, 'config.ini')
            )
            self.config_servers[server_folder] = server_config

    async def on_ready(self):
        await self.add_cog(ModuleConfig(self))
        await self.add_cog(ModuleStockpiles(self))
        await self.add_cog(ModuleRegister(self))
        await self.add_cog(ModuleTodolist(self))
        await self.add_cog(ModuleWiki(self))

        try:
            synced = await self.tree.sync()
            print(f'Synced {len(synced)} command(s)')
        except Exception as e:
            print(e)

        self.load_configs()
        print(f'Logged in as {self.user} (ID:{self.user.id})')

    async def setup_hook(self):
        self.add_view(ConfigViewMenu())
        self.add_view(RegisterViewMenu())
        self.add_view(TodolistViewMenu())
        self.add_dynamic_items(TodolistButtonCheckmark)

    @staticmethod
    async def on_message_delete(message: discord.Message):
        if message.embeds and message.embeds[0].footer:
            test_path = os.path.join(
                pathlib.Path('/'),
                'oisol',
                str(message.guild.id),
                'todolists',
                f'{message.embeds[0].footer.text}.json'
            )
            try:
                os.remove(test_path)
            except FileNotFoundError:
                return

    def validate_all_members(self, members: list, server_id: int, recruit_id: int) -> list:
        """
        This function ensure that all members are unique, part of the server and recruit
        :param self:
        :param members: members list to check
        :param server_id: guild id
        :param recruit_id: recruit role id
        :return: list of processed members
        """
        guild = self.get_guild(server_id)
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

    async def update_register(self, server_id: int, all_members: list):
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
            config.getint('register', 'recruit_id')
        )
        csv_handler.csv_rewrite_file(
            os.path.join(oisol_server_home_path, DataFilesPath.REGISTER.value),
            all_members,
            Modules.REGISTER
        )
        if not config.has_option('register', 'channel'):
            return

        guild = self.get_guild(server_id)
        channel = guild.get_channel(config.getint('register', 'channel'))
        try:
            message = await channel.fetch_message(config.getint('register', 'message_id'))
        except discord.NotFound:
            return

        # Update existing register
        register_view = RegisterViewMenu()
        register_view.refresh_register_embed(str_server_id)
        await message.edit(view=register_view, embed=register_view.get_current_embed())

    async def on_member_update(self, before: discord.Member, after: discord.Member):
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
        if not config.has_section('register') or not config.has_option('register', 'recruit_id') or not bool(config.get('register', 'recruit_id')):
            return
        csv_handler = CsvHandler(['member', 'timer'])

        # Member is now a recruit
        if (
                config.getint('register', 'recruit_id') in [role.id for role in after.roles]
                and config.getint('register', 'recruit_id') not in [role.id for role in before.roles]
        ):
            all_members = csv_handler.csv_get_all_data(
                os.path.join(oisol_server_home_path, DataFilesPath.REGISTER.value)
            )
            if config.has_option('register', 'input'):
                await after.edit(nick=safeguarded_nickname(f'{config["register"]["input"]} {after.display_name}'))
            await self.update_register(
                before.guild.id, all_members + [{'member': after.id, 'timer': int(time.time())}]
            )

        # Member is now a promoted recruit
        # Here I made the choice that any recruit having his recruit role removed is because he got promoted,
        # what usually happens in FCF is that recruit are kicked when they do dumb shit
        # If it becomes necessary in the future, I will add a classic member role in the config
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
                member_name = f'{config.get('regiment', 'tag')} {member_name}'

            await after.edit(nick=safeguarded_nickname(member_name))
            all_members = csv_handler.csv_get_all_data(
                os.path.join(oisol_server_home_path, DataFilesPath.REGISTER.value)
            )
            all_members = [member for member in all_members if member['member'] != str(after.id)]
            await self.update_register(before.guild.id, all_members)

    async def on_guild_join(self, guild: discord.Guild):
        oisol_server_home_path = os.path.join('/', 'oisol', str(guild.id))

        # Create guild and guild/todolists directories if they do not exist
        os.makedirs(os.path.join(oisol_server_home_path), exist_ok=True)
        os.makedirs(os.path.join(oisol_server_home_path, 'todolists'), exist_ok=True)

        # Create oisol/*.csv files
        for datafile in [DataFilesPath.REGISTER, DataFilesPath.STOCKPILES]:
            if not os.path.isfile(os.path.join(oisol_server_home_path, datafile.value)):
                CsvHandler(MODULES_CSV_KEYS[datafile.name.lower()]).csv_try_create_file(
                    os.path.join(oisol_server_home_path, datafile.value)
                )

        # Create oisol/config.ini file with default config
        if not os.path.isfile(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value)):
            config = repair_default_config_dict()
            with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
                config.write(configfile)


if __name__ == '__main__':
    load_dotenv()
    Oisol().run(os.getenv('DISCORD_TOKEN'), reconnect=True)
