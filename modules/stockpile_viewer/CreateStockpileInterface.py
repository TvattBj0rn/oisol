import discord
from discord.ui import Select
from modules.utils.locations import REGIONS_STOCKPILES
from modules.stockpile_viewer import csv_handler
from modules.utils.path import generate_path


class CreateStockpileInterface(discord.ui.View):
    def __init__(self, code: str, name: str):
        super().__init__()
        self.stockpile_region_name = ''
        self.stockpile_subregion_name = ''
        self.stockpile_name = name
        self.stockpile_code = code
        self.stockpile_type = ''

        # Default state of the menu
        self.select_first_letter = Select(
            placeholder="Première lettre de la région",
            options=[
                discord.SelectOption(label='A-M'),
                discord.SelectOption(label='M-W')
            ]
        )
        self.select_region = Select(
            placeholder='Nom de la région',
            options=[discord.SelectOption(label='placeholder')],
            disabled=True
        )
        self.select_subregion = Select(
            placeholder='Nom de la sous-région',
            options=[discord.SelectOption(label='placeholder')],
            disabled=True
        )
        self.select_first_letter.callback = self.callback_letter
        self.select_region.callback = self.callback_region
        self.select_subregion.callback = self.callback_subregion
        self.add_item(self.select_first_letter)
        self.add_item(self.select_region)
        self.add_item(self.select_subregion)

    async def callback_letter(self, interaction):
        self.reset_subregion()
        self.select_first_letter.placeholder = self.select_first_letter.values[0]
        self.select_region.disabled = False
        self.select_region.placeholder = 'Nom de la région'
        if self.select_first_letter.values[0] == 'A-M':
            self.select_region.options = [discord.SelectOption(label=region) for region in dict(list(REGIONS_STOCKPILES.items())[:18])]
        else:
            self.select_region.options = [discord.SelectOption(label=region) for region in dict(list(REGIONS_STOCKPILES.items())[18:])]
        await interaction.response.edit_message(view=self)

    async def callback_region(self, interaction):
        self.reset_subregion()
        self.select_region.placeholder = self.select_region.values[0]
        self.select_subregion.disabled = False
        self.select_subregion.options = [discord.SelectOption(label=subregion, emoji=stockpile_type) for (subregion, stockpile_type) in REGIONS_STOCKPILES[self.select_region.values[0]]]
        await interaction.response.edit_message(view=self)

    async def callback_subregion(self, interaction):
        for stockpile in REGIONS_STOCKPILES[self.select_region.values[0]]:
            if stockpile[0] == self.select_subregion.values[0]:
                self.stockpile_type = 'Seaport' if stockpile[1] == '<:seaport:1077298856196313158>' else 'Storage Depot'
        self.stockpile_region_name = self.select_region.values[0]
        self.stockpile_subregion_name = self.select_subregion.values[0]
        self.select_subregion.placeholder = self.select_subregion.values[0]
        self.send_button.style = discord.ButtonStyle.green
        self.send_button.disabled = False
        await interaction.response.edit_message(view=self)


    @discord.ui.button(label='Créer le stock', style=discord.ButtonStyle.grey, disabled=True, row=4)
    async def send_button(self, interaction: discord.Interaction, button: discord.Button):
        self.stop()
        stockpile = {
            'region': self.stockpile_region_name,
            'subregion': self.stockpile_subregion_name,
            'code': self.stockpile_code,
            'name': self.stockpile_name,
            'type': self.stockpile_type
        }
        file_path = generate_path(interaction.guild.id, 'stockpiles.csv')
        csv_handler.csv_try_create_file(file_path, ['region', 'subregion', 'code', 'name', 'type'])
        csv_handler.csv_append_data(file_path, stockpile)
        await interaction.response.send_message(f'> {self.stockpile_name} (code: {self.stockpile_code}) à {self.stockpile_region_name} | {self.stockpile_subregion_name} a été crée sans problèmes', ephemeral=True)

    def reset_subregion(self):
        self.select_subregion.placeholder = 'Nom de la sous-région'
        self.select_subregion.disabled = True
        self.send_button.style = discord.ButtonStyle.grey
        self.send_button.disabled = True
