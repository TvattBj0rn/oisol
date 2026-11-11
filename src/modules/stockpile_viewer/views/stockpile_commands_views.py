import configparser
import sqlite3
import warnings

import discord
from discord import Interaction
from thefuzz import process

from src.utils import (
    OISOL_HOME_PATH,
    DataFilesPath,
    chunks,
    validate_stockpile_code,
)


class StockpileCreateModal(discord.ui.Modal, title='Stockpile bulk creation'):
    def __init__(self, user_access_level: int, association_id: str):
        super().__init__()
        self._user_access_level = user_access_level
        self._association_id = association_id

    user_information = discord.ui.TextDisplay(
        content='Separator is `|`\n'
                'Each row a different stockpile, in the following format:\n'
                '`name | code | region | subregion | level | owner`\n\n'
                '`name`: name of your stockpile (required)\n'
                '`code`: code of your stockpile (required)\n'
                '`region`: region name of your stockpile (required)\n'
                '`subregion`: subregion name of your stockpile (required)\n'
                '`level`: level of access of your stockpile (optional)\n'
                '`owner`: discord username owning the stock, you by default (optional)'
        ,
    )

    stockpiles_input = discord.ui.TextInput(
        label='User input',
        style=discord.TextStyle.long,
        required=True,
        placeholder='name | code | region | subregion | level | owner',
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        stockpile_rows = self.stockpiles_input.value.split('\n')

        valid_stockpiles = set()  # set[tuple[str]], ensure no duplicate is added
        invalid_stockpiles = []  # list[tuple[str, str]]

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

        # Iterate on user provided stockpile rows
        for stockpile_raw_info in stockpile_rows:
            split_info = [striped_field.strip() for striped_field in stockpile_raw_info.split('|')]
            name, code, region, subregion, owner, access_level, owner_discord_user = None, None, None, None, None, None, None
            match len(split_info):
                case 4:
                    name, code, region, subregion = split_info
                    access_level = '1'
                    owner = interaction.user.name
                case 5:
                    # Assume that if last is a digit, it is an access level, not a username
                    if split_info[-1].isdigit():
                        name, code, region, subregion, access_level = split_info
                        owner = interaction.user.name
                    else:
                        name, code, region, subregion, owner = split_info
                        access_level = '1'
                case 6:
                    name, code, region, subregion, access_level, owner = split_info
                case _:
                    # Ensure the correct amount of info was given
                    invalid_stockpiles.append((stockpile_raw_info, 'incorrect number of parameters'))
                    continue

            # Validate owner
            if owner is not None and (owner_discord_user := interaction.guild.get_member_named(owner)) is None:
                invalid_stockpiles.append((stockpile_raw_info, 'invalid owner'))
                continue

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

            valid_stockpiles.add(
                (self._association_id, region, subregion, code, name, subregion_to_type[subregion], access_level, owner_discord_user.id if owner_discord_user is not None else None),
            )

        # Add validated stockpiles to the db
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            # Pull all stockpile of the association id network
            network_stockpiles = conn.execute(
                'SELECT * FROM GroupsStockpilesList WHERE AssociationId == ?',
                (self._association_id,),
            ).fetchall()

            # Create set of network stockpiles with necessary info to find duplicates
            existing_keys = {(self._association_id, stockpile_subregion, stockpile_name) for _, _, stockpile_subregion, _, stockpile_name, _, _, _ in network_stockpiles}

            # Find the duplicated stockpiles
            duplicated_stockpiles = [(stockpile[0], stockpile[2], stockpile[4]) for stockpile in valid_stockpiles if (stockpile[2], (stockpile[4]) in existing_keys)]

            cursor = conn.cursor()
            # If duplicates exist, all stockpiles matching the requirements are removed and
            # the single target stockpile is then added with the "normal" process
            if duplicated_stockpiles:
                cursor.executemany(
                    'DELETE FROM GroupsStockpilesList WHERE AssociationId == ? AND Subregion == ? AND Name == ?',
                    duplicated_stockpiles,
                )

            cursor.executemany(
                'INSERT INTO GroupsStockpilesList (AssociationId, Region, Subregion, Code, Name, Type, Level, Owner) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                valid_stockpiles,
            )
            conn.commit()

        response_string = 'The stockpiles were properly added'

        if invalid_stockpiles:
            response_string = f'> The following stockpiles could not be added:\n> - {'\n> - '.join(f'{user_input} -> {invalid_reason}' for user_input, invalid_reason in invalid_stockpiles)}'

        await interaction.response.send_message(response_string, ephemeral=True)


class StockpileRefreshCodesModal(discord.ui.Modal):
    def __init__(self, stockpiles_data: list[tuple], association_id: str):
        super().__init__(timeout=None, title='Stockpiles refresh codes')

        self.__interaction_association_id = association_id
        self.__user_stockpiles_data = stockpiles_data

        stockpiles_string_display = ''
        previous_region = None
        previous_subregion = None

        for region, subregion, code, name, _, _ in stockpiles_data:
            if region != previous_region:
                stockpiles_string_display += f'# {region}\n'
                previous_region = region
            if subregion != previous_subregion:
                stockpiles_string_display += f'## {subregion}\n'
                previous_subregion = subregion
            stockpiles_string_display += f'{name} | `{code}`\n'

        self.add_item(
            discord.ui.TextDisplay(content=stockpiles_string_display),
        )
        self.add_item(
            discord.ui.TextInput(
                label='Update existing codes, one stockpile per row',
                placeholder='111111 222222\n777777 888888\n...',
                style=discord.TextStyle.long,
                id=778866,
            ),
        )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        # refreshed_codes_user_input is guaranteed to be of type discord.TextInput, as referred by the custom id
        refreshed_codes_user_input = self.find_item(778866).value
        all_refreshed_codes = refreshed_codes_user_input.split('\n')

        # This prevent codes the user has no access to, to be overwritten
        existing_user_codes = {stockpile_tuple[2] for stockpile_tuple in self.__user_stockpiles_data}

        valid_refreshes = []
        invalid_refreshes = []

        # Validate retrieved codes, this does not ensure the validated codes are in the database
        for refreshed_code in all_refreshed_codes:
            old_new_codes = refreshed_code.split(' ')
            if (
                len(old_new_codes) != 2
                or validate_stockpile_code(old_new_codes[0]) is not None
                or validate_stockpile_code(old_new_codes[1]) is not None
                or old_new_codes[0] not in existing_user_codes
            ):
                invalid_refreshes.append(refreshed_code)
            else:
                # Add as formatted data ready to be used in SQL query below
                valid_refreshes.append((old_new_codes[1], old_new_codes[0], self.__interaction_association_id))

        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            cursor = conn.cursor()
            # Replace old codes with new codes in a given network (association_id)
            # Currently, it is assumed that the probability of having two different stockpiles with same code is near
            # impossible, with 100 stockpiles on a network, with codes between 0 and 999999, the probability of
            # having two at least two exact matches is 0.00000049496865108080689886%
            # https://www.dcode.fr/loi-binomiale: N=100 & p=1/999999 & K=2, P(X >= 2) = 0.00000049496865108080689886%
            # TLDR: this should not be a problem, even on a large coalition scale with 100 stockpiles simultaneously
            cursor.executemany(
                'UPDATE GroupsStockpilesList SET Code = ? WHERE Code == ? AND AssociationId == ?',
                valid_refreshes,
            )
            conn.commit()

        response_string = ''
        if not invalid_refreshes and not valid_refreshes:
            response_string = 'No codes were given for update'
        else:
            if invalid_refreshes:
                response_string += f'The following code combinations could not be updated:\n- {'\n- '.join(comb for comb in invalid_refreshes)}\n'
            if valid_refreshes:
                response_string += f'The following codes were properly updated:\n- {'\n- '.join(f'{comb[1]} {comb[0]}' for comb in valid_refreshes)}'
        await interaction.response.send_message(response_string, ephemeral=True)


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

        await interaction.response.send_message(
            '> The stockpiles were properly deleted',
            ephemeral=True,
            delete_after=5,
        )


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
                stockpiles_to_delete.append(
                    (selected_subregion[1].removesuffix(')'), selected_subregion[0], self.__association_id,
                     self.__level))

        # Delete all user selected stockpiles from subregion
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            conn.cursor().executemany(
                'DELETE FROM GroupsStockpilesList WHERE Region == ? AND Subregion == ? AND AssociationId == ? AND Level <= ?',
                stockpiles_to_delete,
            )
            conn.commit()

        await interaction.response.send_message(
            '> The stockpiles were properly deleted',
            ephemeral=True,
            delete_after=5,
        )


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

        await interaction.response.send_message(
            '> The stockpiles were properly deleted',
            ephemeral=True,
            delete_after=5,
        )
