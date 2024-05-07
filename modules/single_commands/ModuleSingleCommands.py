import discord
from discord import app_commands
from discord.ext import commands


class ModuleSingleCommands(commands.Cog):
    def __init__(self, bot):
        self.oisol = bot

    @app_commands.command(name='oisol_ping', description='check if the bot is running as expected')
    async def oisol_ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong!")
