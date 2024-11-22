import configparser
import discord
import os
from discord import app_commands
from discord.ext import commands
from typing import Optional
from src.utils.CsvHandler import CsvHandler
from src.modules.config.ConfigInterfaces import ConfigViewMenu
from src.utils.functions import repair_default_config_dict
from src.utils.oisol_enums import DataFilesPath
from src.utils.resources import MODULES_CSV_KEYS


class ModuleConfig(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.csv_keys = MODULES_CSV_KEYS

    @app_commands.command(name='repair-oisol', description='Command to add missing config, with possibility to reset to default')
    async def repair_oisol_config(self, interaction: discord.Interaction, force_reset: Optional[bool]):
        print(f'> repair-oisol command by {interaction.user.name} on {interaction.guild.name}')
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
        if not os.path.isfile(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value)) or force_reset:
            config = repair_default_config_dict()
        else:
            current_config = configparser.ConfigParser()
            current_config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
            config = repair_default_config_dict(current_config)

        with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
            config.write(configfile)
        await interaction.response.send_message('> Configuration has been updated', ephemeral=True, delete_after=5)

    @app_commands.command(name='config')
    async def config(self, interaction: discord.Interaction):
        print(f'> config command by {interaction.user.name} on {interaction.guild.name}')
        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild_id))
        try:
            config = configparser.ConfigParser()
            config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        except FileNotFoundError:
            await interaction.response.send_message(
                '> The default config was never set',
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
                '> The default config was never set',
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
            delete_after=5
        )
