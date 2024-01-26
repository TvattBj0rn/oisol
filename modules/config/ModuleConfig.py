import configparser
import discord
import os
import pathlib
from discord import app_commands
from discord.ext import commands
from modules.config import ConfigEnums
from modules.stockpile_viewer import CsvHandlerStockpiles
from modules.utils.DataFiles import DataFilesPath


class ModuleConfig(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.csv_keys = {
            'stockpiles': ['region', 'subregion', 'code', 'name', 'type'],
            'register': ['member', 'timer']
        }

    @app_commands.command(name='oisol_init', description='Command to do when the bot first arrives on the server')
    async def oisol_init(self, interaction: discord.Interaction):
        """
        Generate the files & directories used by the various OISOL commands.
        """

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
            config['default']['language'] = ConfigEnums.Languages.FR.value
            config['default']['faction'] = ConfigEnums.Faction.NEUTRAL.value
            with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w') as configfile:
                config.write(configfile)

        await interaction.response.send_message('> Les fichiers de serveur ont bien été installés', ephemeral=True)
