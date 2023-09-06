import discord


async def send_data_to_discord(embed: discord.Embed, interaction: discord.Interaction, message_id: str, images: [discord.File]):
    for channel in interaction.guild.channels:
        if channel.name == '📦－stockages': ## Add possibility to change channel via config file (into the init command)
            async for message in channel.history():
                if not message.embeds:
                    continue
                message_embed = discord.Embed.to_dict(message.embeds[0])
                if message_embed['footer']['text'] == message_id:
                    await message.edit(embed=embed, attachments=images)
                    return
                else:
                    print(message_embed['footer']['text'], message_id)
            await channel.send(embed=embed, files=images)