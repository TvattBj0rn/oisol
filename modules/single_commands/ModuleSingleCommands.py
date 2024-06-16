import discord
from discord import app_commands
from discord.ext import commands


class ModuleSingleCommands(commands.Cog):
    def __init__(self, bot):
        self.oisol = bot
