import discord
from modules.stockpile_viewer import google_sheet_commands


class StockpileViewerMenu(discord.ui.View):
    def __init__(self, name: str):
        super().__init__()
        self.stockpile_values, self.stockpile_config = google_sheet_commands.get_stockpile_status(name=name)
        self.button_home = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='🏠')
        self.button_home.callback = self.home_page_callback
        self.add_item(self.button_home)
        self.button_all_items = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='<:storageall:1078412155625427094>')
        self.button_all_items.callback = self.all_items_callback
        self.add_item(self.button_all_items)
        self.button_small_arms = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='<:smallarms:1078407919172857976>')
        self.button_small_arms.callback = self.small_arms_items_callback
        self.add_item(self.button_small_arms)
        self.button_heavy_arms = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='<:heavyweaponsicon:1078407453890330634>')
        self.button_heavy_arms.callback = self.heavy_arms_items_callback
        self.add_item(self.button_heavy_arms)
        self.button_heavy_ammunition = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='<:heavyammunitionicon:1078407359405232128>')
        self.button_heavy_ammunition.callback = self.heavy_ammunition_items_callback
        self.add_item(self.button_heavy_ammunition)
        self.button_utility = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='<:utilityicon:1078407699907215510>')
        self.button_utility.callback = self.utility_callback
        self.add_item(self.button_utility)
        self.button_medical = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='<:medicalicon:1078407515437543545>')
        self.button_medical.callback = self.medical_callback
        self.add_item(self.button_medical)
        self.button_resource = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='<:resourceicon:1078408318780964914>')
        self.button_resource.callback = self.resource_callback
        self.add_item(self.button_resource)
        self.button_uniforms = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='<:uniformsicon:1078472370551009310>')
        self.button_uniforms.callback = self.uniforms_callback
        self.add_item(self.button_uniforms)
        self.button_vehicles_crates = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='<:vehicleicon:1078410297099948032>')
        self.button_vehicles_crates.callback = self.vehicles_crates_callback
        self.add_item(self.button_vehicles_crates)
        self.button_vehicles = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='<:vehicleicon:1078410297099948032>')
        self.button_vehicles.callback = self.vehicles_callback
        self.add_item(self.button_vehicles)
        self.button_emplacement_crates = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='<:emplacementicon:1078410257556054036>')
        self.button_emplacement_crates.callback = self.emplacements_crates_callback
        self.add_item(self.button_emplacement_crates)
        self.button_emplacement = discord.ui.Button(style=discord.ButtonStyle.blurple, emoji='<:emplacementicon:1078410257556054036>')
        self.button_emplacement.callback = self.emplacements_callback
        self.add_item(self.button_emplacement)

    def set_home_page(self) -> discord.Embed:
        self.button_home.disabled = True
        return discord.Embed(title=self.stockpile_config['Name'], description=f"{('<:storagedepot:1077298889490694204>' if self.stockpile_config['Type'] == 'Storage Depot' else '<:seaport:1077298856196313158>')} | {self.stockpile_config['Localisation']}\nCode: {self.stockpile_config['Code']}")


    def set_all_items_page(self) -> [discord.Embed]:
        self.button_all_items.disabled = True
        embeds_list = []
        embed = discord.Embed(title='<:storageall:1078412155625427094> | All Items')
        all_items_list = []
        for category in self.stockpile_values:
            if not category:
                continue
            for item in self.stockpile_values[category]:
                all_items_list.append(item)
        for item_index in range(len(all_items_list)):
            if item_index == 24:
                embeds_list.append(embed)
                embed = discord.Embed(title='<:storageall:1078412155625427094> | All Items')
            embed.add_field(name=list(all_items_list[item_index].keys())[0], value=f'x{list(all_items_list[item_index].values())[0]}')
        embeds_list.append(embed)
        return embeds_list

    def set_small_arms_page(self):
        self.button_small_arms.disabled = True
        embeds_list = []
        all_items_list = []
        if not self.stockpile_values['Small Arms']:
            embeds_list.append(discord.Embed(title='<:smallarms:1078407919172857976> | Small Arms').add_field(name='Empty', value=''))
        else:
            for item in self.stockpile_values['Small Arms']:
                all_items_list.append(item)
            embed = discord.Embed(title='<:smallarms:1078407919172857976> | Small Arms')
            for item_index in range(len(all_items_list)):
                if item_index == 24:
                    embeds_list.append(embed)
                    embed = discord.Embed(title='<:smallarms:1078407919172857976> | Small Arms')
                embed.add_field(name=list(all_items_list[item_index].keys())[0], value=f'x{list(all_items_list[item_index].values())[0]}')
            embeds_list.append(embed)
        return embeds_list

    def set_heavy_arms_page(self):
        self.button_heavy_arms.disabled = True
        embeds_list = []
        all_items_list = []
        if not self.stockpile_values['Heavy Arms']:
            embeds_list.append(discord.Embed(title='<:heavyweaponsicon:1078407453890330634> | Heavy Arms').add_field(name='Empty', value=''))
        else:
            for item in self.stockpile_values['Heavy Arms']:
                all_items_list.append(item)
            embed = discord.Embed(title='<:heavyweaponsicon:1078407453890330634> | Heavy Arms')
            for item_index in range(len(all_items_list)):
                if item_index == 24:
                    embeds_list.append(embed)
                    embed = discord.Embed(title='<:heavyweaponsicon:1078407453890330634> | Heavy Arms')
                embed.add_field(name=list(all_items_list[item_index].keys())[0],
                                value=f'x{list(all_items_list[item_index].values())[0]}')
            embeds_list.append(embed)
        return embeds_list

    def set_heavy_ammunition_page(self):
        self.button_heavy_ammunition.disabled = True
        embeds_list = []
        all_items_list = []
        if not self.stockpile_values['Heavy Arms']:
            embeds_list.append(discord.Embed(title='<:heavyammunitionicon:1078407359405232128> | Heavy Ammunition').add_field(name='Empty', value=''))
        else:
            for item in self.stockpile_values['Heavy Ammunition']:
                all_items_list.append(item)
            embed = discord.Embed(title='<:heavyammunitionicon:1078407359405232128> | Heavy Ammunition')
            for item_index in range(len(all_items_list)):
                if item_index == 24:
                    embeds_list.append(embed)
                    embed = discord.Embed(title='<:heavyammunitionicon:1078407359405232128> | Heavy Ammunition')
                embed.add_field(name=list(all_items_list[item_index].keys())[0],
                                value=f'x{list(all_items_list[item_index].values())[0]}')
            embeds_list.append(embed)
        return embeds_list

    def set_utility_page(self):
        self.button_utility.disabled = True
        embeds_list = []
        all_items_list = []
        if not self.stockpile_values['Utility']:
            embeds_list.append(discord.Embed(title='<:utilityicon:1078407699907215510> | Utility').add_field(name='Empty', value=''))
        else:
            for item in self.stockpile_values['Utility']:
                all_items_list.append(item)
            embed = discord.Embed(title='<:utilityicon:1078407699907215510> | Utility')
            for item_index in range(len(all_items_list)):
                if item_index == 24:
                    embeds_list.append(embed)
                    embed = discord.Embed(title='<:utilityicon:1078407699907215510> | Utility')
                embed.add_field(name=list(all_items_list[item_index].keys())[0],
                                value=f'x{list(all_items_list[item_index].values())[0]}')
            embeds_list.append(embed)
        return embeds_list

    def set_medical_page(self):
        self.button_medical.disabled = True
        embeds_list = []
        all_items_list = []
        if not self.stockpile_values['Medical']:
            embeds_list.append(discord.Embed(title='<:medicalicon:1078407515437543545> | Medical').add_field(name='Empty', value=''))
        else:
            for item in self.stockpile_values['Medical']:
                all_items_list.append(item)
            embed = discord.Embed(title='<:medicalicon:1078407515437543545> | Medical')
            for item_index in range(len(all_items_list)):
                if item_index == 24:
                    embeds_list.append(embed)
                    embed = discord.Embed(title='<:medicalicon:1078407515437543545> | Medical')
                embed.add_field(name=list(all_items_list[item_index].keys())[0],
                                value=f'x{list(all_items_list[item_index].values())[0]}')
            embeds_list.append(embed)
        return embeds_list

    def set_resource_page(self):
        self.button_resource.disabled = True
        embeds_list = []
        all_items_list = []
        if not self.stockpile_values['Resource']:
            embeds_list.append(discord.Embed(title='<:resourceicon:1078408318780964914> | Resource').add_field(name='Empty', value=''))
        else:
            for item in self.stockpile_values['Resource']:
                all_items_list.append(item)
            embed = discord.Embed(title='<:resourceicon:1078408318780964914> | Resource')
            for item_index in range(len(all_items_list)):
                if item_index == 24:
                    embeds_list.append(embed)
                    embed = discord.Embed(title='<:resourceicon:1078408318780964914> | Resource')
                embed.add_field(name=list(all_items_list[item_index].keys())[0],
                                value=f'x{list(all_items_list[item_index].values())[0]}')
            embeds_list.append(embed)
        return embeds_list

    def set_uniforms_page(self):
        self.button_uniforms.disabled = True
        embeds_list = []
        all_items_list = []
        if not self.stockpile_values['Uniforms']:
            embeds_list.append(discord.Embed(title='<:uniformsicon:1078472370551009310> | Uniforms').add_field(name='Empty', value=''))
        else:
            for item in self.stockpile_values['Uniforms']:
                all_items_list.append(item)
            embed = discord.Embed(title='<:uniformsicon:1078472370551009310> | Uniforms')
            for item_index in range(len(all_items_list)):
                if item_index == 24:
                    embeds_list.append(embed)
                    embed = discord.Embed(title='<:uniformsicon:1078472370551009310> | Uniforms')
                embed.add_field(name=list(all_items_list[item_index].keys())[0],
                                value=f'x{list(all_items_list[item_index].values())[0]}')
            embeds_list.append(embed)
        return embeds_list

    def set_vehicles_crates_page(self):
        self.button_vehicles_crates.disabled = True
        embeds_list = []
        all_items_list = []
        if not self.stockpile_values['Vehicles Crates']:
            embeds_list.append(discord.Embed(title='<:vehicleicon:1078410297099948032> | Vehicles Crates').add_field(name='Empty', value=''))
        else:
            for item in self.stockpile_values['Vehicles Crates']:
                all_items_list.append(item)
            embed = discord.Embed(title='<:vehicleicon:1078410297099948032> | Vehicles Crates')
            for item_index in range(len(all_items_list)):
                if item_index == 24:
                    embeds_list.append(embed)
                    embed = discord.Embed(title='<:vehicleicon:1078410297099948032> | Vehicles Crates')
                embed.add_field(name=list(all_items_list[item_index].keys())[0],
                                value=f'x{list(all_items_list[item_index].values())[0]}')
            embeds_list.append(embed)
        return embeds_list

    def set_vehicles_page(self):
        self.button_vehicles.disabled = True
        embeds_list = []
        all_items_list = []
        if not self.stockpile_values['Vehicles']:
            embeds_list.append(discord.Embed(title='<:vehicleicon:1078410297099948032> | Vehicles').add_field(name='Empty', value=''))
        else:
            for item in self.stockpile_values['Vehicles']:
                all_items_list.append(item)
            embed = discord.Embed(title='<:vehicleicon:1078410297099948032> | Vehicles')
            for item_index in range(len(all_items_list)):
                if item_index == 24:
                    embeds_list.append(embed)
                    embed = discord.Embed(title='<:vehicleicon:1078410297099948032> | Vehicles')
                embed.add_field(name=list(all_items_list[item_index].keys())[0],
                                value=f'x{list(all_items_list[item_index].values())[0]}')
            embeds_list.append(embed)
        return embeds_list

    def set_emplacements_crates_page(self):
        self.button_emplacement_crates.disabled = True
        embeds_list = []
        all_items_list = []
        if not self.stockpile_values['Emplacements Crates']:
            embeds_list.append(discord.Embed(title='<:emplacementicon:1078410257556054036> | Emplacements Crates').add_field(name='Empty', value=''))
        else:
            for item in self.stockpile_values['Emplacements Crates']:
                all_items_list.append(item)
            embed = discord.Embed(title='<:emplacementicon:1078410257556054036> | Emplacements Crates')
            for item_index in range(len(all_items_list)):
                if item_index == 24:
                    embeds_list.append(embed)
                    embed = discord.Embed(title='<:emplacementicon:1078410257556054036> | Emplacements Crates')
                embed.add_field(name=list(all_items_list[item_index].keys())[0],
                                value=f'x{list(all_items_list[item_index].values())[0]}')
            embeds_list.append(embed)
        return embeds_list

    def set_emplacements_page(self):
        self.button_emplacement.disabled = True
        embeds_list = []
        all_items_list = []
        if not self.stockpile_values['Emplacements']:
            embeds_list.append(discord.Embed(title='<:emplacementicon:1078410257556054036> | Emplacements').add_field(name='Empty', value=''))
        else:
            for item in self.stockpile_values['Emplacements']:
                all_items_list.append(item)
            embed = discord.Embed(title='<:emplacementicon:1078410257556054036> | Emplacements')
            for item_index in range(len(all_items_list)):
                if item_index == 24:
                    embeds_list.append(embed)
                    embed = discord.Embed(title='<:emplacementicon:1078410257556054036> | Emplacements')
                embed.add_field(name=list(all_items_list[item_index].keys())[0],
                                value=f'x{list(all_items_list[item_index].values())[0]}')
            embeds_list.append(embed)
        return embeds_list

    def activate_all_buttons(self):
        self.button_home.disabled = False
        self.button_all_items.disabled = False
        self.button_small_arms.disabled = False
        self.button_heavy_arms.disabled = False
        self.button_heavy_ammunition.disabled = False
        self.button_utility.disabled = False
        self.button_medical.disabled = False
        self.button_resource.disabled = False
        self.button_uniforms.disabled = False
        self.button_vehicles_crates.disabled = False
        self.button_vehicles.disabled = False
        self.button_emplacement_crates.disabled = False
        self.button_emplacement.disabled = False

    async def all_items_callback(self, interaction: discord.Interaction):
        self.activate_all_buttons()
        embed_list = self.set_all_items_page()
        await interaction.response.edit_message(view=self, embeds=embed_list)

    async def home_page_callback(self, interaction: discord.Interaction):
        self.activate_all_buttons()
        embed = self.set_home_page()
        await interaction.response.edit_message(view=self, embed=embed)

    async def small_arms_items_callback(self, interaction: discord.Interaction):
        self.activate_all_buttons()
        embed_list = self.set_small_arms_page()
        await interaction.response.edit_message(view=self, embeds=embed_list)

    async def heavy_arms_items_callback(self, interaction: discord.Interaction):
        self.activate_all_buttons()
        embed_list = self.set_heavy_arms_page()
        await interaction.response.edit_message(view=self, embeds=embed_list)

    async def heavy_ammunition_items_callback(self, interaction: discord.Interaction):
        self.activate_all_buttons()
        embed_list = self.set_heavy_ammunition_page()
        await interaction.response.edit_message(view=self, embeds=embed_list)

    async def utility_callback(self, interaction: discord.Interaction):
        self.activate_all_buttons()
        embed_list = self.set_utility_page()
        await interaction.response.edit_message(view=self, embeds=embed_list)

    async def medical_callback(self, interaction: discord.Interaction):
        self.activate_all_buttons()
        embed_list = self.set_medical_page()
        await interaction.response.edit_message(view=self, embeds=embed_list)

    async def resource_callback(self, interaction: discord.Interaction):
        self.activate_all_buttons()
        embed_list = self.set_resource_page()
        await interaction.response.edit_message(view=self, embeds=embed_list)

    async def uniforms_callback(self, interaction: discord.Interaction):
        self.activate_all_buttons()
        embed_list = self.set_uniforms_page()
        await interaction.response.edit_message(view=self, embeds=embed_list)

    async def vehicles_crates_callback(self, interaction: discord.Interaction):
        self.activate_all_buttons()
        embed_list = self.set_vehicles_crates_page()
        await interaction.response.edit_message(view=self, embeds=embed_list)

    async def vehicles_callback(self, interaction: discord.Interaction):
        self.activate_all_buttons()
        embed_list = self.set_vehicles_page()
        await interaction.response.edit_message(view=self, embeds=embed_list)

    async def emplacements_crates_callback(self, interaction: discord.Interaction):
        self.activate_all_buttons()
        embed_list = self.set_emplacements_crates_page()
        await interaction.response.edit_message(view=self, embeds=embed_list)

    async def emplacements_callback(self, interaction: discord.Interaction):
        self.activate_all_buttons()
        embed_list = self.set_emplacements_page()
        await interaction.response.edit_message(view=self, embeds=embed_list)