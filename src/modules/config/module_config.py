from __future__ import annotations

import configparser
import os
import sqlite3
from configparser import ConfigParser
from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.ext import commands

from src.utils import (
    OISOL_HOME_PATH,
    OISOL_LOGGER,
    DataFilesPath,
    Faction,
    InterfacesTypes,
    repair_default_config_dict,
)

from .config_interfaces import ConfigViewMenu, SelectLanguageView

if TYPE_CHECKING:
    from main import Oisol


class ModuleConfig(commands.Cog):
    def __init__(self, bot: Oisol):
        self.bot = bot

    @staticmethod
    def __add_missing_sections(guild_config: ConfigParser) -> None:
        """
        Ensures all required section of the .ini configfile exist
        :param guild_config: config object to be checked
        """
        required_sections = {'default', 'register', 'regiment', 'stockpile', 'logging'}

        if missing_sections := required_sections - set(guild_config.sections()):
            for missing_section in missing_sections:
                guild_config.add_section(missing_section)

    def _regiment_config_generic(self, guild_id: int, section: str, option: str, value: str) -> None:
        # Init path to file / Config object
        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{guild_id}.ini')
        self.__add_missing_sections(config)

        config.set(section, option, value)

        # Write updated config to file
        with open(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{guild_id}.ini', 'w', newline='') as configfile:
            config.write(configfile)

    @app_commands.command(
        name='repair-oisol',
        description=app_commands.locale_str('Command to add missing config, with possibility to reset the existing configuration'),
    )
    async def repair_oisol_config(self, interaction: discord.Interaction, force_reset: bool = False) -> None:
        OISOL_LOGGER.command(f'repair-oisol command by {interaction.user.name} on {interaction.guild.name}')

        # Create configs directory
        os.makedirs(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value, exist_ok=True)

        # Create oisol/config.ini file with default config
        if not os.path.isfile(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini') or force_reset:
            config = repair_default_config_dict()
        else:
            current_config = configparser.ConfigParser()
            current_config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')
            config = repair_default_config_dict(current_config)

        with open(
            OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini',
            'w',
            newline='',
        ) as configfile:
            config.write(configfile)
        await interaction.response.send_message('> Configuration has been updated', ephemeral=True, delete_after=5)

    @app_commands.command(
        name='config-display',
        description=app_commands.locale_str('Display the current server configuration'),
    )
    async def config(self, interaction: discord.Interaction) -> None:
        OISOL_LOGGER.command(f'config-display command by {interaction.user.name} on {interaction.guild.name}')

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

    @app_commands.command(
        name='config-register',
        description=app_commands.locale_str('Set the recruit discord role, icons for recruits & promoted recruits'),
    )
    async def config_register(
            self,
            interaction: discord.Interaction,
            recruit_role: discord.Role | None = None,
            recruit_symbol: str | None = None,
            promoted_recruit_symbol: str | None = None,
            promotion_gives_symbol: bool | None = None,
    ) -> None:
        OISOL_LOGGER.command(f'config-register command by {interaction.user.name} on {interaction.guild.name}')
        if recruit_role is None and recruit_symbol is None and promoted_recruit_symbol is None and promotion_gives_symbol is None:
            await interaction.response.send_message(
                '> No changes were made because no option was given',
                ephemeral=True,
                delete_after=5,
            )
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

        with open(
            OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini',
            'w',
            newline='',
        ) as configfile:
            config.write(configfile)
        await interaction.response.send_message('> The register config was updated', ephemeral=True, delete_after=5)

    @app_commands.command(
        name='config-language',
        description=app_commands.locale_str('Set the language the bot uses for the server'),
    )
    async def config_language(self, interaction: discord.Interaction) -> None:
        OISOL_LOGGER.command(f'config-language command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.send_message(
            view=SelectLanguageView(self.bot.app_emojis_dict),
            ephemeral=True,
        )

    @app_commands.command(
        name='config-name',
        description=app_commands.locale_str('Set the name of the group using the bot'),
    )
    async def config_name(self, interaction: discord.Interaction, name: str) -> None:
        OISOL_LOGGER.command(f'config-name command by {interaction.user.name} on {interaction.guild.name}')
        self._regiment_config_generic(interaction.guild_id, 'regiment', 'name', name)
        await interaction.response.send_message('> Name was updated', ephemeral=True, delete_after=5)

    @app_commands.command(
        name='config-tag',
        description=app_commands.locale_str('Set the tag of the regiment group using the bot'),
    )
    async def config_tag(self, interaction: discord.Interaction, tag: str) -> None:
        OISOL_LOGGER.command(f'config-tag command by {interaction.user.name} on {interaction.guild.name}')
        self._regiment_config_generic(interaction.guild_id, 'regiment', 'tag', tag)
        await interaction.response.send_message('> Tag was updated', ephemeral=True, delete_after=5)

    @app_commands.command(
        name='config-shard',
        description=app_commands.locale_str('Set the shard of the group (default is Able)'),
    )
    async def config_shard(self, interaction: discord.Interaction, shard_name: str) -> None:
        OISOL_LOGGER.command(f'config-shard command by {interaction.user.name} on {interaction.guild.name}')

        # Case where the user still manually input the shard name, ensure conformity with bot's set
        shard_name = shard_name.upper()

        if shard_name not in self.bot.connected_shards:
            await interaction.response.send_message(
                '> The provided shard does not exist or is currently not live',
                ephemeral=True,
                delete_after=5,
            )
            return

        self._regiment_config_generic(interaction.guild_id, 'default', 'shard', shard_name)
        await interaction.response.send_message('> Shard was updated', ephemeral=True, delete_after=5)

    @app_commands.command(
        name='config-faction',
        description=app_commands.locale_str('Set the faction of the group using the bot, this will impact the color of the stockpile interface'),
    )
    async def config_faction(self, interaction: discord.Interaction, faction: Faction) -> None:
        OISOL_LOGGER.command(f'config-faction command by {interaction.user.name} on {interaction.guild.name}')
        self._regiment_config_generic(interaction.guild_id, 'regiment', 'faction', faction.name)

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            stockpile_interfaces = conn.cursor().execute(
                'SELECT GroupId, ChannelId, MessageId, AssociationId FROM AllInterfacesReferences WHERE GroupId == ? AND InterfaceType == ?',
                (interaction.guild_id, InterfacesTypes.STOCKPILE.value),
            ).fetchall()
        for _, channel_id, message_id, _ in stockpile_interfaces:
            channel = self.bot.get_channel(int(channel_id))
            message = await channel.fetch_message(int(message_id))

            if message.embeds:
                # It is guaranteed that there is only a single embed
                embed_dict = message.embeds[0].to_dict()
                embed_dict['color'] = faction.value
                await message.edit(embed=discord.Embed.from_dict(embed_dict))

        await interaction.response.send_message('> Faction was updated', ephemeral=True, delete_after=5)

    @app_commands.command(
        name='config-set-logging-channel',
        description=app_commands.locale_str('Set the logging channel'),
    )
    async def config_log_channel(self, interaction: discord.Interaction, channel: discord.TextChannel) -> None:
        OISOL_LOGGER.command(f'config-set-logging-channel command by {interaction.user.name} on {interaction.guild.name}')
        bot_as_member = interaction.guild.get_member(self.bot.application_id)

        # Ensure the bot can send message in provided channel
        if not channel.permissions_for(bot_as_member).send_messages:
            await interaction.response.send_message(
                f'> The bot does not have permission to send messages in {channel.name}',
                ephemeral=True,
                delete_after=5,
            )
            return

        self._regiment_config_generic(interaction.guild_id, 'logging', 'channel', str(channel.id))

        await interaction.response.send_message(
            f'> Logging channel {channel.mention} was properly set',
            ephemeral=True,
            delete_after=5,
        )

    @app_commands.command(
        name='config-unset-logging-channel',
        description=app_commands.locale_str('Unbind existing logging channel'),
    )
    async def unbind_log_channel(self, interaction: discord.Interaction) -> None:
        OISOL_LOGGER.command(f'config-unset-logging-channel command by {interaction.user.name} on {interaction.guild.name}')
        # todo: only need to check for existing channel in config then try it

    @config_shard.autocomplete('shard_name')
    async def available_shard_autocomplete(
        self,
        _interaction:
        discord.Interaction,
        _current: str,
    ) -> list[app_commands.Choice]:
        return [app_commands.Choice(name=shard_name, value=shard_name) for shard_name in self.bot.connected_shards]
