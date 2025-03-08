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
            name='__General config__',
            value=f'- **Language**: `{self.config_data.get('default', 'language')}`\n'  # Language always default on english on server join and cannot be null
                  f'- **Shard**: `{self.config_data.get('default', 'shard', fallback='ABLE')}`',
        )
        self.embed.add_field(
            name='__Regiment__',
            value=f'- **Name**: `{self.config_data.get('regiment', 'name', fallback='No name set')}`\n'
                  f'- **Tag**: `{self.config_data.get('regiment', 'tag', fallback='No tag set')}`\n'
                  f'- **Faction**: `{self.config_data.get('regiment', 'faction', fallback='NEUTRAL')}`',
        )
        self.embed.add_field(
            name='__Register__',
            value=f'- **Recruit role**: {interaction.guild.get_role(recruit_id).mention if (recruit_id := self.config_data.getint('register', 'recruit_id', fallback=0)) else '`No recruit role set`'}\n'
                  f'- **Recruit symbol**: `{self.config_data.get('register', 'input', fallback='No recruit symbol set')}`\n'
                  f'- **Promoted recruit symbol**: `{self.config_data.get('register', 'output', fallback='No symbol change for promoted recruits')}`\n'
                  f'- **Promotion gives regiment tag**: `{self.config_data.get('register', 'promoted_get_tag', fallback='False')}`',
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
