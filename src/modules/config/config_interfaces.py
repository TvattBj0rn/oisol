import configparser

import discord

from src.utils import OISOL_HOME_PATH, DataFilesPath, Language


class ConfigViewMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.config_data = None
        self.embed = discord.Embed(title='Configuration')

    async def update_config_embed(self, interaction: discord.Interaction) -> None:
        self.config_data = configparser.ConfigParser()
        self.config_data.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')

        self.embed.clear_fields()
        self.embed.add_field(
            name='💬 | Language',
            value=self.config_data['default']['language'],
            inline=True,
        )
        self.embed.add_field(
            name='🚩 | Regiment',
            value=f"Name: {self.config_data['regiment']['name']}\nTag: {self.config_data['regiment']['tag']}\nFaction: {self.config_data['regiment']['faction']}",
            inline=True,
        )
        self.embed.add_field(
            name='📝 | Register',
            value=f"Recruit symbol: {self.config_data['register']['input']}\nPromoted recruit symbol: {self.config_data['register']['output']}\nPromotion gives regiment tag: {self.config_data['register']['promoted_get_tag']}",
            inline=True,
        )
        self.embed.add_field(
            name='🪖 | Recruit role',
            value=f'{interaction.guild.get_role(int(self.config_data["register"]["recruit_id"])).mention if self.config_data["register"]["recruit_id"] else "None"}\nTo update this role, use: </config-recruit:1261648113505140787>',
            inline=True,
        )

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='config:regiment', emoji='🔄')
    async def refresh_embed(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        await self.update_config_embed(interaction)
        await interaction.response.edit_message(view=self, embed=self.embed)


class SelectLanguageView(discord.ui.View):
    def __init__(self, *, timeout: float | None = None):
        super().__init__(timeout=timeout)
        self.add_item(SelectLanguage())


class SelectLanguage(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='Français', emoji='🇫🇷', value=Language.FR.name),
            discord.SelectOption(label='English', emoji='<:ukus:1205153501823377438>', value=Language.EN.name),
        ]
        super().__init__(placeholder='Choose a language', options=options)

    async def callback(self, interaction: discord.Interaction) -> None:
        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')
        config.set('default', 'language', self.values[0])

        with open(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini', 'w', newline='') as configfile:
            config.write(configfile)

        await interaction.response.edit_message(content='> Language was correctly updated', delete_after=3, view=None)


class SelectFactionView(discord.ui.View):
    def __init__(self, *, timeout: float | None = None):
        super().__init__(timeout=timeout)
        self.add_item(SelectLanguage())


class SelectFaction(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label='English', emoji='<:ukus:1205153501823377438>', value=Language.EN.name),
        ]
        super().__init__(placeholder='Choose a faction', options=options)
