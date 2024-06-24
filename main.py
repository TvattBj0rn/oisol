import pathlib

import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from src.modules.config.ModuleConfig import ModuleConfig
from src.modules.registre.ModuleRegister import ModuleRegister
from src.modules.registre.RegisterViewMenu import RegisterViewMenu
from src.modules.stockpile_viewer.ModuleStockpile import ModuleStockpiles
from src.modules.todolist.ModuleTodolist import ModuleTodolist
# from src.modules.todolist.TodolistViewMenu import TodolistViewMenu
from src.modules.wiki.ModuleWiki import ModuleWiki


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
        # todo: add a reset embed_uuid somewhere here
        self.add_view(RegisterViewMenu())
        # self.add_view(TodolistViewMenu())

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


if __name__ == '__main__':
    load_dotenv()
    Oisol().run(os.getenv('DISCORD_TOKEN'), reconnect=True)
