import discord
import os
import pathlib
from typing_extensions import Self
from src.utils.CsvHandler import CsvHandler
from src.utils.oisol_enums import DataFilesPath, Faction, Modules
from src.utils.resources import MODULES_CSV_KEYS


class RegisterViewMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.color = Faction.WARDEN.value
        self.csv_keys = MODULES_CSV_KEYS['register']
        self.embeds = []
        self.register_members = []
        self.current_page_index = 0

    def refresh_register(self, guild_id: str, updated_recruit_list: list = None) -> Self:
        if updated_recruit_list:
            self.register_members = updated_recruit_list
        else:
            self.register_members = CsvHandler(self.csv_keys).csv_get_all_data(
                os.path.join(pathlib.Path('/'), 'oisol', guild_id, DataFilesPath.REGISTER.value),
                Modules.REGISTER
            )
        self.generate_embeds()

        return self

    def generate_embeds(self):
        self.embeds = []
        embed = discord.Embed(
            title='Registre | Page 0',
            description='Recrues actuelles',
            color=self.color
        )
        embed.set_footer(text='Register')
        for member_index in range(len(self.register_members)):
            if not member_index % 20 and member_index > 0:
                self.embeds.append(embed)
                embed = discord.Embed(
                    title=f'Registre | Page {member_index // 20}',
                    description='Recrues actuelles',
                    color=self.color
                )
                embed.set_footer(text='Register')
            embed.add_field(
                name='',
                value=f'<@{self.register_members[member_index][self.csv_keys[0]]}> **|** <t:{self.register_members[member_index][self.csv_keys[1]]}:R>',
                inline=False
            )
            if member_index == len(self.register_members) - 1:
                self.embeds.append(embed)

    def get_current_embed(self):
        if not self.embeds:
            embed = discord.Embed(
                title='Registre | Page 0',
                description='Recrues actuelles',
                color=self.color
            )
            embed.set_footer(text='Register')
            return embed
        return self.embeds[self.current_page_index]

    @discord.ui.button(label='<', style=discord.ButtonStyle.blurple, custom_id='RegisterViewMenu:left')
    async def left_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page_index - 1 == -1:
            self.current_page_index = len(self.embeds) - 1
        else:
            self.current_page_index -= 1
        self.refresh_register(str(interaction.guild.id))

        await interaction.message.edit(view=self, embed=self.get_current_embed())
        await interaction.response.defer()

    @discord.ui.button(label='>', style=discord.ButtonStyle.blurple, custom_id='RegisterViewMenu:right')
    async def right_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page_index + 1 == len(self.embeds):
            self.current_page_index = 0
        else:
            self.current_page_index += 1
        self.refresh_register(str(interaction.guild.id))

        await interaction.message.edit(view=self, embed=self.get_current_embed())
        await interaction.response.defer()
