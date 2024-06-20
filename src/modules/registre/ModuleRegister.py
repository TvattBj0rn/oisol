import configparser
import discord
import os
import pathlib
import time
from discord import app_commands
from discord.ext import commands
from src.utils.functions import update_discord_interface, safeguarded_nickname
from src.utils.oisol_enums import DataFilesPath, Modules
from src.utils.resources import MODULES_CSV_KEYS
from src.utils.CsvHandler import CsvHandler
from src.modules.registre.RegisterViewMenu import RegisterViewMenu


class ModuleRegister(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.oisol = bot

    @app_commands.command(name='register_view')
    async def register_view(self, interaction: discord.Interaction):
        print(f'> register_view command by {interaction.user.name} on {interaction.guild.name}')
        await interaction.response.defer()

        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild.id))
        config = configparser.ConfigParser()
        config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        config['register'] = {}
        config['register']['channel'] = str(interaction.channel_id)
        with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
            config.write(configfile)

        register_view_instance = RegisterViewMenu().refresh_register(str(interaction.guild.id))
        await interaction.followup.send(view=register_view_instance, embed=register_view_instance.get_current_embed())

    @app_commands.command(name='register_add')
    async def register_add(self, interaction: discord.Interaction, member: discord.Member):
        print(f'> register_add command by {interaction.user.name} on {interaction.guild.name}')
        if interaction.guild.owner_id == member.id:
            await interaction.response.send_message('Le propriétaire du serveur ne peut pas être ajouté au registre')
            return

        recruit_id, recruit_timer = member.id, int(time.time())
        CsvHandler(MODULES_CSV_KEYS['register']).csv_append_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value),
            {
                MODULES_CSV_KEYS['register'][0]: recruit_id,
                MODULES_CSV_KEYS['register'][1]: recruit_timer
            },
            Modules.REGISTER
        )
        register_view = RegisterViewMenu().refresh_register(str(interaction.guild.id))
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.join('/', 'oisol', str(interaction.guild.id)), DataFilesPath.CONFIG.value))
        if config['register']['input'] != 'None':
            await member.edit(nick=safeguarded_nickname(f"{config['register']['input']} {member.display_name}"))

        await update_discord_interface(
            interaction,
            'Register',
            view=register_view
        )
        await interaction.response.send_message(f'> {member.mention} a été ajouté au registre', ephemeral=True)

    @app_commands.command(name='register_clean')
    async def register_clean(self, interaction: discord.Interaction):
        print(f'> register_clean command by {interaction.user.name} on {interaction.guild.name}')
        updated_recruit_list = []
        register_members = CsvHandler(MODULES_CSV_KEYS['register']).csv_get_all_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value),
            Modules.REGISTER
        )
        for register_member in register_members:
            # if member still on the server and has role_id 1125790881094570045 in its roles
            if interaction.guild.get_member(int(register_member[MODULES_CSV_KEYS['register'][0]])):  # and interaction.guild.get_member(int(register_member[MODULES_CSV_KEYS['register'][0]])).get_role(1125790881094570045):
                updated_recruit_list.append(register_member)
        CsvHandler(MODULES_CSV_KEYS['register']).csv_rewrite_file(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value),
            updated_recruit_list,
            Modules.REGISTER
        )
        register_view = RegisterViewMenu().refresh_register(str(interaction.guild.id), updated_recruit_list)

        await update_discord_interface(
            interaction,
            'Register',
            view=register_view
        )
        await interaction.response.send_message(
            "> Le registre a été nettoyé (doublons / plus enlistés / plus sur le serveur)",
            ephemeral=True
        )

    @app_commands.command(name='register_promote')
    async def register_promote(self, interaction: discord.Interaction, member: discord.Member, is_promoted: bool):
        print(f'> register_promote command by {interaction.user.name} on {interaction.guild.name}')
        updated_recruit_list = []
        is_member_in_register = False
        register_members = CsvHandler(MODULES_CSV_KEYS['register']).csv_get_all_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value),
            Modules.REGISTER
        )

        for register_member in register_members:
            if int(register_member[MODULES_CSV_KEYS['register'][0]]) != int(member.id):
                updated_recruit_list.append(register_member)
            else:
                is_member_in_register = True
        if not is_member_in_register:
            await interaction.response.send_message(f"> {member.mention} n'est pas dans le registre.")
            return

        CsvHandler(MODULES_CSV_KEYS['register']).csv_rewrite_file(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value),
            updated_recruit_list,
            Modules.REGISTER
        )
        register_view = RegisterViewMenu().refresh_register(str(interaction.guild.id), updated_recruit_list)
        await update_discord_interface(
            interaction,
            'Register',
            view=register_view
        )

        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.join('/', 'oisol', str(interaction.guild.id)), DataFilesPath.CONFIG.value))

        if config['register']['input'] != 'None':
            new_member_name = member.display_name
            if new_member_name.startswith(f"{config['register']['input']} "):
                new_member_name = new_member_name[2:]
        else:
            new_member_name = member.display_name

        if is_promoted:
            if config['register']['output']:
                new_member_name = f"{config['register']['output']} {new_member_name}"
            if bool(config['register']['promoted_get_tag']):
                new_member_name = f"[{config['regiment']['tag']}] {new_member_name}"
            await interaction.response.send_message(f'> {member.mention} a été promu !')
        else:
            await interaction.response.send_message(f'> {member.mention} a été retiré du registre.')
        await member.edit(nick=safeguarded_nickname(new_member_name))
