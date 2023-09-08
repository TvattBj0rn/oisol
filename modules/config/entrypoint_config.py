import configparser
import discord
import os
from discord import app_commands
from discord.ext import commands
from modules.config import ConfigEnums
from modules.stockpile_viewer import CsvHandlerStockpiles
from modules.registre import CsvHandlerRegistre
from modules.utils import path


class ModuleConfig(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.csv_keys = {
            'stockpiles': ['region', 'subregion', 'code', 'name', 'type'],
            'register': ['member', 'timer']
        }

    @app_commands.command(name='oisol_init', description='Command to do when the bot first arrives on the server')
    async def oisol_init(self, interaction: discord.Interaction):
        server_id = interaction.guild.id

        os.makedirs(f'{path.get_root_path()}{str(server_id)}', exist_ok=True)
        os.makedirs(f'{path.get_root_path()}{str(server_id)}/todolists/', exist_ok=True)

        if not os.path.isfile(f'{path.get_root_path()}{server_id}/{path.DataFilesPath.STOCKPILES.value}'):
            CsvHandlerStockpiles.CsvHandlerStockpiles(self.csv_keys['stockpiles']).csv_try_create_file(
                path.generate_path(server_id, path.DataFilesPath.STOCKPILES.value))

        if not os.path.isfile(f'{path.get_root_path()}{server_id}/{path.DataFilesPath.REGISTER.value}'):
            CsvHandlerRegistre.CsvHandlerRegister(self.csv_keys['register']).csv_try_create_file(
                path.generate_path(server_id, path.DataFilesPath.REGISTER.value))

        ## Default Config
        if not os.path.isfile(f'{path.get_root_path()}{server_id}/{path.DataFilesPath.CONFIG.value}'):
            config = configparser.ConfigParser()
            config['default'] = {}
            config['default']['language'] = ConfigEnums.Languages.FR.value
            config['default']['faction'] = ConfigEnums.Faction.NEUTRAL.value
            with open(path.generate_path(server_id, path.DataFilesPath.CONFIG.value), 'w') as configfile:
                config.write(configfile)


        await interaction.response.send_message('> Les fichiers de serveur ont bien été installés', ephemeral=True)