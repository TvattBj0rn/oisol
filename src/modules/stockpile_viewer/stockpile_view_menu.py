import configparser
import sqlite3
import warnings

import discord
from discord import Interaction
from thefuzz import process

from src.utils import (
    OISOL_HOME_PATH,
    STOCKPILE_MAIN_INTERFACE_EDITOR_COMPONENT_ID,
    DataFilesPath,
    DiscordIdType,
    Faction,
    InterfacesTypes,
    OisolLogger,
    chunks,
    get_user_access_level,
    sort_nested_dicts_by_key,
)


class StockpilesViewMenu(discord.ui.View):
    """
    Main menu interface of the stockpiles module
    """
    def __init__(self):
        super().__init__(timeout=None)

    @staticmethod
    def generate_stockpile_embed_fields(guild_stockpiles: list[tuple], group_faction: str, emojis_dict: dict) -> list:
        # Group stockpiles by regions
        grouped_stockpiles = {}
        for region, subregion, code, name, building_type, level, owner_id in guild_stockpiles:
            if region not in grouped_stockpiles:
                grouped_stockpiles[region] = {}
            if f'{subregion}_{building_type}' not in grouped_stockpiles[region]:
                grouped_stockpiles[region][f'{subregion}_{building_type}'] = {}
            grouped_stockpiles[region][f'{subregion}_{building_type}'][name] = f'{code}_{level}_{owner_id}'

        # Sort all keys in dict and subdicts by key
        sorted_grouped_stockpiles = sort_nested_dicts_by_key(grouped_stockpiles)

        # Set stockpiles to discord fields format
        embed_fields = []
        for region, v in sorted_grouped_stockpiles.items():
            value_string = ''
            for subregion_type, vv in v.items():
                value_string += f'**{subregion_type.split('_')[0]}** ({emojis_dict[f'{'_'.join(subregion_type.split('_')[1:])}_{group_faction}'.lower()]})\n'
                for name, code_level in vv.items():
                    code, level, owner_id = code_level.split('_')
                    value_string += f'{name} ({level}) **|** {code}'
                    if owner_id != 'None':
                        value_string += f' **|** <@{owner_id}>'
                    value_string += '\n'
                value_string += '\n'
            embed_fields.append({'name': f'‎\n**__{region.upper()}__**', 'value': value_string, 'inline': False})
        return embed_fields

    def generate_stockpile_embed_data(
            self,
            stockpiles_data: list[tuple],
            user_access_level: int,
            group_faction: str,
            emojis_dict: dict,
    ) -> dict[str, str | list]:
        return {
            'title': f'Access Level {user_access_level}',
            'color': Faction[group_faction].value,
            'fields': self.generate_stockpile_embed_fields(stockpiles_data, group_faction, emojis_dict),
        }

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id='Stockpile:View', label='View Stockpiles', emoji='📥')
    async def display_stockpiles(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        OisolLogger('oisol').interface(f'stockpiles view interaction by {interaction.user.name} on {interaction.guild.name}')
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()

            # Retrieve the maximum level of the author's interaction
            user_level = get_user_access_level(
                conn,
                interaction.user.roles,
                str(interaction.guild_id),
                str(interaction.channel_id),
                str(interaction.message.id),
            )

            # Retrieve the interface association id
            association_id = cursor.execute(
                'SELECT AssociationId FROM AllInterfacesReferences WHERE GroupId == ? AND ChannelId == ? AND MessageId == ?',
                (interaction.guild_id, interaction.channel_id, interaction.message.id),
            ).fetchone()[0]

            # Retrieve the interface's stockpiles, using the user's level access level
            access_level_stockpiles = cursor.execute(
                'SELECT Region, Subregion, Code, Name, Type, Level, Owner From GroupsStockpilesList WHERE Level <= ? AND AssociationId == ?',
                (user_level, association_id),
            ).fetchall()
        if not access_level_stockpiles:
            await interaction.response.send_message('> There are currently no stockpiles for your access level', ephemeral=True, delete_after=5)
            return

        # Get group faction
        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')
        group_faction = config.get('regiment', 'faction', fallback='NEUTRAL')

        await interaction.response.send_message(
            embed=discord.Embed.from_dict(self.generate_stockpile_embed_data(
                access_level_stockpiles,
                user_level,
                group_faction,
                interaction.client.app_emojis_dict,
            )),
            ephemeral=True,
        )
        if interaction.guild_id == 1125790880922607616:
            await auto_migrate_stockpile_interface(interaction.guild, interaction.message, interaction.client.app_emojis_dict)

    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id='Stockpile:Roles', label='Edit Roles', emoji='✏️')
    async def edit_interface_roles(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        if interaction.user.name != interaction.message.embeds[0].footer.text:
            await interaction.response.send_message('> Only the creator of the interface can do this action', ephemeral=True, delete_after=5)
            return
        await interaction.response.send_modal(StockpileEditRolesModal(interaction))


    @discord.ui.button(style=discord.ButtonStyle.grey, custom_id='Stockpile:Share', label='Share ID', emoji='🔗')
    async def get_stockpile_association_id(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        """
        Interaction when the Share button is clicked. Since only the user that created the interface can do this action,
        a check is made to ensure the interaction author is the same as the username in the interface footer.
        Then the association id is retrieved and sent in an ephemeral message.
        """
        if interaction.user.name != interaction.message.embeds[0].footer.text:
            await interaction.response.send_message('> Only the creator of the interface can do this action', ephemeral=True, delete_after=5)
            return
        OisolLogger('oisol').interface(f'share id interaction by {interaction.user.name} on {interaction.guild.name}')

        # Retrieve the association id using the interface guild, channel & message ids
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            association_id = conn.cursor().execute(
                'SELECT AssociationId FROM AllInterfacesReferences WHERE GroupId == ? AND ChannelId == ? AND MessageId == ? AND InterfaceType == ?',
                (interaction.guild_id, interaction.channel_id, interaction.message.id, InterfacesTypes.STOCKPILE.value),
            ).fetchone()
        await interaction.response.send_message(f'> The association id is: `{association_id[0]}`', ephemeral=True)



class StockpileEditRolesModal(discord.ui.Modal, title='Edit interface roles'):
    def __init__(self, interaction: discord.Interaction):
        super().__init__()

        # Retrieve existing roles
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            interface_roles = conn.cursor().execute(
                'SELECT Level, DiscordId FROM GroupsInterfacesAccess WHERE GroupId == ? AND ChannelId == ? AND MessageId == ?',
                (interaction.guild_id, interaction.channel_id, interaction.message.id),
            ).fetchall()

        # Create a dict where each existing access level has an associated set of role ids
        level_roles = {}
        for access_level, role_id in interface_roles:
            if access_level not in level_roles:
                level_roles[access_level] = set()
            if role := self.__fetch_role(list(interaction.guild.roles), int(role_id)):
                level_roles[access_level].add(role)

        # Create role edit user input using existing values as default values
        for level_value in range(5, 0, -1):
            self.add_item(discord.ui.Label(
                id=level_value,
                text=f'Level {level_value}',
                description=f'Select the role(s) for level {level_value}/5',
                component=discord.ui.RoleSelect(
                    max_values=25,
                    default_values=level_roles.get(level_value, []),
                ),
            ))

    async def on_submit(self, interaction: discord.Interaction) -> None:
        OisolLogger('oisol').interface(f'stockpiles role edit interaction by {interaction.user.name} on {interaction.guild.name}')
        interface_new_roles = []

        # Create the parameters for the SQL query
        for level_value in range(5, 0, -1):
            roles_select_input = self.find_item(level_value)
            # The case this prevents should not exist, but it properly integrates the typing
            if not (
                isinstance(roles_select_input, discord.ui.Label)
                and isinstance(roles_select_input.component, discord.ui.RoleSelect)
            ):
                continue
            # There can be multiple selected roles, here all available role are added within a generator
            interface_new_roles.extend(
                (interaction.guild_id, interaction.channel_id, interaction.message.id, role.id, DiscordIdType.ROLE.name, level_value)
                for role in roles_select_input.component.values
            )

        # Remove old roles values & add the one submitted in the form
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM GroupsInterfacesAccess WHERE GroupId == ? AND ChannelId == ? AND MessageId == ?',
                (interaction.guild_id, interaction.channel_id, interaction.message.id),
            )

            cursor.executemany(
                'INSERT INTO GroupsInterfacesAccess (GroupId, ChannelId, MessageId, DiscordId, DiscordIdType, Level) VALUES (?, ?, ?, ?, ?, ?)',
                interface_new_roles,
            )

            conn.commit()

        await interaction.response.send_message('> The interface roles were properly updated', ephemeral=True, delete_after=5)


    @staticmethod
    def __fetch_role(guild_roles: list[discord.Role], role_id: int) -> discord.Role | None:
        for role in guild_roles:
            if role.id == role_id:
                return role
        return None

class StockpileCreateModal(discord.ui.Modal, title='Stockpile bulk creation'):
    def __init__(self, user_access_level: int, association_id: str):
        super().__init__()
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
                continue

            # Validate access level
            if not access_level.isdigit() or int(access_level) < 1 or int(access_level) > 5 or int(access_level) > self._user_access_level:
                invalid_stockpiles.append((stockpile_raw_info, 'invalid access level'))
                continue

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

        response_string = 'The stockpiles were properly added'

        if invalid_stockpiles:
            response_string = f'> The following stockpiles could not be added:\n> - {'\n> - '.join(f'{user_input} -> {invalid_reason}' for user_input, invalid_reason in invalid_stockpiles)}'

        await interaction.response.send_message(response_string, ephemeral=True)


class StockpileEditDropDownView(discord.ui.View):
    def __init__(self, stockpiles_info: list[tuple[str]], faction: str, association_id: str, emojis_dict: dict):
        super().__init__(timeout=None)
        self.add_item(StockpileEditDropDownSelect(stockpiles_info, faction, association_id, emojis_dict))


class StockpileEditDropDownSelect(discord.ui.Select):
    def __init__(self, stockpiles_info: list[tuple[str]], faction: str, association_id: str, emoji_dict: dict):
        self.interaction_association_id = association_id
        self.stockpiles_info = stockpiles_info
        self.__emojis_dict = emoji_dict

        # Add user interactions
        options = []
        for region, subregion, code, name, stockpile_type, access_level in stockpiles_info:
            options.append(discord.SelectOption(
                label=f'{name} | {subregion} in {region} | {code} ({access_level})',
                value=f'{region}@{subregion}@{code}@{name}@{access_level}',
                emoji=self.__emojis_dict[f'{stockpile_type}_{faction}'.lower()],
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


class StockpileBulkDeleteModalStockpileDisplay(discord.ui.Modal, title='Stockpile bulk delete'):
    def __init__(
            self,
            stockpiles_info: list[tuple[str]],
            faction: str,
            association_id: str,
            emojis_dict: dict,
    ):
        super().__init__()
        self.__association_id = association_id

        # This will create a list of chunks of 25 stockpiles max.
        options_list = list(chunks([discord.SelectOption(
            label=f'{name} | {subregion} in {region} | {code} ({access_level})',
            value=f'{name}@{region}@{subregion}@{code}@{access_level}',
            emoji=emojis_dict[f'{stockpile_type}_{faction}'.lower()],
        ) for region, subregion, code, name, stockpile_type, access_level in stockpiles_info],
        25))

        # Each chunk is added as a separate field
        for i, chunk in enumerate(options_list):
            self.add_item(discord.ui.Label(
                text='Bulk-delete (stockpile display)',
                description='Select one or more stockpiles to be deleted',
                component=discord.ui.Select(
                    options=chunk,
                    min_values=1,
                    max_values=len(chunk),
                    id=i,
                ),
            ))

    async def on_submit(self, interaction: Interaction) -> None:
        stockpiles_to_delete = []
        for i in range(4):
            if (modal_select := self.find_item(i)) is None:
                break

            for selected_stockpile in modal_select.values:
                name, region, subregion, code, _ = selected_stockpile.split('@')
                stockpiles_to_delete.append((name, region, subregion, code, self.__association_id))

        # Delete all user selected stockpiles
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            conn.cursor().executemany(
                'DELETE FROM GroupsStockpilesList WHERE Name == ? AND Region == ? AND Subregion == ? AND Code == ? AND AssociationId == ?',
                stockpiles_to_delete,
            )
            conn.commit()

        await interaction.response.send_message('> The stockpiles were properly deleted', ephemeral=True, delete_after=5)


class StockpileBulkDeleteModalSubregionDisplay(discord.ui.Modal, title='Stockpile bulk delete'):
    def __init__(
            self,
            stockpiles_info: list[tuple[str]],
            association_id: str,
            emojis_dict: dict,
    ):
        super().__init__()
        self.__association_id = association_id
        self.__level = 1

        # Select all subregion from user stockpiles as dict to keep number of potential stockpiles too
        subregions_dict = {}
        for region, subregion, _, _, _, level in stockpiles_info:
            # Allow to specify a level limit for stockpiles deletions for lower ranks without impacting upper ranks
            if int(level) > self.__level:
                self.__level = int(level)
            if (titled_subregion := f'{subregion} (in {region})') not in subregions_dict:
                subregions_dict[titled_subregion] = 1
            else:
                subregions_dict[titled_subregion] += 1

        # This will create a list of chunks of 25 stockpiles max.
        options_list = list(chunks([discord.SelectOption(
            label=f'{titled_subregion} | {potential_stockpiles} stockpiles would be deleted',
            value=titled_subregion,
            emoji=emojis_dict['region'],
        ) for titled_subregion, potential_stockpiles in subregions_dict.items()],
            25))

        # Each chunk is added as a separate field
        for i, chunk in enumerate(options_list):
            self.add_item(discord.ui.Label(
                text='Bulk-delete (subregion display)',
                description='Select one or more subregion to delete all the stockpiles from',
                component=discord.ui.Select(
                    options=chunk,
                    min_values=1,
                    max_values=len(chunk),
                    id=i,
                ),
            ))

    async def on_submit(self, interaction: Interaction) -> None:
        stockpiles_to_delete = []
        for i in range(4):
            if (modal_select := self.find_item(i)) is None:
                break
            modal_select: discord.ui.Select

            for selected_subregion in modal_select.values:
                selected_subregion = selected_subregion.split(' (in ')
                stockpiles_to_delete.append((selected_subregion[1].removesuffix(')'), selected_subregion[0], self.__association_id, self.__level))

        # Delete all user selected stockpiles from subregion
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            conn.cursor().executemany(
                'DELETE FROM GroupsStockpilesList WHERE Region == ? AND Subregion == ? AND AssociationId == ? AND Level <= ?',
                stockpiles_to_delete,
            )
            conn.commit()

        await interaction.response.send_message('> The stockpiles were properly deleted', ephemeral=True, delete_after=5)


class StockpileBulkDeleteModalRegionDisplay(discord.ui.Modal, title='Stockpile bulk delete'):
    def __init__(
            self,
            stockpiles_info: list[tuple[str]],
            association_id: str,
            emojis_dict: dict,
    ):
        super().__init__()
        self.__association_id = association_id
        self.__level = 1

        # Select all regions from user stockpiles as dict to keep number of potential stockpiles too
        regions_dict = {}
        for region, _, _, _, _, level in stockpiles_info:
            # Allow to specify a level limit for stockpiles deletions for lower ranks without impacting upper ranks
            if int(level) > self.__level:
                self.__level = int(level)
            if region not in regions_dict:
                regions_dict[region] = 1
            else:
                regions_dict[region] += 1

        # This will create a list of chunks of 25 stockpiles max.
        options_list = list(chunks([discord.SelectOption(
            label=f'{region} | {potential_stockpiles} stockpiles would be deleted',
            value=region,
            emoji=emojis_dict['region'],
        ) for region, potential_stockpiles in regions_dict.items()],
            25))

        # Each chunk is added as a separate field
        for i, chunk in enumerate(options_list):
            self.add_item(discord.ui.Label(
                text='Bulk-delete (region display)',
                description='Select one or more region to delete all the stockpiles from',
                component=discord.ui.Select(
                    options=chunk,
                    min_values=1,
                    max_values=len(chunk),
                    id=i,
                ),
            ))

    async def on_submit(self, interaction: Interaction) -> None:
        stockpiles_to_delete = []
        for i in range(4):
            if (modal_select := self.find_item(i)) is None:
                break
            modal_select: discord.ui.Select
            stockpiles_to_delete.extend((region, self.__association_id, self.__level) for region in modal_select.values)

        # Delete all user selected stockpiles from region
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            conn.cursor().executemany(
                'DELETE FROM GroupsStockpilesList WHERE Region == ? AND AssociationId == ? AND Level <= ?',
                stockpiles_to_delete,
            )
            conn.commit()

        await interaction.response.send_message('> The stockpiles were properly deleted', ephemeral=True, delete_after=5)


class StockpileMainInterfaceViewStockpiles(discord.ui.LayoutView):
    def __init__(
            self,
            emojis_dict: dict[str, str],
            stockpile_data: list[tuple],
            guild_faction: str,
            user_access_level: int,
    ):
        super().__init__(timeout=None)
        stockpiles_content = self.__generate_stockpiles_content(emojis_dict, stockpile_data, guild_faction)
        display_stockpiles_container = discord.ui.Container(
                # Title
                discord.ui.TextDisplay(content=f'## Access Level {user_access_level}'),
                discord.ui.Separator(),
                *stockpiles_content,
            )

        # Color cannot be set as named parameter after a star expression
        faction_color_code = Faction[guild_faction].value
        display_stockpiles_container.accent_colour = faction_color_code

        self.add_item(display_stockpiles_container)

    @staticmethod
    def __generate_stockpile_embed_fields(emojis_dict: dict, guild_stockpiles: list[tuple], guild_faction: str) -> list:
        # Group stockpiles by regions
        grouped_stockpiles = {}
        for region, subregion, code, name, building_type, level, owner_id in guild_stockpiles:
            if region not in grouped_stockpiles:
                grouped_stockpiles[region] = {}
            if f'{subregion}_{building_type}' not in grouped_stockpiles[region]:
                grouped_stockpiles[region][f'{subregion}_{building_type}'] = {}
            grouped_stockpiles[region][f'{subregion}_{building_type}'][name] = f'{code}_{level}_{owner_id}'

        # Sort all keys in dict and subdicts by key
        sorted_grouped_stockpiles = sort_nested_dicts_by_key(grouped_stockpiles)

        # Set stockpiles to discord fields format
        regions_strings = []
        for region, v in sorted_grouped_stockpiles.items():
            value_string = f'## **__{region.upper()}__**\n'
            for subregion_type, vv in v.items():
                value_string += f'### **{subregion_type.split('_')[0]}** ({emojis_dict[f'{'_'.join(subregion_type.split('_')[1:])}_{guild_faction}'.lower()]})\n'
                for name, code_level in vv.items():
                    code, level, owner_id = code_level.split('_')
                    value_string += f'- {name} ({level})'
                    if owner_id != 'None':
                        value_string += f' **|** <@{owner_id}>'
                    value_string += f' **|** `{code}`\n'
                value_string += '\n'
            regions_strings.append(value_string)
        return regions_strings

    def __generate_stockpiles_content(
            self,
            emojis_dict: dict[str, str],
            stockpile_data: list[tuple],
            guild_faction: str,
    ) -> list[discord.TextDisplay]:
        merged_strings = []
        buffer = ''

        for region_string in self.__generate_stockpile_embed_fields(emojis_dict, stockpile_data, guild_faction):
            if len(buffer) + len(region_string) >= 4000:
                merged_strings.append(buffer)
                buffer = region_string
            else:
                buffer += region_string
        merged_strings.append(buffer)

        return [discord.ui.TextDisplay(region_string) for region_string in merged_strings]


class StockpileMainInterface(discord.ui.LayoutView):

    __stockpile_main_interface_buttons = discord.ui.ActionRow()

    def __init__(self):
        super().__init__(timeout=None)

    def reset_interface(
            self,
            emojis_dict: dict,
            stockpile_interface_name: str,
            user: discord.User | discord.Member,
            guild_faction: str,
    ) -> None:
        self.clear_items()
        self.add_item(
            discord.ui.Container(
                # Title
                discord.ui.TextDisplay(
                    content=f'## {emojis_dict.get('region')} | Stockpiles | {stockpile_interface_name}',
                ),
                discord.ui.Separator(),
                # Main content
                discord.ui.TextDisplay(
                    content='- **View Stockpiles**: will display more or less stockpiles to the user depending on its level of access to the interface (5-1), 5 being the highest level and 1 the lowest\n'
                            '- **Edit Roles**: available only to the creator of the interface, edit access levels of the interface by assigning role(s) to levels 1 to 5\n'
                            '- **Share ID**: available only to the creator of the interface, get the association ID of the interface to share with other server(s)',
                ),
                discord.ui.Separator(),
                # Interface editor
                discord.ui.TextDisplay(
                    content=f'> Interface editor: {user.mention}',
                    id=STOCKPILE_MAIN_INTERFACE_EDITOR_COMPONENT_ID,
                ),
                discord.ui.Separator(),
                # Buttons row
                self.__stockpile_main_interface_buttons,
                accent_colour=Faction[guild_faction].value,
            ),
        )

    @__stockpile_main_interface_buttons.button(
        style=discord.ButtonStyle.blurple,
        custom_id='view_stockpiles',
        label='View Stockpiles',
        emoji='📥',
    )
    async def display_stockpiles(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        OisolLogger('oisol').interface(
            f'stockpiles view interaction by {interaction.user.name} on {interaction.guild.name}')
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()

            # Retrieve the maximum level of the author's interaction
            user_level = get_user_access_level(
                conn,
                interaction.user.roles,
                str(interaction.guild_id),
                str(interaction.channel_id),
                str(interaction.message.id),
            )

            # Retrieve the interface association id
            association_id = cursor.execute(
                'SELECT AssociationId FROM AllInterfacesReferences WHERE GroupId == ? AND ChannelId == ? AND MessageId == ?',
                (interaction.guild_id, interaction.channel_id, interaction.message.id),
            ).fetchone()[0]

            # Retrieve the interface's stockpiles, using the user's level access level
            access_level_stockpiles = cursor.execute(
                'SELECT Region, Subregion, Code, Name, Type, Level, Owner From GroupsStockpilesList WHERE Level <= ? AND AssociationId == ?',
                (user_level, association_id),
            ).fetchall()
        if not access_level_stockpiles:
            await interaction.response.send_message(
                '> There are currently no stockpiles for your access level',
                ephemeral=True,
                delete_after=5,
            )
            return

        # Get group faction
        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')
        group_faction = config.get('regiment', 'faction', fallback='NEUTRAL')

        await interaction.response.send_message(
            view=StockpileMainInterfaceViewStockpiles(interaction.client.app_emojis_dict, access_level_stockpiles, group_faction, user_level),
            ephemeral=True,
        )

    @__stockpile_main_interface_buttons.button(
        style=discord.ButtonStyle.grey,
        custom_id='stockpiles_edit_roles',
        label='Edit Roles',
        emoji='✏️',
    )
    async def edit_interface_roles(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        # Stockpile main interface contains a single container component with multiple children
        editor_container = next(component for component in interaction.message.components[0].children if component.id == STOCKPILE_MAIN_INTERFACE_EDITOR_COMPONENT_ID)

        # editor_container is of type discord.components.TextDisplay here
        if interaction.user.id != int(editor_container.content.split('<@')[-1].split('>')[0]):
            await interaction.response.send_message(
                '> Only the creator of the interface can do this action',
                ephemeral=True,
                delete_after=5,
            )
            return
        await interaction.response.send_modal(StockpileEditRolesModal(interaction))

    @__stockpile_main_interface_buttons.button(
        style=discord.ButtonStyle.grey,
        custom_id='stockpile_share_id',
        label='Share ID',
        emoji='🔗',
    )
    async def get_stockpile_association_id(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        """
        Interaction when the Share button is clicked. Since only the user that created the interface can do this action,
        a check is made to ensure the interaction author is the same as the username in the interface footer.
        Then the association id is retrieved and sent in an ephemeral message.
        """
        # Stockpile main interface contains a single container component with multiple children
        editor_container = next(component for component in interaction.message.components[0].children if component.id == STOCKPILE_MAIN_INTERFACE_EDITOR_COMPONENT_ID)

        # editor_container is of type discord.components.TextDisplay here
        if interaction.user.id != int(editor_container.content.split('<@')[-1].split('>')[0]):
            await interaction.response.send_message(
                '> Only the creator of the interface can do this action',
                ephemeral=True,
                delete_after=5,
            )
            return
        OisolLogger('oisol').interface(f'share id interaction by {interaction.user.name} on {interaction.guild.name}')

        # Retrieve the association id using the interface guild, channel & message ids
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            association_id = conn.cursor().execute(
                'SELECT AssociationId FROM AllInterfacesReferences WHERE GroupId == ? AND ChannelId == ? AND MessageId == ? AND InterfaceType == ?',
                (interaction.guild_id, interaction.channel_id, interaction.message.id, InterfacesTypes.STOCKPILE.value),
            ).fetchone()
        await interaction.response.send_message(f'> The association id is: `{association_id[0]}`', ephemeral=True)



async def auto_migrate_stockpile_interface(
        guild: discord.Guild,
        interface_message: discord.Message,
        emoji_dict: dict,
) -> None:
    oisol_logger = OisolLogger('oisol')
    new_interface = StockpileMainInterface()

    # Retrieve guild faction, for embed color
    config = configparser.ConfigParser()
    config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{guild.id}.ini')
    guild_faction = config.get('regiment', 'faction', fallback='NEUTRAL')

    # There can only be one embed
    old_interface = interface_message.embeds[0]
    interface_title = old_interface.title.split(' | ')[-1]
    user = guild.get_member_named(old_interface.footer.text)

    if user is None:
        oisol_logger.warning(f'Could not migrate interface on {guild.name}')
        return

    new_interface.reset_interface(emoji_dict, interface_title, user, guild_faction)

    await interface_message.edit(embed=None, view=new_interface)
    oisol_logger.info(f'Stockpile interface was properly migrated on {guild.name}')
