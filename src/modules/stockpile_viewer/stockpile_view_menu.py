import configparser
import sqlite3

import discord

from src.utils import (
    OISOL_HOME_PATH,
    DataFilesPath,
    InterfacesTypes,
    sort_nested_dicts_by_key, FoxholeBuildings, Faction,
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

    def generate_stockpile_embed_data(self, stockpiles_data: list[tuple], user_access_level, group_faction: str) -> dict[str, str | list]:
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
                (access_level,)
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
            cursor = conn.cursor()
            deleted_stockpiles = cursor.executemany(
                'DELETE FROM GroupsStockpilesList WHERE Region == ? AND Subregion == ? AND Code == ? AND AssociationId == ? RETURNING *',
                values_as_query_parameters,
            ).fetchall()
            conn.commit()

        # Print out the stockpiles that were properly removed
        await interaction.response.send_message(
            f'> The following stockpiles were properly deleted:\n```{'\n -'.join(f'{name} | {region} in {subregion} | {code} ({level})' for _, region, subregion, code, name, _, level in deleted_stockpiles)}```',
            ephemeral=True,
        )
