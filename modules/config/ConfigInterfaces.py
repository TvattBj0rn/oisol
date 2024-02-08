import configparser
import discord
import os
import traceback
from modules.utils import Language, DataFilesPath


class SelectLanguage(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Français', emoji='🇫🇷', value=Language.FR.name),
            discord.SelectOption(label='English', emoji='<:ukus:1205153501823377438>', value=Language.EN.name),
        ]
        super().__init__(placeholder='Choose a language', options=options)

    async def callback(self, interaction: discord.Interaction):
        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild.id))
        config = configparser.ConfigParser()
        config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        config['default']['language'] = self.values[0]
        with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
            config.write(configfile)

        await interaction.response.edit_message(content='> La langue a bien été mise à jour', delete_after=3, view=None)


class SelectLanguageView(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        self.add_item(SelectLanguage())


class ModalConfig(discord.ui.Modal, title='Configuration'):
    def __init__(self, faction: str):
        super().__init__()
        self.faction = faction

    regi = discord.ui.TextInput(
        label='Regiment Name',
        placeholder='...',
    )
    regi_tag = discord.ui.TextInput(
        label='Regiment Tag',
        placeholder='...',
    )

    async def on_submit(self, interaction: discord.Interaction):
        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild.id))
        config = configparser.ConfigParser()
        config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        config['regiment'] = {}
        config['regiment']['name'] = str(self.regi)
        config['regiment']['tag'] = str(self.regi_tag)
        config['regiment']['faction'] = self.faction
        with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
            config.write(configfile)
        await interaction.response.send_message('Config saved !', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message("Oops! Something went wrong ^^'", ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)


