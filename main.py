import configparser
import discord
import os
import pathlib
import time
from discord.ext import commands
from dotenv import load_dotenv
from src.modules.config.ModuleConfig import ModuleConfig
from src.modules.config.ConfigInterfaces import ConfigViewMenu
from src.modules.registre.ModuleRegister import ModuleRegister
from src.modules.registre.RegisterViewMenu import RegisterViewMenu
from src.modules.todolist.TodolistViewMenu import TodolistViewMenu, TodolistButtonCheckmark
from src.modules.stockpile_viewer.ModuleStockpile import ModuleStockpiles
from src.modules.todolist.ModuleTodolist import ModuleTodolist
from src.modules.wiki.ModuleWiki import ModuleWiki
from src.utils.CsvHandler import CsvHandler
from src.utils.functions import safeguarded_nickname
from src.utils.oisol_enums import DataFilesPath, Modules


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

    def validate_all_members(self, members: list, server_id: str, recruit_id: int):
        # Things to ensure:
        # - All members are unique
        # - All members are part of the guild/server
        # - All members are recruits

        guild = self.get_guild(int(server_id))
        all_members = []
        all_members_id = []
        for member in members:
            if int(member['member']) in [m.id for m in guild.members] and guild.get_member(int(member['member'])).get_role(recruit_id) and member['member'] not in all_members_id:
                all_members.append(member)
                all_members_id.append(member['member'])

        return all_members

    async def update_register(self, server_id: str, all_members: list):
        oisol_server_home_path = os.path.join('/', 'oisol', server_id)
        try:
            config = configparser.ConfigParser()
            config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        except FileNotFoundError:
            return
        csv_handler = CsvHandler(['member', 'timer'])
        all_members = self.validate_all_members(all_members, server_id, int(config['register']['recruit_id']))
        csv_handler.csv_rewrite_file(os.path.join(oisol_server_home_path, DataFilesPath.REGISTER.value), all_members, Modules.REGISTER)

        guild = self.get_guild(int(server_id))
        channel = guild.get_channel(int(config['register']['channel']))
        message = await channel.fetch_message(int(config['register']['message_id']))
        register_view = RegisterViewMenu()
        register_view.refresh_register_embed(server_id)
        await message.edit(view=register_view, embed=register_view.get_current_embed())

    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before.id == before.guild.owner.id:
            return
        oisol_server_home_path = os.path.join('/', 'oisol', str(before.guild.id))
        try:
            config = configparser.ConfigParser()
            config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        except FileNotFoundError:
            return
        # In some cases, there might be an update of any members roles before the init command is executed.
        # As such this ensures there are no errors on the bot side when this case happens.
        try:
            if not config['register']['recruit_id']:
                return
        # If there are no register values, no point in doing any of the checks bellow the except.
        except KeyError:
            return
        csv_handler = CsvHandler(['member', 'timer'])

        # Member is now a recruit
        if int(config['register']['recruit_id']) in [role.id for role in after.roles] and int(config['register']['recruit_id']) not in [role.id for role in before.roles] and config['register']['input']:
            all_members = csv_handler.csv_get_all_data(os.path.join(oisol_server_home_path, DataFilesPath.REGISTER.value), Modules.REGISTER)
            await after.edit(nick=safeguarded_nickname(f'{config["register"]["input"]} {after.display_name}'))
            await self.update_register(str(before.guild.id), all_members + [{'member': after.id, 'timer': int(time.time())}])

        # Member is now a promoted recruit
        # Here I made the choice that any recruit having his recruit role removed is because he got promoted,
        # what usually happens in FCF is that recruit are kicked when they do dumb shit
        # If it becomes necessary in the future, I will add a classic member role in the config
        elif int(config['register']['recruit_id']) in [role.id for role in before.roles] and int(config['register']['recruit_id']) not in [role.id for role in after.roles]:
            member_name = after.display_name
            if config['register']['input']:
                member_name.replace(config['register']['input'], '')
            if config['register']['output']:
                member_name = f'{config["register"]["output"]} {member_name}'
            if config['register']['promoted_get_tag'][0] == 'y':
                member_name = f'{config["regiment"]["tag"]} {member_name}'
            await after.edit(nick=safeguarded_nickname(member_name))
            all_members = csv_handler.csv_get_all_data(os.path.join(oisol_server_home_path, DataFilesPath.REGISTER.value), Modules.REGISTER)
            for i, member in enumerate(all_members):
                if member['member'] == str(after.id):
                    all_members.pop(i)
            await self.update_register(str(before.guild.id), all_members)


if __name__ == '__main__':
    load_dotenv()
    Oisol().run(os.getenv('DISCORD_TOKEN'), reconnect=True)
