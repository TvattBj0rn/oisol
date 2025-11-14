import configparser
import sqlite3
import warnings

import discord

from thefuzz import process

from src.utils import (
    OISOL_HOME_PATH,
    DataFilesPath,
    Faction,
    FoxholeBuildings,
    InterfacesTypes,
    OisolLogger,
    sort_nested_dicts_by_key, REGIONS_TYPES,
)


class StockpilesViewMenu(discord.ui.View):
    """
    Main menu interface of the stockpiles module
    """
    def __init__(self):
        super().__init__(timeout=None)

    @staticmethod
    def generate_stockpile_embed_fields(guild_stockpiles: list[tuple], group_faction: str) -> list:
        # Group stockpiles by regions
        grouped_stockpiles = {}
        for region, subregion, code, name, building_type, level in guild_stockpiles:
            if region not in grouped_stockpiles:
                grouped_stockpiles[region] = {}
            if f'{subregion}_{building_type}' not in grouped_stockpiles[region]:
                grouped_stockpiles[region][f'{subregion}_{building_type}'] = {}
            grouped_stockpiles[region][f'{subregion}_{building_type}'][name] = f'{code}_{level}'

        # Sort all keys in dict and subdicts by key
        sorted_grouped_stockpiles = sort_nested_dicts_by_key(grouped_stockpiles)

        # Set stockpiles to discord fields format
        embed_fields = []
        for region, v in sorted_grouped_stockpiles.items():
            value_string = ''
            for subregion_type, vv in v.items():
                value_string += f'**{subregion_type.split('_')[0]}** ({FoxholeBuildings[f'{'_'.join(subregion_type.split('_')[1:])}_{group_faction}'].value})\n'
                for name, code_level in vv.items():
                    code, level = code_level.split('_')
                    value_string += f'{name} **|** ({level}) {code}\n'
                value_string += '\n'
            embed_fields.append({'name': f'‎\n**__{region.upper()}__**', 'value': value_string, 'inline': True})
        return embed_fields

    def generate_stockpile_embed_data(self, stockpiles_data: list[tuple], user_access_level: int, group_faction: str) -> dict[str, str | list]:
        return {
            'title': f'Access Level {user_access_level}',
            'color': Faction[group_faction].value,
            'fields': self.generate_stockpile_embed_fields(stockpiles_data, group_faction),
        }

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='Stockpile:View', label='View Stockpiles', emoji='📥')
    async def display_stockpiles(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            interface_access_levels = dict(cursor.execute(
                'SELECT DiscordId, Level FROM GroupsInterfacesAccess WHERE GroupId == ? AND ChannelId == ? AND MessageId == ?',
                (interaction.guild_id, interaction.channel_id, interaction.message.id),
            ).fetchall())
            access_level = 5
            # Search for matching ids between interface roles and user roles
            for user_role_id in [str(role.id) for role in interaction.user.roles]:
                if user_role_id in interface_access_levels:
                    access_level = interface_access_levels[user_role_id]
                    # No need to continue searching when max possible level is found
                    if interface_access_levels[user_role_id] == 1:
                        break

            access_level_stockpiles = cursor.execute(
                'SELECT Region, Subregion, Code, Name, Type, Level From GroupsStockpilesList WHERE Level >= ?',
                (access_level,),
            ).fetchall()
        if not access_level_stockpiles:
            await interaction.response.send_message('> There are currently no stockpiles for your access level', ephemeral=True, delete_after=5)
            return
        # Get group faction
        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')
        group_faction = config.get('regiment', 'faction', fallback='NEUTRAL')

        await interaction.response.send_message(embed=discord.Embed.from_dict(self.generate_stockpile_embed_data(access_level_stockpiles, access_level, group_faction)), ephemeral=True)


    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='Stockpile:Share', label='Share ID', emoji='🔗')
    async def get_stockpile_association_id(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        """
        Interaction when the Share button is clicked. Since only the user that created the interface can do this action,
        a check is made to ensure the interaction author is the same as the username in the interface footer.
        Then the association id is retrieved and sent in an ephemeral message.
        """
        if interaction.user.name != interaction.message.embeds[0].footer.text:
            await interaction.response.send_message('> Only the creator of the interface can do this action', ephemeral=True)
        else:
            with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
                association_id = conn.cursor().execute(
                    'SELECT AssociationId FROM AllInterfacesReferences WHERE GroupId == ? AND ChannelId == ? AND MessageId == ? AND InterfaceType == ?',
                    (interaction.guild_id, interaction.channel_id, interaction.message.id, InterfacesTypes.STOCKPILE.value),
                ).fetchone()
            await interaction.response.send_message(f'> The association id is: `{association_id[0]}`', ephemeral=True)


class StockpileCreateModal(discord.ui.Modal, title='Stockpile bulk creation'):
    def __init__(self, user_access_level: int, association_id: str):
        super().__init__()
        self.logger = OisolLogger('oisol')

        self._user_access_level = user_access_level
        self._association_id = association_id

    user_information = discord.ui.TextDisplay(
        content='Separator is `|`\n'
                'Each row a different stockpile, in the following format:\n'
                '`name | code | region | subregion | level`\n\n'
                '`name`: name of your stockpile (required)\n'
                '`code`: code of your stockpile (required)\n'
                '`region`: region name of your stockpile (required)\n'
                '`subregion`: subregion name of your stockpile (required)\n'
                '`level`: level of access of your stockpile (optional)\n',
    )

    stockpiles_input = discord.ui.TextInput(
        label='User input',
        style=discord.TextStyle.long,
        required=True,
        placeholder='name | code | region | subregion | level',
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        stockpile_rows = self.stockpiles_input.value.split('\n')

        valid_stockpiles = [] # list[tuple[str]]
        invalid_stockpiles = [] # list[tuple[str, str]]

        # Retrieve shard of the guild the command is run from
        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')
        guild_shard = config.get('default', 'shard', fallback='ABLE')

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            region_subregion_list = conn.cursor().execute(
                'SELECT Region, Subregion, Type FROM StockpilesZones WHERE Shard == ?',
                (guild_shard,),
            ).fetchall()
        subregions_to_region = {subregion: region for region, subregion, _ in region_subregion_list}
        subregion_to_type = {subregion: subregion_type for _, subregion, subregion_type in region_subregion_list}
        shard_all_subregions = list(subregions_to_region)

        for stockpile_raw_info in stockpile_rows:
            split_info = [striped_field.strip() for striped_field in stockpile_raw_info.split('|')]

            # Ensure the correct amount of info was given
            if len(split_info) != 5:
                invalid_stockpiles.append((stockpile_raw_info, 'incorrect number of parameters'))
                continue
            name, code, region, subregion, access_level = split_info

            # Validate code
            if len(code) != 6 or not code.isdigit():
                invalid_stockpiles.append((stockpile_raw_info, 'invalid code'))

            # Validate access level
            if not access_level.isdigit() or int(access_level) < 1 or int(access_level) > 5 or int(access_level) < self._user_access_level:
                invalid_stockpiles.append((stockpile_raw_info, 'invalid access level'))

            # For both region & subregion there is not proper validation, only a match to the most likely name
            # Match subregion, currently no need to match region as well
            subregion = process.extract(subregion, shard_all_subregions)[0][0]
            region = subregions_to_region[subregion]

            valid_stockpiles.append(
                (self._association_id, region, subregion, code, name, subregion_to_type[subregion], access_level),
            )

        # Add validated stockpiles to the db
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            conn.cursor().executemany(
                'INSERT INTO GroupsStockpilesList (AssociationId, Region, Subregion, Code, Name, Type, Level) VALUES (?, ?, ?, ?, ?, ?, ?)',
                valid_stockpiles,
            )
            conn.commit()

        await interaction.response.send_message('> The stockpiles were properly added', ephemeral=True, delete_after=5)


class StockpileEditDropDownView(discord.ui.View):
    def __init__(self, stockpiles_info: list[tuple[str]], faction: str, association_id: str):
        super().__init__(timeout=None)
        self.add_item(StockpileEditDropDownSelect(stockpiles_info, faction, association_id))


class StockpileEditDropDownSelect(discord.ui.Select):
    def __init__(self, stockpiles_info: list[tuple[str]], faction: str, association_id: str):
        self.interaction_association_id = association_id
        self.stockpiles_info = stockpiles_info

        # Add user interactions
        options = []
        for region, subregion, code, name, stockpile_type, access_level in stockpiles_info:
            options.append(discord.SelectOption(
                label=f'{name} | {subregion} in {region} | {code} ({access_level})',
                value=f'{region}@{subregion}@{code}@{name}@{access_level}',
                emoji=FoxholeBuildings[f'{stockpile_type}_{faction}'].value,
            ))

        super().__init__(placeholder='Choose the stockpiles you want to edit', options=options, max_values=len(options) if len(options) < 5 else 5)

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_modal(StockpileEditModal(
            [selected_option.split('@') for selected_option in self.values],
            self.interaction_association_id,
        ))


class StockpileEditModal(discord.ui.Modal, title='Refresh stockpiles code'):
    def __init__(self, selected_stockpiles_data: list[list[str]], association_id: str):
        super().__init__()
        self.logger = OisolLogger('oisol')
        self._selected_stockpiles_data = selected_stockpiles_data
        self._association_id = association_id
        self._selected_stockpiles_buffer = {}

        for region, subregion, code, name, level in self._selected_stockpiles_data:
            stockpile_label = f'{name} ({level}) | {subregion}, {region}'

            # discord API prevent labels lengths over 45 chars
            if len(stockpile_label) >= 45:
                stockpile_label = f'{name} ({level})'

            text_input = discord.ui.TextInput(
                label=stockpile_label,
                style=discord.TextStyle.short,
                required=True,
                default=code,
            )

            # save stockpile infos to be used on submit
            self._selected_stockpiles_buffer[text_input.custom_id.__hash__()] = [association_id, region, subregion, name]

            self.add_item(text_input)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        invalid_codes = []
        valid_query_codes = []
        for modal_item in self.children:
            # Ensure the current item is a user input
            if not isinstance(modal_item, discord.ui.TextInput):
                continue
            new_stockpile_code = modal_item.value

            # Ensure the user provided code is valid
            if len(new_stockpile_code) != 6 or not new_stockpile_code.isdigit():
                invalid_codes.append((new_stockpile_code, modal_item.label))
                continue

            # This action raise a deprecation warning and provide a replacement that has not been implemented yet
            # This warning cannot be avoided nor fixed in the current discord-py version (~=2.6)
            with warnings.catch_warnings(action='ignore'):
                stockpile_info = self._selected_stockpiles_buffer[modal_item.custom_id.__hash__()]

            valid_query_codes.append((new_stockpile_code, *stockpile_info))

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            conn.cursor().executemany(
                'UPDATE GroupsStockpilesList SET Code = ? WHERE AssociationId == ? AND Region == ? AND Subregion == ? AND Name == ?',
                valid_query_codes,
            )
            conn.commit()

        response_string = '> '
        if valid_query_codes:
            response_string += f'The following stockpiles codes were properly updated:\n> - {'\n> - '.join(f'{name} ({code}) | {subregion} in {region}' for code, _, region, subregion, name in valid_query_codes)}\n'
        if invalid_codes:
            response_string += f'The provided new codes are invalid for the following stockpiles:\n> - {'\n- '.join(f'{code}, {label}' for code, label in invalid_codes)}'

        await interaction.response.send_message(response_string, ephemeral=True)


class StockpileBulkDeleteDropDownView(discord.ui.View):
    def __init__(self, stockpiles_info: list[tuple[str]], faction: str, association_id: str):
        super().__init__(timeout=None)
        self.add_item(StockpileBulkDeleteDropDownSelect(stockpiles_info, faction, association_id))


class StockpileBulkDeleteDropDownSelect(discord.ui.Select):
    def __init__(self, stockpiles_info: list[tuple[str]], faction: str, association_id: str):
        self.interaction_association_id = association_id

        options = []
        for region, subregion, code, name, stockpile_type, access_level in stockpiles_info:
            options.append(discord.SelectOption(
                label=f'{name} | {subregion} in {region} | {code} ({access_level})',
                value=f'{name}@{region}@{subregion}@{code}@{access_level}',
                emoji=FoxholeBuildings[f'{stockpile_type}_{faction}'].value,
            ))

        super().__init__(placeholder='Choose the stockpiles you want to delete', options=options, max_values=len(options) if len(options) < 25 else 25)

    async def callback(self, interaction: discord.Interaction) -> None:
        values_as_query_parameters = []
        for value in self.values:
            name, region, subregion, code, level = value.split('@')
            values_as_query_parameters.append((region, subregion, code, self.interaction_association_id))

        # Delete all user selected stockpiles
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            conn.cursor().executemany(
                'DELETE FROM GroupsStockpilesList WHERE Region == ? AND Subregion == ? AND Code == ? AND AssociationId == ?',
                values_as_query_parameters,
            )
            conn.commit()

        await interaction.response.send_message('> The stockpiles were properly deleted', ephemeral=True, delete_after=5)
