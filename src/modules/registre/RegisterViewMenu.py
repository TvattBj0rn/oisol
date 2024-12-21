import os
import pathlib

import discord

from src.utils import MODULES_CSV_KEYS, CsvHandler, DataFilesPath, Faction


class RegisterViewMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.color = Faction.WARDEN.value
        self.csv_keys = MODULES_CSV_KEYS['register']
        self.embeds = []
        self.register_members = []
        self.current_page_index = 0

    def refresh_register_embed(self, guild_id: str):
        self.current_page_index = 0
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
            # If "i" reaches 25 and is non-null, the embed is reset
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
            # If "i" is the last of the list, the embed is appended as-is
            if i == len(self.register_members) - 1:
                self.embeds.append(embed)

    def get_current_embed(self):
        if not self.embeds:
            return discord.Embed().from_dict(
                {
                    'title': 'Register | Page 1',
                    'color': self.color,
                    'footer': {'text': 'Register'}
                }
            )
        return self.embeds[self.current_page_index]

    @discord.ui.button(emoji='◀️', style=discord.ButtonStyle.blurple, custom_id='RegisterViewMenu:left')
    async def left_button_callback(self, interaction: discord.Interaction, _button: discord.ui.Button):
        if self.current_page_index == 0:
            self.current_page_index = len(self.embeds) - 1
        else:
            self.current_page_index -= 1
        self.refresh_register_embed(str(interaction.guild_id))

        await interaction.response.edit_message(view=self, embed=self.get_current_embed())

    @discord.ui.button(emoji='▶️', style=discord.ButtonStyle.blurple, custom_id='RegisterViewMenu:right')
    async def right_button_callback(self, interaction: discord.Interaction, _button: discord.ui.Button):
        if self.current_page_index + 1 == len(self.embeds):
            self.current_page_index = 0
        else:
            self.current_page_index += 1
        self.refresh_register_embed(str(interaction.guild_id))

        await interaction.response.edit_message(view=self, embed=self.get_current_embed())
