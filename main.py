import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from modules.registre.entrypoint_registre import ModuleRegister
from modules.config.entrypoint_config import ModuleConfig
from modules.stockpile_viewer.entrypoint_stockpile_viewer import ModuleStockpiles
from modules.todolist.entrypoint_todolist import ModuleTodolist



# Bot settings
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix='$',
    intents=intents,
    help_command=commands.DefaultHelpCommand(no_category='Commands')
)


@bot.event
async def on_ready():
    await bot.add_cog(ModuleConfig(bot))
    await bot.add_cog(ModuleStockpiles(bot))
    await bot.add_cog(ModuleRegister(bot))
    await bot.add_cog(ModuleTodolist(bot))

    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

    print(f'Logged in as {bot.user} (ID:{bot.user.id})')


if __name__ == '__main__':
    load_dotenv()
    bot.run(os.getenv('DISCORD_TOKEN'), reconnect=True)
