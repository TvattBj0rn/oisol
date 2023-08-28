import os
import sys

import discord
import discord.utils
import requests
from discord.ext import commands, tasks


class APILector(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.get_war_status.start()
        self.get_war_stats_report.start()


    @tasks.loop(hours=1)
    async def get_war_stats_report(self):
        response = requests.get('https://war-service-live.foxholeservices.com/api/worldconquest/maps')
        enlistments_total = 0
        warden_casualties = 0
        colonial_casualties = 0
        message_id = 'War Stats'

        for region in response.json():
            response = requests.get(f'https://war-service-live.foxholeservices.com/api/worldconquest/warReport/{region}')
            enlistments_total += response.json()['totalEnlistments']
            warden_casualties += response.json()['wardenCasualties']
            colonial_casualties += response.json()['colonialCasualties']
        war_stats_embed = discord.Embed(title='Statistiques')
        war_stats_embed.set_footer(text=message_id)
        war_stats_embed.add_field(
            name=f'<:soldiersupplies:1077742140211343371> **|** Enrôlements (Wardens/Colonials): {enlistments_total}',
            value='',
            inline=False
        )
        war_stats_embed.add_field(
            name=f'<:warden_emblem:1145860117032603719> **|** Pertes Warden: {warden_casualties}',
            value='',
            inline=False
        )
        war_stats_embed.add_field(
            name=f'<:colonial_emblem:1145860105515040859> **|** Pertes Coloniales: {colonial_casualties}',
            value='',
            inline=False
        )
        await send_data_to_discord(embed=war_stats_embed, bot=self.bot, message_id=message_id, images=[])


    @tasks.loop(minutes=5)
    async def get_war_status(self):
        response = requests.get('https://war-service-live.foxholeservices.com/api/worldconquest/war')
        if response.status_code != 200:
            print(response.status_code, file=sys.stderr)
            return
        message_id = 'War Status'
        message_images = []
        war_data = response.json()

        war_status_embed = discord.Embed(title=f"Guerre {war_data['warNumber']}")
        war_status_embed.set_footer(text=message_id)

        message_images.append(discord.File('modules/api_lector/images/emblems/foxhole_emblem.jpg'))
        war_status_embed.set_thumbnail(url='attachment://foxhole_emblem.jpg')

        if war_data['winner'] == 'NONE':
            war_status_embed.add_field(
                name='Début de Guerre',
                value=f"<t:{int(war_data['conquestStartTime'] / 1000)}:d> **|** <t:{int(war_data['conquestStartTime'] / 1000)}:R>"
            )
        else:
            war_status_embed.add_field(
                name='Fin de la guerre',
                value=f"<t:{int(war_data['conquestEndTime'] / 1000)}:d> **|** <t:{int(war_data['conquestEndTime'] / 1000)}:R>"
            )
            war_status_embed.add_field(
                name=f"Victoire {war_data['winner'].title()} !",
                value=''
            )
            message_images.append(discord.File(f"modules/api_lector/images/emblems/{war_data['winner'].lower()}_emblem.png"))
            war_status_embed.set_image(url=f"attachment://{war_data['winner'].lower()}_emblem.jpg")

        await send_data_to_discord(embed=war_status_embed, bot=self.bot, message_id=message_id, images=message_images)


async def send_data_to_discord(embed: discord.Embed, bot: commands.Bot, message_id: str, images: [discord.File]):
    for server in bot.guilds:
        for channel in server.channels:
            if channel.name == '⚔－war-api-viewer':
                async for message in channel.history():
                    if not message.embeds:
                        continue
                    message_embed = discord.Embed.to_dict(message.embeds[0])
                    if message_embed['footer']['text'] == message_id:
                        await message.edit(embed=embed, attachments=images)
                        return
                await channel.send(embed=embed, files=images)

