import configparser
import discord
import os
from src.utils.oisol_enums import Language, DataFilesPath


class SelectLanguageView(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        self.add_item(SelectLanguage())


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

        await interaction.response.edit_message(content='> Language was correctly updated', delete_after=3, view=None)


    class SelectFactionView(discord.ui.View):
        def __init__(self, *, timeout=None):
            super().__init__(timeout=timeout)
            self.add_item(SelectLanguage())


    class SelectFaction(discord.ui.Select):
        def __init__(self):
            options = [
                discord.SelectOption(label='Français', emoji='🇫🇷', value=Language.FR.name),
                discord.SelectOption(label='English', emoji='<:ukus:1205153501823377438>', value=Language.EN.name),
            ]
            super().__init__(placeholder='Choose a faction', options=options)
