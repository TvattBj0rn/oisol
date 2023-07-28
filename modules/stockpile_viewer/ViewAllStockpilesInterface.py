import discord
from modules.stockpile_viewer import csv_handler
from modules.utils import foxhole_types, locations
from modules.utils.path import generate_path


class ViewAllStockpilesInterface(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.file_path = generate_path(interaction.guild.id, 'stockpiles.csv')
        self.file_path_msg = generate_path(interaction.guild.id, 'message_id.txt')
        self.timeout = None
        self.embed = None
        self.generateEmbed(self.file_path)


    @discord.ui.button(emoji='🔄', style=discord.ButtonStyle.blurple)
    async def refresh_stockpile_list(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.generateEmbed(self.file_path)
        await interaction.response.defer()
        await interaction.edit_original_response(embed=self.embed, view=self)

    def generateEmbed(self, file_path: str):
        stockpile_list = csv_handler.csv_get_all_data(file_path)

        sorted_stockpile_list = dict()

        for stockpile in stockpile_list:
            if not stockpile['region'] in sorted_stockpile_list.keys():
                sorted_stockpile_list[stockpile['region']] = {stockpile['subregion']: [stockpile]}
            else:
                if not stockpile['subregion'] in sorted_stockpile_list[stockpile['region']].keys():
                    sorted_stockpile_list[stockpile['region']][stockpile['subregion']] = [stockpile]
                else:
                    sorted_stockpile_list[stockpile['region']][stockpile['subregion']].append(stockpile)

        sorted_region_list = list(sorted_stockpile_list.keys())
        sorted_region_list.sort()

        embed = discord.Embed(
            title='Stockpiles FCF',
            description='Liste des stockpiles FCF actuels',
            color=foxhole_types.FACTION_COLORS['Warden']
        )
        for region in sorted_region_list:
            sorted_subregion_list = list(sorted_stockpile_list[region].keys())
            sorted_subregion_list.sort()
            embed.add_field(
                name=f'{region}',
                value='',
                inline=False
            )
            subregion_stockpiles_values = ''
            for subregion in sorted_subregion_list:
                for stockpile in sorted_stockpile_list[region][subregion]:
                    subregion_stockpiles_values = f"{stockpile['name']} **|** {stockpile['code']}" if not subregion_stockpiles_values else subregion_stockpiles_values + f"\n{stockpile['name']} **|** {stockpile['code']}"
                subregion_icon = ''
                for subregion_tuple in locations.REGIONS_STOCKPILES[region]:
                    if subregion_tuple[0] == subregion:
                        subregion_icon = subregion_tuple[1]
                embed.add_field(
                    name=f'{subregion_icon} **|** {subregion}',
                    value=subregion_stockpiles_values,
                    inline=False
                )
        self.embed = embed
