import discord
import os
import pathlib
from src.utils.CsvHandler import CsvHandler
from src.utils.oisol_enums import DataFilesPath, Faction
from src.utils.resources import MODULES_CSV_KEYS


class RegisterViewMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.color = Faction.WARDEN.value
        self.csv_keys = MODULES_CSV_KEYS['register']
        self.embeds = []
        self.register_members = []
        self.current_page_index = 0

    def refresh_register_embed(self, guild_id: str):
        self.register_members = CsvHandler(self.csv_keys).csv_get_all_data(
            os.path.join(pathlib.Path('/'), 'oisol', guild_id, DataFilesPath.REGISTER.value)
        )
        self.generate_embeds()

    def generate_embeds(self):
        self.embeds = []
        embed = discord.Embed(
            title='Register | Page 1',
            color=self.color
        )
        if not self.register_members:
            self.embeds.append(embed)
            return

        for i, member_dict in enumerate(self.register_members):
            if i % 25 == 0 and i > 0:
                self.embeds.append(embed)
                embed = discord.Embed(
                    title=f'Register | Page {(i // 25) + 1}',  # Page 0 might seem weird to non-devs
                    color=self.color
                )
                embed.set_footer(text='Register')
            embed.add_field(
                name='',
                value=f'<@{member_dict[self.csv_keys[0]]}> **|** <t:{member_dict[self.csv_keys[1]]}>',
                inline=False
            )
            if i == len(self.register_members) - 1:
                self.embeds.append(embed)

    def get_current_embed(self):
        if not self.embeds:
            embed = discord.Embed(
                title='Registre | Page 1',
                color=self.color
            )
            embed.set_footer(text='Register')
            return embed
        return self.embeds[self.current_page_index]

    @discord.ui.button(emoji='◀️', style=discord.ButtonStyle.blurple, custom_id='RegisterViewMenu:left')
    async def left_button_callback(self, interaction: discord.Interaction, _button: discord.ui.Button):
        if self.current_page_index - 1 == -1:
            self.current_page_index = len(self.embeds) - 1
        else:
            self.current_page_index -= 1
        self.refresh_register_embed(str(interaction.guild.id))

        await interaction.message.edit(view=self, embed=self.get_current_embed())
        await interaction.response.defer()

    @discord.ui.button(emoji='▶️', style=discord.ButtonStyle.blurple, custom_id='RegisterViewMenu:right')
    async def right_button_callback(self, interaction: discord.Interaction, _button: discord.ui.Button):
        if self.current_page_index + 1 == len(self.embeds):
            self.current_page_index = 0
        else:
            self.current_page_index += 1
        self.refresh_register_embed(str(interaction.guild.id))

        await interaction.message.edit(view=self, embed=self.get_current_embed())
        await interaction.response.defer()
