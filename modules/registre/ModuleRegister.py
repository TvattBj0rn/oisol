import discord
import os
import pathlib
import time
from discord import app_commands
from discord.ext import commands
from modules.utils.DataFiles import DataFilesPath
from modules.utils.functions import safeguarded_nickname
from modules.registre.CsvHandlerRegistre import CsvHandlerRegister
from modules.registre.RegisterViewMenu import RegisterViewMenu


async def send_data_to_discord(interaction: discord.Interaction, view: RegisterViewMenu, message_id: str):
    for channel in interaction.guild.channels:
        if channel.name == '📋－registre':  # Add possibility to change channel via config file (into the init command)
            async for message in channel.history():
                if not message.embeds:
                    continue
                message_embed = discord.Embed.to_dict(message.embeds[0])
                if message_embed['footer']['text'] == message_id:
                    await message.edit(view=view, embed=view.get_current_embed())
                    return
                else:
                    print(message_embed['footer']['text'], message_id)
            await channel.send(view=view)


class ModuleRegister(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.csv_keys = ['member', 'timer']

    @app_commands.command(name='register_view')
    async def register_view(self, interaction: discord.Interaction):
        await interaction.response.defer()
        register_members = CsvHandlerRegister(self.csv_keys).csv_get_all_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value)
        )
        register_view = RegisterViewMenu(self.csv_keys, register_members)

        await interaction.followup.send(view=register_view, embed=register_view.get_current_embed())

    @app_commands.command(name='register_add')
    async def register_add(self, interaction: discord.Interaction, member: discord.Member):
        if interaction.guild.owner_id == member.id:
            await interaction.response.send_message(f'Le propriétaire du serveur ne peut pas être ajouté au registre')
            return

        recruit_id, recruit_timer = member.id, int(time.time())
        CsvHandlerRegister(self.csv_keys).csv_append_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value),
            {
                self.csv_keys[0]: recruit_id,
                self.csv_keys[1]: recruit_timer
            }
        )
        register_members = CsvHandlerRegister(self.csv_keys).csv_get_all_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value)
        )
        await member.edit(nick=safeguarded_nickname(f'⦾ {member.display_name}'))
        await send_data_to_discord(
            interaction,
            RegisterViewMenu(self.csv_keys, register_members),
            'Register'
        )
        await interaction.response.send_message(f'> {member.mention} a été ajouté au registre')

    @app_commands.command(name='register_clean')
    async def register_clean(self, interaction: discord.Interaction):
        updated_recruit_list = []
        register_members = CsvHandlerRegister(self.csv_keys).csv_get_all_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value)
        )
        for register_member in register_members:
            # if member still on the server and has role_id 1125790881094570045 in its roles
            if interaction.guild.get_member(int(register_member[self.csv_keys[0]])) and interaction.guild.get_member(
                    int(register_member[self.csv_keys[0]])).get_role(1125790881094570045):
                updated_recruit_list.append(register_member)
        CsvHandlerRegister(self.csv_keys).csv_rewrite_file(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value),
            updated_recruit_list
        )
        await send_data_to_discord(
            interaction,
            RegisterViewMenu(self.csv_keys, updated_recruit_list),
            'Register'
        )
        await interaction.response.send_message("> Le registre a été nettoyé (doublons / plus enlistés / plus sur le serveur)")

    @app_commands.command(name='register_promote')
    async def register_promote(self, interaction: discord.Interaction, member: discord.Member, is_promoted: bool):
        updated_recruit_list = []
        is_member_in_register = False
        register_members = CsvHandlerRegister(self.csv_keys).csv_get_all_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value)
        )

        for register_member in register_members:
            if int(register_member[self.csv_keys[0]]) != int(member.id):
                updated_recruit_list.append(register_member)
            else:
                is_member_in_register = True
        if not is_member_in_register:
            await interaction.response.send_message(f"> {member.mention} n'est pas dans le registre.")
            return
        CsvHandlerRegister(self.csv_keys).csv_rewrite_file(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value),
            updated_recruit_list
        )
        await send_data_to_discord(
            interaction,
            RegisterViewMenu(self.csv_keys, updated_recruit_list),
            'Register'
        )

        new_member_name = member.display_name
        await member.edit(nick=safeguarded_nickname(new_member_name))
        if new_member_name.startswith('⦾ '):
            new_member_name = new_member_name[2:]
        if is_promoted:
            new_member_name = f'[FCF] ⦿ {new_member_name}'
            await interaction.response.send_message(f'> {member.mention} a été promu !')
        else:
            await interaction.response.send_message(f'> {member.mention} a été retiré du registre.')
