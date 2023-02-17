import discord
import discord_token
from discord.ext import commands


# Bot settings
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$',
                   intents=intents,
                   help_command=commands.DefaultHelpCommand(no_category='Commands')
                   )


@bot.event
async def on_ready():
    await bot.load_extension('modules.vehicles_stats.fstats')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)

    print(f'Logged in as {bot.user} (ID:{bot.user.id})')


if __name__ == '__main__':
    bot.run(discord_token.token, reconnect=True)
