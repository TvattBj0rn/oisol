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


class ModuleRegister(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot
        self.csv_keys = ['member', 'timer']

    @app_commands.command(name='register_view')
    async def register_view(self, interaction: discord.Interaction):
        # TODO: en 2e etape rendre cette méthode statique et créer une méthode dynamique qui prend sa place
        await interaction.response.defer()
        register_members = CsvHandlerRegister(self.csv_keys).csv_get_all_data(
            os.path.join(pathlib.Path(pathlib.Path.home()), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value)
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
            os.path.join(pathlib.Path(pathlib.Path.home()), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value),
            {
                self.csv_keys[0]: recruit_id,
                self.csv_keys[1]: recruit_timer
            }
        )

        await member.edit(nick=safeguarded_nickname(f'⦾ {member.display_name}'))
        await interaction.response.send_message(f'> {member.mention} a été ajouté au registre')

    @app_commands.command(name='register_clean')
    async def register_clean(self, interaction: discord.Interaction):
        updated_recruit_list = []
        register_members = CsvHandlerRegister(self.csv_keys).csv_get_all_data(
            os.path.join(pathlib.Path(pathlib.Path.home()), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value)
        )
        for register_member in register_members:
            # if member still on the server and has role_id 1125790881094570045 in its roles
            if interaction.guild.get_member(int(register_member[self.csv_keys[0]])) and interaction.guild.get_member(int(register_member[self.csv_keys[0]])).get_role(1125790881094570045):
                updated_recruit_list.append(register_member)
        CsvHandlerRegister(self.csv_keys).csv_rewrite_file(
            os.path.join(pathlib.Path(pathlib.Path.home()), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value),
            updated_recruit_list
        )
        await interaction.response.send_message("> Le registre a été nettoyé (doublons / plus enlistés / plus sur le serveur)")

    @app_commands.command(name='register_promote')
    async def register_promote(self, interaction: discord.Interaction, member: discord.Member, is_promoted: bool):
        updated_recruit_list = []
        is_member_in_register = False
        register_members = CsvHandlerRegister(self.csv_keys).csv_get_all_data(
            os.path.join(pathlib.Path(pathlib.Path.home()), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value)
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
            os.path.join(pathlib.Path(pathlib.Path.home()), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value),
            updated_recruit_list
        )
        new_member_name = member.display_name
        if new_member_name.startswith('⦾ '):
            new_member_name = new_member_name[2:]
        if is_promoted:
            new_member_name = f'[FCF] ⦿ {new_member_name}'
            await interaction.response.send_message(f'> {member.mention} a été promu !')
        else:
            await interaction.response.send_message(f'> {member.mention} a été retiré du registre.')
        await member.edit(nick=safeguarded_nickname(new_member_name))
