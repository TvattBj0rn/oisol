from __future__ import annotations

import configparser
import os
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.modules.stockpile_viewer import ModuleStockpiles
from src.utils import (
    OISOL_HOME_PATH,
    DataFilesPath,
    EmbedIds,
    Faction,
    Shard,
    repair_default_config_dict,
    update_discord_interface,
)

from .config_interfaces import ConfigViewMenu, SelectLanguageView

if TYPE_CHECKING:
    from main import Oisol


class ModuleConfig(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot

    @app_commands.command(name='repair-oisol', description='Command to add missing config, with possibility to reset to default')
    async def repair_oisol_config(self, interaction: discord.Interaction, force_reset: bool = False) -> None:
        self.bot.logger.command(f'repair-oisol command by {interaction.user.name} on {interaction.guild.name}')

        # Create configs directory
        os.makedirs(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value, exist_ok=True)

        # Create oisol/config.ini file with default config
        if not os.path.isfile(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini') or force_reset:
            config = repair_default_config_dict()
        else:
            current_config = configparser.ConfigParser()
            current_config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')
            config = repair_default_config_dict(current_config)

        with open(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini', 'w', newline='') as configfile:
            config.write(configfile)
        await interaction.response.send_message('> Configuration has been updated', ephemeral=True, delete_after=5)

    @app_commands.command(name='config-display', description='Display current config for the server')
    async def config(self, interaction: discord.Interaction) -> None:
        self.bot.logger.command(f'config-display command by {interaction.user.name} on {interaction.guild.name}')

        config = configparser.ConfigParser()
        if not config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini'):
            await interaction.response.send_message(
                '> The default config was never set',
                ephemeral=True,
                delete_after=5,
            )
            return
        config_view = ConfigViewMenu()
        await config_view.update_config_embed(interaction)
        await interaction.response.send_message(view=config_view, embed=config_view.embed)

    @app_commands.command(name='config-register', description='Set the recruit discord role, icons for recruit & promoted recruit and the option to not change ')
    async def config_register(self, interaction: discord.Interaction, recruit_role: discord.Role | None = None, recruit_symbol: str | None = None, promoted_recruit_symbol: str | None = None, promotion_gives_symbol: bool | None = None) -> None:
        self.bot.logger.command(f'config-register command by {interaction.user.name} on {interaction.guild.name}')
        if recruit_role is None and recruit_symbol is None and promoted_recruit_symbol is None and promotion_gives_symbol is None:
            await interaction.response.send_message('> No changes were made because no option was given', ephemeral=True, delete_after=5)
            return

        config = configparser.ConfigParser()
        if not config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini'):
            await interaction.response.send_message(
                '> The default config was never set',
                ephemeral=True,
                delete_after=5,
            )
            return
        if recruit_role is not None:
            config.set('register', 'recruit_id', str(recruit_role.id))
        if recruit_symbol is not None:
            config.set('register', 'input', recruit_symbol)
        if promoted_recruit_symbol is not None:
            config.set('register', 'output', promoted_recruit_symbol)
        if promotion_gives_symbol is not None:
            config.set('register', 'promoted_get_tag', str(promotion_gives_symbol))

        with open(self.bot.home_path / str(interaction.guild_id) / DataFilesPath.CONFIG.value, 'w', newline='') as configfile:
            config.write(configfile)
        await interaction.response.send_message('> The register config was updated', ephemeral=True, delete_after=5)

    @app_commands.command(name='config-language', description='Set the language the bot uses for the server')
    async def config_language(self, interaction: discord.Interaction) -> None:
        self.bot.logger.command(f'config-language command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.send_message(
            view=SelectLanguageView(),
            ephemeral=True,
        )

    @staticmethod
    def _regiment_config_generic(guild_id: int, **kwargs: str) -> None:
        # Init path to file / Config object
        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{guild_id}.ini')
        if not config.has_section('regiment'):
            config.add_section('regiment')

        # There should be only one item inside **kwargs when this method is called, so only the first item is retrieved
        param_name, param_value = next(iter(kwargs.items()))
        if param_name == 'shard':
            config.set('default', 'shard', param_value)
        else:
            config.set('regiment', param_name, param_value)

        # Write updated config to file
        with open(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{guild_id}.ini', 'w', newline='') as configfile:
            config.write(configfile)

    @app_commands.command(name='config-name', description='Set the name of the group using the bot')
    async def config_name(self, interaction: discord.Interaction, name: str) -> None:
        self.bot.logger.command(f'config-name command by {interaction.user.name} on {interaction.guild.name}')
        self._regiment_config_generic(interaction.guild_id, name=name)
        await interaction.response.send_message('> Name was updated', ephemeral=True, delete_after=5)

    @app_commands.command(name='config-tag', description='Set the tag of the regiment group using the bot')
    async def config_tag(self, interaction: discord.Interaction, tag: str) -> None:
        self.bot.logger.command(f'config-tag command by {interaction.user.name} on {interaction.guild.name}')
        self._regiment_config_generic(interaction.guild_id, tag=tag)
        await interaction.response.send_message('> Tag was updated', ephemeral=True, delete_after=5)

    @app_commands.command(name='config-shard', description='Set the shard of the group')
    async def config_shard(self, interaction: discord.Interaction, shard: Shard) -> None:
        self.bot.logger.command(f'config-shard command by {interaction.user.name} on {interaction.guild.name}')
        self._regiment_config_generic(interaction.guild_id, shard=shard.name)
        await interaction.response.send_message('> Shard was updated', ephemeral=True, delete_after=5)

    @app_commands.command(name='config-faction', description='Set the faction of the group using the bot')
    async def config_faction(self, interaction: discord.Interaction, faction: Faction) -> None:
        self.bot.logger.command(f'config-faction command by {interaction.user.name} on {interaction.guild.name}')
        self._regiment_config_generic(interaction.guild_id, faction=faction.name)

        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')
        if config.has_option('stockpile', 'channel'):
            stockpile_interface_exists = False
            channel = interaction.guild.get_channel(int(config['stockpile']['channel']))
            async for message in channel.history():
                if not message.embeds:
                    continue
                message_embed = discord.Embed.to_dict(message.embeds[0])
                if 'footer' in message_embed and message_embed['footer']['text'] == EmbedIds.STOCKPILES_VIEW.value:
                    stockpile_interface_exists = True
            if stockpile_interface_exists:
                await update_discord_interface(
                    interaction,
                    EmbedIds.STOCKPILES_VIEW.value,
                    embed=ModuleStockpiles.refresh_stockpile_interface(self.bot, interaction.guild_id),
                )
        await interaction.response.send_message('> Faction was updated', ephemeral=True, delete_after=5)
