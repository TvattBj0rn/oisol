import discord
from modules.stockpile_viewer import google_sheet_commands
from modules.utils import foxhole_types, locations

class ViewAllStockpilesInterface(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.embed = None
        self.generateEmbed()
        # self.addButton = discord.ui.Button(emoji='➕', style=discord.ButtonStyle.green)
        self.removeButton = discord.ui.Button(emoji='➖', style=discord.ButtonStyle.red)


    def generateEmbed(self):
        stockpile_list = google_sheet_commands.get_all_stockpiles()
        sorted_stockpile_list = dict()

        for stockpile_name, stockpile_values in stockpile_list.items():
            region, subregion = stockpile_values['localisation'].split(' - ')

            for stockpile_type in locations.REGIONS_STOCKPILES[region]:
                if subregion in stockpile_type:
                    stockpile_values['localisation'] = f'{stockpile_type[1]} | {region} - {subregion}'
            if stockpile_values['localisation'] not in sorted_stockpile_list.keys():
                sorted_stockpile_list[stockpile_values['localisation']] = list()
            sorted_stockpile_list[stockpile_values['localisation']].append({stockpile_name: stockpile_values})
        embed = discord.Embed(
            title='Stockpiles',
            description='Current accessible stockpiles',
            color=foxhole_types.FACTION_COLORS['Warden']
        )

        for localisation, stockpile_list in sorted_stockpile_list.items():
            stockpiles_here = str()
            for stockpile in stockpile_list:
                stockpiles_here += f"{stockpile[list(stockpile.keys())[0]]['name']} | {stockpile[list(stockpile.keys())[0]]['code']}\n"
            embed.add_field(
                name=localisation,
                value=stockpiles_here,
                inline=False
            )
        embed.add_field(
            name='',
            value=f"[Google Sheets]({'https://docs.google.com/spreadsheets/d/1xp-t0g0eAK8olQv_ZIdL_T-ZoW8T6fuG86MqkmW4lOY/'})",
            inline=False
        )
        self.embed = embed
