import asyncio
import os
import sqlite3

import aiohttp
import discord
from aiohttp import ClientSession
from discord.ext import commands
from dotenv import load_dotenv

from src.modules.config import ConfigViewMenu, ModuleConfig
from src.modules.data_cleaning_tasks import DatabaseCleaner
from src.modules.foxhole_api_map_interactions_tasks import WorldSpawnsStatus
from src.modules.registre import ModuleRegister, RegisterViewMenu
from src.modules.stockpile_viewer import (
    ModuleStockpiles,
    StockpilesViewMenu,
    TaskUpdateAvailableStockpiles,
)
from src.modules.todolist import (
    ModuleTodolist,
    TodolistButtonCheckmark,
    TodolistViewMenu,
)
from src.modules.translation import ModuleTranslation
from src.modules.wiki import ModuleWiki
from src.utils import (
    OISOL_HOME_PATH,
    DataFilesPath,
    OisolFormatter,
    OisolLogger,
    Shard,
    repair_default_config_dict,
)
from src.utils.bot_translator import OisolTranslator


class Oisol(commands.Bot):
    def __init__(self):
        # Discord default config
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(
            command_prefix='$',
            intents=intents,
            help_command=commands.DefaultHelpCommand(no_category='Commands'),
        )

        # Custom bot emojis not relying on dedicated discord servers
        self.app_emojis = []

        # Sorted app_emojis with name as key to easily retrieve
        self.app_emojis_dict = {}

        # Custom logger with colors for tasks, commands, buttons interactions, joins, ...
        self.logger = OisolLogger('oisol')

        # Cache for non-persistent data (e.g. world spawns status such as town bases levels)
        self.cache = {}

        # Set of shards name, containing the shards that are currently live
        self.connected_shards = set()


    async def on_ready(self) -> None:
        # Modules loading
        await self.add_cog(ModuleConfig(self))
        await self.add_cog(ModuleStockpiles(self))
        await self.add_cog(ModuleRegister(self))
        await self.add_cog(ModuleTodolist(self))
        await self.add_cog(ModuleTranslation(self))
        await self.add_cog(ModuleWiki(self))

        await self._fetch_available_shards()

        # Ready the db
        self._setup_oisol_db()

        # Sync app emojis
        self.app_emojis = await self.fetch_application_emojis()
        self.app_emojis_dict = {emoji.name: f'<:{emoji.name}:{emoji.id}>' for emoji in self.app_emojis}

        try:
            synced = await self.tree.sync()
            self.logger.info(f'Synced {len(synced)} command(s)')
        except Exception as e:
            print(e)
            self.logger.error(f'Could not sync tree properly {e}')

        self.logger.info(f'Logged in as {self.user} (ID:{self.user.id})')

        # Display current guilds with the format: - Name (id)
        self.logger.info(f'Guilds joined ({len(self.guilds)}):\n{'\n'.join(f'- {guild.name} ({guild.id})' for guild in self.guilds)}')

        # Tasks loading
        await self.add_cog(DatabaseCleaner(self))
        await self.add_cog(TaskUpdateAvailableStockpiles(self))
        await self.add_cog(WorldSpawnsStatus(self))

    async def setup_hook(self) -> None:
        self.add_view(ConfigViewMenu())
        self.add_view(RegisterViewMenu())
        self.add_view(TodolistViewMenu())
        self.add_view(StockpilesViewMenu())
        self.add_dynamic_items(TodolistButtonCheckmark)
        await self.tree.set_translator(OisolTranslator())

    async def on_guild_join(self, guild: discord.Guild) -> None:
        self.logger.join(f'joined {guild.name} (id: {guild.id})')

        # Create guilds configs directory if it does not exist
        os.makedirs(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value, exist_ok=True)

        # Create oisol/config.ini file with default config
        if not os.path.isfile(config_path := OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{guild.id}.ini'):
            config = repair_default_config_dict()
            with open(config_path, 'w', newline='') as configfile:
                config.write(configfile)

    @staticmethod
    def _setup_oisol_db() -> None:
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            conn.cursor().executescript(
                '''
                CREATE TABLE IF NOT EXISTS AllInterfacesReferences(AssociationId TEXT, GroupId TEXT, ChannelId TEXT, MessageId TEXT, InterfaceType TEXT, InterfaceReference TEXT, InterfaceName TEXT);
                CREATE TABLE IF NOT EXISTS GroupsInterfacesAccess(GroupId TEXT, ChannelId INTEGER, MessageId TEXT, DiscordId TEXT, DiscordIdType TEXT, Level INTEGER);
                CREATE TABLE IF NOT EXISTS GroupsRegister(GroupId INTEGER, RegistrationDate INTEGER, MemberId INTEGER);
                CREATE TABLE IF NOT EXISTS GroupsStockpilesList(AssociationId TEXT, Region TEXT, Subregion TEXT, Code TEXT, Name TEXT, Type TEXT, Level TEXT);
                CREATE TABLE IF NOT EXISTS GroupsTodolistsTasks(AssociationId TEXT, GroupId INTEGER, TodolistId TEXT, TaskContent TEXT, TaskPriority TEXT, LastUpdated INTEGER);
                CREATE TABLE IF NOT EXISTS StockpilesZones(Shard TEXT, WarNumber INTEGER, ConquestStartTime INTEGER, Region TEXT, Subregion TEXT, Type TEXT);
                ''',
            )

    async def _test_potential_shard(self, session: ClientSession, shard: Shard) -> None:
        """
        Method that will try to get the default shard api/ url, if the return code is 503, the shard is not live else
        the shard is added to the bot's set of available shards
        :param session: Current session
        :param shard: Shard object to test
        """
        async with session.get(shard.value) as response:
            # Shards that are not live will specifically return the 503 code
            if response.status == 503:
                return

        if shard.name != 'BAKER': # Hard lock baker to prevent continuous errors
            # Shard is live
            self.connected_shards.add(shard.name)

    async def _fetch_available_shards(self) -> None:
        """
        Method that will call the method for each shard value concurrently
        """
        async with aiohttp.ClientSession() as session:
            tasks = [self._test_potential_shard(session, shard) for shard in Shard]
            await asyncio.gather(*tasks)


if __name__ == '__main__':
    load_dotenv()
    Oisol().run(os.getenv('DISCORD_TOKEN'), reconnect=True, log_formatter=OisolFormatter())
