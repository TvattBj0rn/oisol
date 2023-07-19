import discord
import csv
import os
import time
from main import bot as oisol
from modules.stockpile_viewer import csv_handler
from modules.utils.path import generate_path


@oisol.tree.command(name='register_display')
async def register_display(interaction: discord.Interaction):
    await interaction.response.defer()
    register_embed = discord.Embed(
        title='Registre',
        description='Recrues actuelles',
        color=0x477DA9
    )
    try:
        register_file = open(generate_path(interaction.guild.id, 'register.csv'), 'r')
    except FileNotFoundError:
        await interaction.followup.send('> Aucune recrue dans le registre actuellement !')
        return
    csv_reader = csv.reader(register_file, delimiter=';')
    for row in csv_reader:
        register_embed.add_field(name='', value=f'<@{row[0]}> **|** <t:{row[1]}:R>', inline=False)
    register_file.close()
    await interaction.followup.send(embed=register_embed)


@oisol.tree.command(name='register_init')
async def register_init(interaction: discord.Interaction):
    os.makedirs(generate_path(interaction.guild.id, ''), exist_ok=True)
    try:
        csv_handler.csv_try_create_file(generate_path(interaction.guild.id, 'register.csv'), ['region', 'subregion', 'code', 'name', 'type'])
    except FileExistsError:
        pass
    await interaction.response.send_message(f'> Tout a bien pu être initialisé !', ephemeral=True)

@oisol.tree.command(name='register_prolong')
async def register_prolong(interaction: discord.Interaction, member: discord.Member):
    updated_recruit_list = []
    try:
        register_file = open(generate_path(interaction.guild.id, 'register.csv'), 'r')
    except FileNotFoundError:
        await interaction.followup.send('> Aucune recrue dans le registre actuellement !')
        return
    csv_reader = csv.reader(register_file, delimiter=';')
    for row in csv_reader:
        if int(row[0]) != int(member.id):
            updated_recruit_list.append(row)
        else:
            updated_recruit_list.append([row[0], int(time.time()) + 1209600])
    register_file.close()
    with open(generate_path(interaction.guild.id, 'register.csv'), 'w') as register_file:
        csv_writer = csv.writer(register_file, delimiter=';')
        for row in updated_recruit_list:
            csv_writer.writerow(row)



@oisol.tree.command(name='register_add')
async def register_add(interaction: discord.Interaction, member: discord.Member, timer: str = '0'):
    recruit_id, recruit_timer = member.id, int(time.time()) + 1209600 if timer == '0' else int(timer[3:-1]) + 1209600
    try:
        register_file = open(generate_path(interaction.guild.id, 'register.csv'), 'a')
    except FileNotFoundError:
        register_file = open(generate_path(interaction.guild.id, 'register.csv'), 'w')
    register_writer = csv.writer(register_file, delimiter=';')
    register_writer.writerow([recruit_id, recruit_timer])
    register_file.close()
    await interaction.response.send_message(f"> <@{recruit_id}> a vu sa période d'essai prolongée, passage potentiel en soldat dans <t:{recruit_timer}:R>")


@oisol.tree.command(name='register_promote')
async def register_promote(interaction: discord.Interaction, member: discord.Member, is_promoted: bool):
    updated_recruit_list = []
    try:
        register_file = open(generate_path(interaction.guild.id, 'register.csv'), 'r')
    except FileNotFoundError:
        await interaction.followup.send('> Aucune recrue dans le registre actuellement !')
        return
    csv_reader = csv.reader(register_file, delimiter=';')
    for row in csv_reader:
        if int(row[0]) != int(member.id):
            updated_recruit_list.append(row)
    register_file.close()
    with open(generate_path(interaction.guild.id, 'register.csv'), 'w') as register_file:
        csv_writer = csv.writer(register_file, delimiter=';')
        for row in updated_recruit_list:
            csv_writer.writerow(row)
    if is_promoted:
        await interaction.response.send_message(f'> <@{member.id}> a été promu !')
    else:
        await interaction.response.send_message(f'> <@{member.id}> a été retiré du registre')

async def setup(bot):
    bot.tree.add_command(register_display)
    bot.tree.add_command(register_init)
    bot.tree.add_command(register_add)
    bot.tree.add_command(register_promote)
    bot.tree.add_command(register_prolong)