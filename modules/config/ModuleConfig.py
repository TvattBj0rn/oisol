import configparser
import discord
import os
import termcolor
from discord import app_commands
from discord.ext import commands
from modules.stockpile_viewer import CsvHandlerStockpiles
from modules.config.ConfigInterfaces import ModalConfig, ModalRegister, SelectLanguageView
from modules.utils import DataFilesPath, Language, Faction, MODULES_CSV_KEYS


class ModuleConfig(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.csv_keys = MODULES_CSV_KEYS

    @app_commands.command(name='oisol_init', description='Command to do when the bot first arrives on the server')
    async def oisol_init(self, interaction: discord.Interaction):
        """
        Generate the files & directories used by the various OISOL commands.
        """
        termcolor.colored(f'> oisol_init command by {interaction.user.name} on {interaction.guild.name}', 'blue')
        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild.id))

        os.makedirs(os.path.join(oisol_server_home_path), exist_ok=True)
        os.makedirs(os.path.join(oisol_server_home_path, 'todolists'), exist_ok=True)

        for datafile in [DataFilesPath.REGISTER, DataFilesPath.STOCKPILES]:
            if not os.path.isfile(os.path.join(oisol_server_home_path, datafile.value)):
                CsvHandlerStockpiles.CsvHandlerStockpiles(self.csv_keys[datafile.name.lower()]).csv_try_create_file(
                    os.path.join(oisol_server_home_path, datafile.value)
                )

        if not os.path.isfile(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value)):
            config = configparser.ConfigParser()
            config['default'] = {}
            config['regiment'] = {}
            config['default']['language'] = Language.EN.name
            config['regiment']['faction'] = Faction.NEUTRAL.name
            with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
                config.write(configfile)
        await interaction.response.send_message('> Les fichiers ont bien été générés', ephemeral=True)

    @app_commands.command(name='config_regiment')
    async def config_regiment(self, interaction: discord.Interaction, faction: Faction):
        print(f'> config_regiment command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.send_modal(ModalConfig(faction.name))

    @app_commands.command(name='config_language')
    async def config_language(self, interaction: discord.Interaction):
        print(f'> config_language command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.send_message(view=SelectLanguageView(), ephemeral=True)

    @app_commands.command(name='config_register')
    async def config_register(self, interaction: discord.Interaction, promoted_get_tag: bool):
        print(f'> config_register command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.send_modal(ModalRegister(promoted_get_tag))
