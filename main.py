import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


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
    await bot.load_extension('modules.registre.entrypoint_registre')
    await bot.load_extension('modules.stockpile_viewer.entrypoint_stockpile_viewer')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

    print(f'Logged in as {bot.user} (ID:{bot.user.id})')


if __name__ == '__main__':
    load_dotenv()
    bot.run(os.getenv('DISCORD_TOKEN'), reconnect=True)
