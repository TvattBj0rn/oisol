import configparser
import discord
import os
from modules.utils import DataFilesPath


async def send_data_to_discord(embed: discord.Embed, interaction: discord.Interaction, message_id: str):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.join('/', 'oisol', str(interaction.guild.id)), DataFilesPath.CONFIG.value))
    channel = interaction.guild.get_channel(int(config['stockpile']['channel']))

    async for message in channel.history():
        if not message.embeds:
            continue
        message_embed = discord.Embed.to_dict(message.embeds[0])
        if message_embed['footer']['text'] == message_id:
            await message.edit(embed=embed)
            return
        else:
            print(message_embed['footer']['text'], message_id)
    await channel.send(embed=embed)
