import configparser
import discord
import os
from discord import app_commands
from discord.ext import commands
from src.utils.oisol_enums import DataFilesPath
from src.utils.resources import MODULES_CSV_KEYS
from src.utils.CsvHandler import CsvHandler
from src.modules.registre.RegisterViewMenu import RegisterViewMenu


class ModuleRegister(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.CsvHandler = CsvHandler(MODULES_CSV_KEYS['register'])

    @app_commands.command(name='register-view', description='Command to display the current list of recruit with the date the got the recruit role')
    async def register_view(self, interaction: discord.Interaction):
        print(f'> register-view command by {interaction.user.name} on {interaction.guild.name}')
        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild_id))
        config = configparser.ConfigParser()
        config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        if not config.has_section('register'):
            config.add_section('register')
        config.set('register', 'channel', str(interaction.channel_id))

        register_view_instance = RegisterViewMenu()
        register_view_instance.refresh_register_embed(str(interaction.guild_id))

        await interaction.response.send_message(view=register_view_instance, embed=register_view_instance.embeds[0])

        sent_msg = await interaction.original_response()

        config.set('register', 'message_id', str(sent_msg.id))
        with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
            config.write(configfile)
