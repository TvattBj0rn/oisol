import discord
import csv
import os
import time
from main import bot as oisol
from modules.stockpile_viewer import csv_handler
from modules.utils.path import generate_path, DataFilesPath


@oisol.tree.command(name='register_view')
async def register_view(interaction: discord.Interaction):
    await interaction.response.defer()
    register_embed = discord.Embed(
        title='Registre',
        description='Recrues actuelles',
        color=0x477DA9
    )
    try:
        register_file = open(generate_path(interaction.guild.id, DataFilesPath.REGISTER.value), 'r')
    except FileNotFoundError:
        await interaction.followup.send('> Aucune recrue dans le registre actuellement !')
        return
    csv_reader = csv.reader(register_file, delimiter=';')
    next(csv_reader, None)
    for row in csv_reader:
        register_embed.add_field(name='', value=f'<@{row[0]}> **|** <t:{row[1]}:R>', inline=False)
    register_file.close()
    await interaction.followup.send(embed=register_embed)


@oisol.tree.command(name='register_init')
async def register_init(interaction: discord.Interaction):
    os.makedirs(generate_path(interaction.guild.id, ''), exist_ok=True)
    try:
        csv_handler.csv_try_create_file(generate_path(interaction.guild.id, DataFilesPath.REGISTER.value))
    except FileExistsError:
        pass
    await interaction.response.send_message(f'> Tout a bien pu être initialisé !', ephemeral=True)
# 1209600

@oisol.tree.command(name='register_add')
async def register_add(interaction: discord.Interaction, member: discord.Member):
    recruit_id, recruit_timer = member.id, int(time.time())
    with open(generate_path(interaction.guild.id, DataFilesPath.REGISTER.value), 'a') as csv_file:
        register_writer = csv.writer( csv_file,delimiter=';')
        register_writer.writerow([recruit_id, recruit_timer])

    await interaction.response.send_message(f'> <@{recruit_id}> a été ajouté au registre')

@oisol.tree.command(name='register_clean')
async def register_clean(interaction: discord.Interaction):
    updated_recruit_list = []
    try:
        register_file = open(generate_path(interaction.guild.id, DataFilesPath.REGISTER.value), 'r')
    except FileNotFoundError:
        await interaction.followup.send('> Aucune recrue dans le registre actuellement !')
        return
    csv_reader = csv.reader(register_file, delimiter=';')
    next(csv_reader, None)
    for row in csv_reader:
        if interaction.guild.get_member(int(row[0])) is not None:
            for role in interaction.guild.get_member(int(row[0])).roles:
                if role.name == 'Enlisté':
                    updated_recruit_list.append(row)
    with open(generate_path(interaction.guild.id, DataFilesPath.REGISTER.value), 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['member', 'timer'])
        for row in updated_recruit_list:
            writer.writerow(row)
    await interaction.response.send_message("> Le registre a été nettoyé (personnes n'étant plus enlistées ou plus sur le serveur)")

@oisol.tree.command(name='register_promote')
async def register_promote(interaction: discord.Interaction, member: discord.Member, is_promoted: bool):
    updated_recruit_list = []
    try:
        register_file = open(generate_path(interaction.guild.id, DataFilesPath.REGISTER.value), 'r')
    except FileNotFoundError:
        await interaction.followup.send('> Aucune recrue dans le registre actuellement !')
        return
    csv_reader = csv.reader(register_file, delimiter=';')
    next(csv_reader, None)
    for row in csv_reader:
        if int(row[0]) != int(member.id):
            updated_recruit_list.append(row)
    register_file.close()
    with open(generate_path(interaction.guild.id, DataFilesPath.REGISTER.value), 'w') as register_file:
        csv_writer = csv.writer(register_file, delimiter=';')
        for row in updated_recruit_list:
            csv_writer.writerow(row)
    if is_promoted:
        await interaction.response.send_message(f'> <@{member.id}> a été promu !')
    else:
        await interaction.response.send_message(f'> <@{member.id}> a été retiré du registre')



async def setup(bot):
    bot.tree.add_command(register_view)
    bot.tree.add_command(register_init)
    bot.tree.add_command(register_add)
    bot.tree.add_command(register_clean)
    bot.tree.add_command(register_promote)
