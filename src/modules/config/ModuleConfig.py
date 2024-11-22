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
from src.modules.config.ConfigInterfaces import SelectLanguageView, ConfigViewMenu
from src.utils.oisol_enums import DataFilesPath, Language, Faction
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

    @app_commands.command(name='config', description='Display current config for the server')
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

    @app_commands.command(name='config-language', description='Set the language the bot uses for the server')
    async def config_language(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            view=SelectLanguageView(),
            ephemeral=True
        )

    @staticmethod
    def regiment_config_generic(guild_id: int, **kwargs):
        # Init path to file / Config object
        oisol_server_home_path = os.path.join('/', 'oisol', str(guild_id))
        config = configparser.ConfigParser()
        config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        if not config.has_section('regiment'):
            config['regiment'] = {}

        # For now, there can be only one item inside **kwargs when this method is called, so the first item is retrived
        data_to_write = next(iter(kwargs.items()))
        config['regiment'][data_to_write[0]] = data_to_write[1]

        # Write updated config to file
        with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
            config.write(configfile)

    @app_commands.command(name='config-name', description='Set the name of the group using the bot')
    async def config_name(self, interaction: discord.Interaction, name: str):
        self.regiment_config_generic(interaction.guild_id, name=name)
        await interaction.response.send_message('> Name was updated', ephemeral=True, delete_after=5)

    @app_commands.command(name='config-tag', description='Set the tag of the regiment group using the bot')
    async def config_tag(self, interaction: discord.Interaction, tag: str):
        self.regiment_config_generic(interaction.guild_id, tag=tag)
        await interaction.response.send_message('> Tag was updated', ephemeral=True, delete_after=5)

    @app_commands.command(name='config-faction', description='Set the faction of the regiment group using the bot')
    async def config_faction(self, interaction: discord.Interaction, faction: Faction):
        self.regiment_config_generic(interaction.guild_id, faction=faction.name)
        await interaction.response.send_message('> Faction was updated', ephemeral=True, delete_after=5)
