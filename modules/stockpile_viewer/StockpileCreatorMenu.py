import discord
from discord.ui import Select
from modules.stockpile_viewer.locations import REGIONS
from modules.stockpile_viewer import google_sheet_commands


class StockpileCreatorMenu(discord.ui.View):
    def __init__(self, code: int, name: str):
        super().__init__()
        self.stockpile_location = []
        self.stockpile_name = name
        self.stockpile_code = code
        self.stockpile_type = ''
        self.select_type = Select(
            placeholder='Choose the storage type',
            options=[
                discord.SelectOption(label='Seaport', emoji='<:seaport:1077298856196313158>'),
                discord.SelectOption(label='Storage Depot', emoji='<:storagedepot:1077298889490694204>')
            ]
        )
        self.select_first_letter = Select(
            placeholder="Choose the region's starting letter",
            options=[
                discord.SelectOption(label='A-M'),
                discord.SelectOption(label='N-W')
            ]
        )
        self.select_region = Select(
            placeholder='Choose a region',
            options=[discord.SelectOption(label='')],
            disabled=True
        )
        self.select_subregion = Select(
            placeholder='Choose a sub-region',
            options=[discord.SelectOption(label='')],
            disabled=True
        )
        self.select_type.callback = self.callback_type
        self.select_first_letter.callback = self.callback_letter
        self.select_region.callback = self.callback_region
        self.select_subregion.callback = self.callback_subregion
        self.add_item(self.select_type)
        self.add_item(self.select_first_letter)
        self.add_item(self.select_region)
        self.add_item(self.select_subregion)

    async def callback_letter(self, interaction):
        self.select_first_letter.placeholder = self.select_first_letter.values[0]
        self.select_region.disabled = False
        if self.select_first_letter.values[0] == 'A-M':
            self.select_region.options = [discord.SelectOption(label=region) for region in dict(list(REGIONS.items())[:18])]
        else:
            self.select_region.options = [discord.SelectOption(label=region) for region in dict(list(REGIONS.items())[18:])]
        await interaction.response.edit_message(view=self)

    async def callback_region(self, interaction):
        self.select_region.placeholder = self.select_region.values[0]
        self.select_subregion.disabled = False
        self.select_subregion.options = [discord.SelectOption(label=subregion) for subregion in REGIONS[self.select_region.values[0]]]
        await interaction.response.edit_message(view=self)

    async def callback_subregion(self, interaction):
        self.stockpile_location.append(self.select_region.values[0])
        self.stockpile_location.append(self.select_subregion.values[0])
        self.select_subregion.placeholder = self.select_subregion.values[0]
        self.send_button.style = discord.ButtonStyle.green
        self.send_button.disabled = False
        await interaction.response.edit_message(view=self)

    async def callback_type(self, interaction):
        self.stockpile_type = self.select_type.values[0]
        self.select_type.placeholder = self.select_type.values[0]
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Create Stockpile', style=discord.ButtonStyle.grey, disabled=True, row=4)
    async def send_button(self, interaction: discord.Interaction, button: discord.Button):
        self.stop()
        google_sheet_commands.create_stockpile(self.stockpile_location, self.stockpile_code, self.stockpile_name, self.stockpile_type)
        await interaction.response.send_message(f'> {self.stockpile_type} {self.stockpile_name} (code: {self.stockpile_code}) at {self.stockpile_location[0]} | {self.stockpile_location[1]} was created', ephemeral=True)
