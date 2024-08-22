import configparser
import discord
import json
import os
from src.utils.oisol_enums import DataFilesPath
from src.modules.registre.RegisterViewMenu import RegisterViewMenu


async def update_discord_interface(
        interaction: discord.Interaction,
        message_id: str,
        view: RegisterViewMenu = None,
        embed: discord.Embed = None
) -> None:
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.join('/', 'oisol', str(interaction.guild.id)), DataFilesPath.CONFIG.value))
    channel = interaction.guild.get_channel(int(config['register' if view else 'stockpile']['channel']))

    async for message in channel.history():
        if not message.embeds:
            continue
        message_embed = discord.Embed.to_dict(message.embeds[0])
        if 'footer' in message_embed.keys() and message_embed['footer']['text'] == message_id:
            await message.edit(view=view, embed=view.get_current_embed()) if view else await message.edit(embed=embed)
            return
        else:
            print(message_embed['footer']['text'], message_id)
    await channel.send(view=view) if view else await channel.send(embed=embed)


def safeguarded_nickname(nickname: str) -> str:
    """
    Function required as discord does not allow for nicknames longer than 32 characters.
    :param nickname: wanted name
    :return: nickname equal or shortened to 32 chars
    """
    return nickname[:32 - len(nickname)] if len(nickname) > 32 else nickname


def load_json_file(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def update_json_file(file_path: str, new_data: dict) -> None:
    with open(file_path, 'w') as file:
        json.dump(new_data, file)
