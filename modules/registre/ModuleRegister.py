import discord
import os
import pathlib
import time
from discord import app_commands
from discord.ext import commands
from modules.utils import DataFilesPath, safeguarded_nickname, MODULES_CSV_KEYS
from modules.registre.CsvHandlerRegistre import CsvHandlerRegister
from modules.registre.RegisterViewMenu import RegisterViewMenu


REGISTER_CSV_KEYS = MODULES_CSV_KEYS['register']


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

    @app_commands.command(name='register_view')
    async def register_view(self, interaction: discord.Interaction):
        await interaction.response.defer()
        register_view_instance = RegisterViewMenu().refresh_register(str(interaction.guild.id))
        await interaction.followup.send(view=register_view_instance, embed=register_view_instance.get_current_embed())

    @app_commands.command(name='register_add')
    async def register_add(self, interaction: discord.Interaction, member: discord.Member):
        if interaction.guild.owner_id == member.id:
            await interaction.response.send_message(f'Le propriétaire du serveur ne peut pas être ajouté au registre')
            return

        recruit_id, recruit_timer = member.id, int(time.time())
        CsvHandlerRegister(REGISTER_CSV_KEYS).csv_append_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value),
            {
                REGISTER_CSV_KEYS[0]: recruit_id,
                REGISTER_CSV_KEYS[1]: recruit_timer
            }
        )
        register_view = RegisterViewMenu().refresh_register(str(interaction.guild.id))

        await member.edit(nick=safeguarded_nickname(f'⦾ {member.display_name}'))
        await send_data_to_discord(
            interaction,
            register_view,
            'Register'
        )
        await interaction.response.send_message(f'> {member.mention} a été ajouté au registre', ephemeral=True)

    @app_commands.command(name='register_clean')
    async def register_clean(self, interaction: discord.Interaction):
        updated_recruit_list = []
        register_members = CsvHandlerRegister(REGISTER_CSV_KEYS).csv_get_all_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value)
        )
        for register_member in register_members:
            # if member still on the server and has role_id 1125790881094570045 in its roles
            if interaction.guild.get_member(int(register_member[REGISTER_CSV_KEYS[0]])) and interaction.guild.get_member(
                    int(register_member[REGISTER_CSV_KEYS[0]])).get_role(1125790881094570045):
                updated_recruit_list.append(register_member)
        CsvHandlerRegister(REGISTER_CSV_KEYS).csv_rewrite_file(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value),
            updated_recruit_list
        )
        register_view = RegisterViewMenu().refresh_register(str(interaction.guild.id), updated_recruit_list)

        await send_data_to_discord(
            interaction,
            register_view,
            'Register'
        )
        await interaction.response.send_message(
            "> Le registre a été nettoyé (doublons / plus enlistés / plus sur le serveur)",
            ephemeral=True
        )

    @app_commands.command(name='register_promote')
    async def register_promote(self, interaction: discord.Interaction, member: discord.Member, is_promoted: bool):
        updated_recruit_list = []
        is_member_in_register = False
        register_members = CsvHandlerRegister(REGISTER_CSV_KEYS).csv_get_all_data(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value)
        )

        for register_member in register_members:
            if int(register_member[REGISTER_CSV_KEYS[0]]) != int(member.id):
                updated_recruit_list.append(register_member)
            else:
                is_member_in_register = True
        if not is_member_in_register:
            await interaction.response.send_message(f"> {member.mention} n'est pas dans le registre.")
            return

        CsvHandlerRegister(REGISTER_CSV_KEYS).csv_rewrite_file(
            os.path.join(pathlib.Path('/'), 'oisol', str(interaction.guild.id), DataFilesPath.REGISTER.value),
            updated_recruit_list
        )
        register_view = RegisterViewMenu().refresh_register(str(interaction.guild.id), updated_recruit_list)

        new_member_name = member.display_name
        if new_member_name.startswith('⦾ '):
            new_member_name = new_member_name[2:]

        await send_data_to_discord(
            interaction,
            register_view,
            'Register'
        )
        if is_promoted:
            new_member_name = f'[FCF] ⦿ {new_member_name}'
            await interaction.response.send_message(f'> {member.mention} a été promu !')
        else:
            await interaction.response.send_message(f'> {member.mention} a été retiré du registre.')
        await member.edit(nick=safeguarded_nickname(new_member_name))
