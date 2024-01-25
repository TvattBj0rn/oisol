import discord


class RegisterViewMenu(discord.ui.View):
    def __init__(self, csv_keys: list, register_members: list):
        super().__init__()
        self.color = 0x477DA9
        self.embeds = []
        self.current_page_index = 0
        self.csv_keys = csv_keys
        self.register_members = register_members
        self.left_button = discord.ui.Button(
            label='<',
            style=discord.ButtonStyle.blurple,
            disabled=True
        )
        self.left_button.callback = self.left_button_callback
        self.right_button = discord.ui.Button(
            label='>',
            style=discord.ButtonStyle.blurple,
            disabled=True
        )
        self.right_button.callback = self.right_button_callback
        self.add_item(self.left_button)
        self.add_item(self.right_button)
        self.generate_embeds()
        self.refresh_button_status()

    def generate_embeds(self):
        embed = discord.Embed(
            title='Registre | Page 0',
            description='Recrues actuelles',
            color=self.color
        )
        for member_index in range(len(self.register_members)):
            if not member_index % 20 and member_index > 0:
                self.embeds.append(embed)
                embed = discord.Embed(
                    title=f'Registre | Page {member_index // 20}',
                    description='Recrues actuelles',
                    color=self.color
                )
            embed.add_field(
                name='',
                value=f'<@{self.register_members[member_index][self.csv_keys[0]]}> **|** <t:{self.register_members[member_index][self.csv_keys[1]]}:R>',
                inline=False
            )
            if member_index == len(self.register_members) - 1:
                self.embeds.append(embed)

    def get_current_embed(self):
        return self.embeds[self.current_page_index]

    def refresh_button_status(self):
        self.left_button.disabled = True
        self.right_button.disabled = True

        if self.current_page_index - 1 > -1:
            self.left_button.disabled = False

        if self.current_page_index + 1 < len(self.embeds):
            self.right_button.disabled = False

    async def left_button_callback(self, interaction: discord.Interaction):
        self.current_page_index -= 1
        self.refresh_button_status()
        await interaction.message.edit(view=self, embed=self.get_current_embed())
        await interaction.response.defer()

    async def right_button_callback(self, interaction: discord.Interaction):
        self.current_page_index += 1
        self.refresh_button_status()
        await interaction.message.edit(view=self, embed=self.get_current_embed())
        await interaction.response.defer()
