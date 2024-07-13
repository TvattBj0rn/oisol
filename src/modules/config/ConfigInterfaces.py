import configparser
import discord
import os
import traceback
from src.utils.oisol_enums import Language, DataFilesPath


class ConfigViewMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.config_data = None
        self.embed = discord.Embed(title='Configuration')

    async def update_config_embed(self, interaction: discord.Interaction):
        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild_id))
        self.config_data = configparser.ConfigParser()
        self.config_data.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))

        self.embed.clear_fields()
        self.embed.add_field(
            name='💬 | Language',
            value=self.config_data['default']['language'],
            inline=True
        )
        self.embed.add_field(
            name='🚩 | Regiment',
            value=f"Name: {self.config_data['regiment']['name']}\nTag: {self.config_data['regiment']['tag']}\nFaction: {self.config_data['regiment']['faction']}",
            inline=True
        )
        self.embed.add_field(
            name='📝 | Register',
            value=f"Recruit symbol: {self.config_data['register']['input']}\nPromoted recruit symbol: {self.config_data['register']['output']}\nPromotion gives regiment tag: {self.config_data['register']['promoted_get_tag']}",
            inline=True
        )
        self.embed.add_field(
            name='🪖 | Recruit role',
            value=f'{interaction.guild.get_role(int(self.config_data["register"]["recruit_id"])).mention if self.config_data["register"]["recruit_id"] else "None"}\nTo update this role, use: </config-recruit:1261648113505140787>',
            inline=True
        )

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='config:language', emoji='💬')
    async def update_language(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            view=SelectLanguageView(message_id=interaction.message.id),
            ephemeral=True
        )

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='config:regiment', emoji='🚩')
    async def update_regiment(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ModalConfig())
        await self.update_config_embed(interaction)
        await interaction.message.edit(embed=self.embed)

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='config:register', emoji='📝')
    async def update_register(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ModalRegister())
        await self.update_config_embed(interaction)
        await interaction.edit_original_response(embed=self.embed)


class SelectLanguage(discord.ui.Select):
    def __init__(self, message_id: int):
        options = [
            discord.SelectOption(label='Français', emoji='🇫🇷', value=Language.FR.name),
            discord.SelectOption(label='English', emoji='<:ukus:1205153501823377438>', value=Language.EN.name),
        ]
        super().__init__(placeholder='Choose a language', options=options)
        self.message_id = message_id

    async def callback(self, interaction: discord.Interaction):
        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild.id))
        config = configparser.ConfigParser()
        config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        config['default']['language'] = self.values[0]

        with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
            config.write(configfile)

        config_view = ConfigViewMenu()
        await config_view.update_config_embed(interaction)
        config_original_message = await interaction.channel.fetch_message(self.message_id)
        await config_original_message.edit(embed=config_view.embed)
        await interaction.response.edit_message(content='> Language was correctly updated', delete_after=3, view=None)


class SelectLanguageView(discord.ui.View):
    def __init__(self, *, timeout=None, message_id: int):
        super().__init__(timeout=timeout)
        self.add_item(SelectLanguage(message_id))


class ModalConfig(discord.ui.Modal, title='Regiment configuration'):
    def __init__(self):
        super().__init__(timeout=None)

    regi = discord.ui.TextInput(
        label='Regiment Name',
        placeholder='...',
    )
    regi_tag = discord.ui.TextInput(
        label='Regiment Tag',
        placeholder='...',
    )
    faction = discord.ui.TextInput(
        label='Faction',
        placeholder='colonial / neutral / warden',
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild.id))
        config = configparser.ConfigParser()
        config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        config['regiment'] = {}
        config['regiment']['name'] = str(self.regi)
        config['regiment']['tag'] = str(self.regi_tag)
        config['regiment']['faction'] = str(self.faction).upper() if str(self.faction).upper() in ['COLONIAL', 'WARDEN'] else 'NEUTRAL'

        with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
            config.write(configfile)

        config_view = ConfigViewMenu()
        await config_view.update_config_embed(interaction)
        await interaction.message.edit(view=config_view, embed=config_view.embed)
        await interaction.response.send_message('> Configuration was correctly updated', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message('> Oops! Something went wrong', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)


class ModalRegister(discord.ui.Modal, title='Register Icon'):
    def __init__(self):
        super().__init__(timeout=None)

    arriving = discord.ui.TextInput(
        label='New recruits icon',
        placeholder='icon that will be given to new recruits in front of their name',
        required=False
    )
    promoted = discord.ui.TextInput(
        label='Promoted recruits icon',
        placeholder='icon that will be given to promoted recruits',
        required=False
    )
    promoted_get_tag = discord.ui.TextInput(
        label='Promoted recruits get regiment tag assigned',
        placeholder='yes / no',
        required=False
    )

    async def on_submit(self, interaction: discord.Interaction):
        oisol_server_home_path = os.path.join('/', 'oisol', str(interaction.guild_id))
        config = configparser.ConfigParser()
        config.read(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value))
        if not config.has_section('register'):
            config['register'] = {}
        config['register']['input'] = str(self.arriving)
        config['register']['output'] = str(self.promoted)
        config['register']['promoted_get_tag'] = str(self.promoted_get_tag).lower() if str(self.promoted_get_tag).lower() == 'y' else 'n'

        with open(os.path.join(oisol_server_home_path, DataFilesPath.CONFIG.value), 'w', newline='') as configfile:
            config.write(configfile)
        config_view = ConfigViewMenu()
        await config_view.update_config_embed(interaction)
        await interaction.message.edit(view=config_view, embed=config_view.embed)
        await interaction.response.send_message('> Configuration was correctly updated', ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message('> Oops! Something went wrong', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)
