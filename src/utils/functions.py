import configparser
import os
from configparser import ConfigParser

import discord

from .oisol_enums import DataFilesPath, Faction, Language


async def update_discord_interface(
        interaction: discord.Interaction,
        message_id: str,
        embed: discord.Embed = None
) -> None:
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.join('/', 'oisol', str(interaction.guild.id)), DataFilesPath.CONFIG.value))

    if config.has_option('stockpile', 'channel'):
        channel = interaction.guild.get_channel(int(config['stockpile']['channel']))
    else:
        # Edge case where oisol was not setup on guild but command /stockpile-create called
        # -> Case where the interface does not exist
        return

    async for message in channel.history():
        if not message.embeds:
            continue
        message_embed = discord.Embed.to_dict(message.embeds[0])
        if 'footer' in message_embed and message_embed['footer']['text'] == message_id:
            await message.edit(embed=embed)
            return
    await channel.send(embed=embed)


def safeguarded_nickname(nickname: str) -> str:
    """
    Function required as discord does not allow for nicknames longer than 32 characters.
    :param nickname: wanted name
    :return: nickname equal or shortened to 32 chars
    """
    return nickname[:32 - len(nickname)] if len(nickname) > 32 else nickname


def repair_default_config_dict(current_config: ConfigParser = None) -> ConfigParser:
    """
    Function that updates the configuration of a given config file by completing the missing values with the expected
    default values. If not config is passed as parameter, the function will return the default config file.
    :param current_config: Optional current config file to update.
    :return: update default config file.
    """
    final_config = configparser.ConfigParser()

    section_name = 'default'
    final_config.add_section(section_name)
    final_config.set(section_name, 'language', Language.EN.name if not current_config or not current_config.has_option(section_name, 'language') else current_config.get(section_name, 'language'))

    section_name = 'register'
    final_config.add_section(section_name)
    final_config.set(section_name, 'input', '' if not current_config or not current_config.has_option(section_name, 'input') else current_config.get(section_name, 'input'))
    final_config.set(section_name, 'output', '' if not current_config or not current_config.has_option(section_name, 'output') else current_config.get(section_name, 'output'))
    final_config.set(section_name, 'promoted_get_tag', 'False' if not current_config or not current_config.has_option(section_name, 'promoted_get_tag') else current_config.get(section_name, 'promoted_get_tag'))
    final_config.set(section_name, 'recruit_id', '' if not current_config or not current_config.has_option(section_name, 'recruit_id') else current_config.get(section_name, 'recruit_id'))

    section_name = 'regiment'
    final_config.add_section(section_name)
    final_config.set(section_name, 'faction', Faction.NEUTRAL.name if not current_config or not current_config.has_option(section_name, 'faction') else current_config.get(section_name, 'faction'))
    final_config.set(section_name, 'name', '' if not current_config or not current_config.has_option(section_name, 'name') else current_config.get(section_name, 'name'))
    final_config.set(section_name, 'tag', '' if not current_config or not current_config.has_option(section_name, 'tag') else current_config.get(section_name, 'tag'))

    return final_config
