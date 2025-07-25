import sqlite3

import discord

from src.utils import OISOL_HOME_PATH


class RegisterViewMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        # Not clean because this means two connection to the same db but this will have to do for now
        self.connection = sqlite3.connect(OISOL_HOME_PATH / 'oisol.db')
        self.cursor = self.connection.cursor()
        self.embeds = []
        self.register_members = []
        self.current_page_index = 0

    def refresh_register_embed(self, guild_id: int) -> None:
        self.current_page_index = 0

        self.register_members = self.cursor.execute(
            'SELECT MemberId, RegistrationDate FROM GroupsRegister WHERE GroupId == ?',
            (guild_id,)
        ).fetchall()
        self._generate_embeds()

    def _generate_embeds(self) -> None:
        self.embeds = []
        embed = discord.Embed(
            title='Register | Page 1',
        )
        # Default embed when no member is registered
        if not self.register_members:
            self.embeds.append(embed)
            return

        for i, member_tuple in enumerate(self.register_members):
            # If "i" reaches 25 and is non-null, the embed is reset
            if i % 25 == 0 and i > 0:
                self.embeds.append(embed)
                embed = discord.Embed(
                    title=f'Register | Page {(i // 25) + 1}',  # Page 0 might seem weird to non-devs
                )
                embed.set_footer(text='Register')
            embed.add_field(
                name='',
                value=f'<@{member_tuple[0]}> **|** <t:{member_tuple[1]}>',
                inline=False,
            )
            # If "i" is the last of the list, the embed is appended as-is
            if i == len(self.register_members) - 1:
                self.embeds.append(embed)

    def get_current_embed(self) -> discord.Embed:
        if not self.embeds:
            return discord.Embed().from_dict(
                {
                    'title': 'Register | Page 1',
                    'footer': {'text': 'Register'},
                },
            )
        return self.embeds[self.current_page_index]

    @discord.ui.button(emoji='◀️', style=discord.ButtonStyle.blurple, custom_id='RegisterViewMenu:left')
    async def left_button_callback(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        if self.current_page_index == 0:
            self.current_page_index = len(self.embeds) - 1
        else:
            self.current_page_index -= 1
        self.refresh_register_embed(interaction.guild_id)

        await interaction.response.edit_message(view=self, embed=self.get_current_embed())

    @discord.ui.button(emoji='▶️', style=discord.ButtonStyle.blurple, custom_id='RegisterViewMenu:right')
    async def right_button_callback(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        if self.current_page_index + 1 == len(self.embeds):
            self.current_page_index = 0
        else:
            self.current_page_index += 1
        self.refresh_register_embed(interaction.guild_id)

        await interaction.response.edit_message(view=self, embed=self.get_current_embed())
