import configparser
import discord
import os
from discord import app_commands
from discord.ext import commands
from src.utils.CsvHandler import CsvHandler
from src.modules.config.ConfigInterfaces import ModalConfig, ModalRegister, SelectLanguageView, ConfigViewMenu
from src.utils.oisol_enums import DataFilesPath, Language, Faction
from src.utils.resources import MODULES_CSV_KEYS


class ModuleConfig(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.csv_keys = MODULES_CSV_KEYS

    @staticmethod
    def display_current_conf(conf: configparser.ConfigParser) -> str:
        conf_msg_txt = ''

        print(conf.sections())
        for section in conf.sections():
            conf_msg_txt += f'{section}\n'
            conf_msg_txt += f'\t'

        return conf_msg_txt

    @app_commands.command(name='oisol_init', description='Command to set the default config (and reset)')
    async def oisol_init(self, interaction: discord.Interaction):
        print(f'> oisol_init command by {interaction.user.name} on {interaction.guild.name}')
        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild_id))

        # Create oisol and oisol/todolists directories
        os.makedirs(os.path.join(oisol_server_home_path), exist_ok=True)
        os.makedirs(os.path.join(oisol_server_home_path, 'todolists'), exist_ok=True)

        # Create oisol/*.csv files
        for datafile in [DataFilesPath.REGISTER, DataFilesPath.STOCKPILES]:
            if not os.path.isfile(os.path.join(oisol_server_home_path, datafile.value)):
                CsvHandler(self.csv_keys[datafile.name.lower()]).csv_try_create_file(
                    os.path.join(oisol_server_home_path, datafile.value)
                )

        # Create oisol/config.ini file with default config
        if not os.path.isfile(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value)):
            config = configparser.ConfigParser()
            config['default'] = {}
            config['default']['language'] = Language.EN.name

            config['register'] = {}
            config['register']['input'] = ''
            config['register']['output'] = ''
            config['register']['promoted_get_tag'] = 'False'
            config['register']['recruit_id'] = ''

            config['regiment'] = {}
            config['regiment']['faction'] = Faction.NEUTRAL.name
            config['regiment']['name'] = ''
            config['regiment']['tag'] = ''
            with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
                config.write(configfile)
        await interaction.response.send_message('> Default configuration has been set', ephemeral=True, delete_after=3)

    @app_commands.command(name='config')
    async def config(self, interaction: discord.Interaction):
        print(f'> config command by {interaction.user.name} on {interaction.guild.name}')
        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild_id))
        try:
            config = configparser.ConfigParser()
            config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        except FileNotFoundError:
            await interaction.response.send_message(
                '> The default config was never set, you can set it using </oisol_init:1253044649589997609>',
                ephemeral=True,
                delete_after=5
            )
            return
        config_view = ConfigViewMenu()
        await config_view.update_config_embed(interaction)
        await interaction.response.send_message(view=config_view, embed=config_view.embed)

    @app_commands.command(name='config-recruit', description='Set the recruit role of the regiment')
    async def config_recruit(self, interaction: discord.Interaction, recruit_role: discord.Role):
        print(f'> config command by {interaction.user.name} on {interaction.guild.name}')
        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild_id))
        try:
            config = configparser.ConfigParser()
            config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        except FileNotFoundError:
            await interaction.response.send_message(
                '> The default config was never set, you can set it using </oisol_init:1253044649589997609>',
                ephemeral=True,
                delete_after=5
            )
            return
        config['register']['recruit_id'] = str(recruit_role.id)
        with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
            config.write(configfile)
        await interaction.response.send_message(
            f'> The recruit role has been updated to {recruit_role.mention}',
            ephemeral=True,
            delete_after=3
        )
