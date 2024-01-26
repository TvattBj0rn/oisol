import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from modules.registre.ModuleRegister import ModuleRegister
from modules.config.ModuleConfig import ModuleConfig
from modules.stockpile_viewer.entrypoint_stockpile_viewer import ModuleStockpiles
from modules.todolist.entrypoint_todolist import ModuleTodolist
from modules.single_commdands.ModuleSingleCommands import ModuleSingleCommands


# Bot settings
# intents = discord.Intents.default()
# intents.message_content = True
# intents.members = True
#
# bot = commands.Bot(
#     command_prefix='$',
#     intents=intents,
#     help_command=commands.DefaultHelpCommand(no_category='Commands')
# )
#
#
# @bot.event
# async def on_ready():
#     await bot.add_cog(ModuleConfig(bot))
#     await bot.add_cog(ModuleStockpiles(bot))
#     await bot.add_cog(ModuleRegister(bot))
#     await bot.add_cog(ModuleTodolist(bot))
#     await bot.add_cog(ModuleSingleCommands(bot))
#
#     try:
#         synced = await bot.tree.sync()
#         print(f'Synced {len(synced)} command(s)')
#     except Exception as e:
#         print(e)
#
#     print(f'Logged in as {bot.user} (ID:{bot.user.id})')


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


if __name__ == '__main__':
    load_dotenv()
    # bot.run(os.getenv('DISCORD_TOKEN'), reconnect=True)
    Oisol().run(os.getenv('DISCORD_TOKEN'), reconnect=True)
