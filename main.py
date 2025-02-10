import configparser
import logging
import os
import sqlite3

import discord
from discord.ext import commands
from dotenv import load_dotenv

from src.modules.config import ConfigViewMenu, ModuleConfig
from src.modules.registre import ModuleRegister, RegisterViewMenu
from src.modules.stockpile_viewer import ModuleStockpiles, StockpileTasks
from src.modules.todolist import (
    ModuleTodolist,
    TodolistButtonCheckmark,
    TodolistViewMenu,
)
from src.modules.wiki import ModuleWiki
from src.utils import (
    OISOL_HOME_PATH,
    DataFilesPath,
    repair_default_config_dict,
)


class Oisol(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(
            command_prefix='$',
            intents=intents,
            help_command=commands.DefaultHelpCommand(no_category='Commands'),
        )

    async def on_ready(self) -> None:
        # Ready the db
        self._setup_oisol_db()

        # Modules loading
        await self.add_cog(ModuleConfig(self))
        await self.add_cog(ModuleStockpiles(self))
        await self.add_cog(ModuleRegister(self))
        await self.add_cog(ModuleTodolist(self))
        await self.add_cog(ModuleWiki(self))

        try:
            synced = await self.tree.sync()
            logging.info(f'Synced {len(synced)} command(s)')
        except Exception:
            logging.exception('Could not sync tree properly')

        logging.info(f'Logged in as {self.user} (ID:{self.user.id})')
        await self.add_cog(StockpileTasks(self))

    async def setup_hook(self) -> None:
        self.add_view(ConfigViewMenu())
        self.add_view(RegisterViewMenu())
        self.add_view(TodolistViewMenu())
        self.add_dynamic_items(TodolistButtonCheckmark)

    async def on_guild_join(self, guild: discord.Guild) -> None:
        logging.info(f'[JOIN] joined {guild.name} (id: {guild.id})')

        # Create guilds configs directory if it does not exist
        os.makedirs(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value, exist_ok=True)

        # Create oisol/config.ini file with default config
        if not os.path.isfile(config_path := OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{str(guild.id)}.ini'):
            config = repair_default_config_dict()
            with open(config_path, 'w', newline='') as configfile:
                config.write(configfile)

    def _setup_oisol_db(self) -> None:
        self.connection = sqlite3.connect(OISOL_HOME_PATH / 'oisol.db')
        self.cursor = self.connection.cursor()

        # Available stockpiles per shard
        self.cursor.execute('CREATE TABLE IF NOT EXISTS StockpilesZones(Shard TEXT, WarNumber INTEGER, ConquestStartTime INTEGER, Region TEXT, Subregion TEXT, Type TEXT)')

        # Guilds stockpiles
        self.cursor.execute('CREATE TABLE IF NOT EXISTS GroupsStockpiles(GroupId INTEGER, Region TEXT, Subregion TEXT, Code INTEGER, Name TEXT, Type TEXT)')

        # Guilds register
        self.cursor.execute('CREATE TABLE IF NOT EXISTS GroupsRegister(GroupId INTEGER, RegistrationDate INTEGER, MemberId INTEGER)')

        # Guilds todolists
        self.cursor.execute('CREATE TABLE IF NOT EXISTS GroupsTodolistsAccess(GroupId INTEGER, TodolistId TEXT, DiscordId INTEGER, DiscordIdType TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS GroupsTodolistsTasks(GroupId INTEGER, TodolistId TEXT, TaskContent TEXT, TaskPriority TEXT, LastUpdated INTEGER)')

        # Interfaces references
        self.cursor.execute('CREATE TABLE IF NOT EXISTS AllInterfacesReferences(GroupId INTEGER, ChannelId INTEGER, MessageId INTEGER, InterfaceType TEXT)')


if __name__ == '__main__':
    # Logging setup
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)

    # Bot Run
    load_dotenv()
    Oisol().run(os.getenv('DISCORD_TOKEN'), reconnect=True, log_handler=None)
