import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from modules.config.ModuleConfig import ModuleConfig
from modules.registre.ModuleRegister import ModuleRegister
from modules.registre.RegisterViewMenu import RegisterViewMenu
from modules.single_commdands.ModuleSingleCommands import ModuleSingleCommands
from modules.stockpile_viewer.ModuleStockpile import ModuleStockpiles
from modules.todolist.ModuleTodolist import ModuleTodolist


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
        await self.add_cog(ModuleSingleCommands(self))

        try:
            synced = await self.tree.sync()
            print(f'Synced {len(synced)} command(s)')
        except Exception as e:
            print(e)

        print(f'Logged in as {self.user} (ID:{self.user.id})')

    async def setup_hook(self):
        self.add_view(RegisterViewMenu())


if __name__ == '__main__':
    load_dotenv()
    Oisol().run(os.getenv('DISCORD_TOKEN'), reconnect=True)
