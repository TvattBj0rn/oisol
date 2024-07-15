import configparser
import discord
import os
import pathlib
import time
from discord import app_commands
from discord.ext import commands, tasks
from src.utils.functions import update_discord_interface, safeguarded_nickname
from src.utils.oisol_enums import DataFilesPath, Modules
from src.utils.resources import MODULES_CSV_KEYS
from src.utils.CsvHandler import CsvHandler
from src.modules.registre.RegisterViewMenu import RegisterViewMenu


class ModuleRegister(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.CsvHandler = CsvHandler(MODULES_CSV_KEYS['register'])

    @app_commands.command(name='register-view')
    async def register_view(self, interaction: discord.Interaction):
        print(f'> register-view command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.defer()

        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild.id))
        config = configparser.ConfigParser()
        config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        try:
            config['register']['channel'] = str(interaction.channel_id)
        except KeyError:
            await interaction.followup.send(
                '> The default config was never set, you can set it using </oisol_init:1253044649589997609>',
                ephemeral=True,
                delete_after=5
            )
            return

        register_view_instance = RegisterViewMenu()
        register_view_instance.refresh_register_embed(str(interaction.guild.id))
        await interaction.followup.send(view=register_view_instance, embed=register_view_instance.embeds[0])
        sent_msg = await interaction.original_response()
        config['register']['message_id'] = str(sent_msg.id)
        with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
            config.write(configfile)
