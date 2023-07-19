import discord
import csv
import time
from main import bot as oisol

@oisol.tree.command(name='register_display')
async def register_display(interaction: discord.Interaction):
    await interaction.response.defer()
    register_embed = discord.Embed(
        title='Registre',
        description='Recrues actuelles',
        color=0x477DA9
    )
    try:
        register_file = open(f'/home/ubuntu/oisol/data/{interaction.guild.id}/register.csv', 'r')
    except FileNotFoundError:
        await interaction.followup.send('> Aucune recrue dans le registre actuellement !')
        return
    csv_reader = csv.reader(register_file, delimiter=';')
    for row in csv_reader:
        register_embed.add_field(name='', value=f'<@{row[0]}> **|** <t:{row[1]}:R>', inline=False)
    register_file.close()
    await interaction.followup.send(embed=register_embed)


@oisol.tree.command(name='register_add')
async def register_add(interaction: discord.Interaction, member: discord.Member, timer: str = '0'):
    recruit_id, recruit_timer = member.id, int(time.time()) + 604800 if timer == '0' else int(timer[3:-1]) + 604800
    try:
        register_file = open(f'/home/ubuntu/oisol/data/{interaction.guild.id}/register.csv', 'a')
    except FileNotFoundError:
        register_file = open(f'/home/ubuntu/oisol/data/{interaction.guild.id}/register.csv', 'w')
    register_writer = csv.writer(register_file, delimiter=';')
    register_writer.writerow([recruit_id, recruit_timer])
    register_file.close()
    await interaction.response.send_message(f'> <@{recruit_id}> a été ajouté au registre, passage potentiel en soldat dans <t:{recruit_timer}:R>')


@oisol.tree.command(name='register_promote')
async def register_promote(interaction: discord.Interaction, member: discord.Member):
    updated_recruit_list = []
    try:
        register_file = open(f'/home/ubuntu/oisol/data/{interaction.guild.id}/register.csv', 'r')
    except FileNotFoundError:
        await interaction.followup.send('> Aucune recrue dans le registre actuellement !')
        return
    csv_reader = csv.reader(register_file, delimiter=';')
    for row in csv_reader:
        if int(row[0]) != int(member.id):
            updated_recruit_list.append(row)
    register_file.close()
    with open('register.csv', 'w') as register_file:
        csv_writer = csv.writer(register_file, delimiter=';')
        for row in updated_recruit_list:
            csv_writer.writerow(row)
    await interaction.response.send_message(f'> <@{member.id}> a été promu !')

async def setup(bot):
    bot.tree.add_command(register_display)
    bot.tree.add_command(register_add)
    bot.tree.add_command(register_promote)