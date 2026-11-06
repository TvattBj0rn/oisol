import configparser
import sqlite3

import discord
from discord import Interaction, TextStyle

from src.utils import (
    OISOL_HOME_PATH,
    OISOL_LOGGER,
    STOCKPILE_MAIN_INTERFACE_EDITOR_COMPONENT_ID,
    DataFilesPath,
    Faction,
    get_user_access_level,
)
from utils import DiscordIdType, InterfacesTypes


class StockpileEditRolesModal(discord.ui.Modal, title='Edit interface roles'):
    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.__main_interaction = interaction

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
        await OISOL_LOGGER.interface(
            f'stockpiles role edit interaction by {interaction.user.name} on {interaction.guild.name}',
            action_interaction=interaction,
        )
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
                (self.__main_interaction.guild_id, self.__main_interaction.channel_id, self.__main_interaction.message.id, role.id, DiscordIdType.ROLE.name, level_value)
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

        await interaction.response.send_message(
            '> The interface roles were properly updated',
            ephemeral=True,
            delete_after=5,
        )

    @staticmethod
    def __fetch_role(guild_roles: list[discord.Role], role_id: int) -> discord.Role | None:
        for role in guild_roles:
            if role.id == role_id:
                return role
        return None


class StockpileAddAPIModal(discord.ui.Modal, title='Stockpile network API linking'):
    __desc = discord.ui.TextDisplay(content="Add an API token to allow customized interactions on this stockpile network's outside of Discord.\nKeep empty to clear and unlink an existing token")
    __user_token_input_field = discord.ui.TextInput(label='API token', required=False)

    def __init__(
        self,
        guild_id: int,
        channel_id: int,
        message_id: int,
    ):
        super().__init__()

        # Retrieve the interface association id
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            self.__association_id = conn.cursor().execute(
                'SELECT AssociationId FROM AllInterfacesReferences WHERE GroupId == ? AND ChannelId == ? AND MessageId == ?',
                (guild_id, channel_id, message_id),
            ).fetchone()[0]

        # Retrieve a potentially existing token
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol_core.db') as conn:
            self.__token = conn.cursor().execute(
                'SELECT Token FROM NetworkTokens WHERE AuthorizedNetwork == ?',
                (self.__association_id,),
            ).fetchone()

        if self.__token is not None:
            self.__token = self.__token[0]
            self.__user_token_input_field.default = self.__token


    async def __add_api_token(self, interaction: Interaction, submitted_user_token: str) -> None:
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol_core.db') as conn_oisol_core:
            cursor_oisol_core = conn_oisol_core.cursor()
            matching_tokens = cursor_oisol_core.execute(
                'SELECT Token FROM NewTokensWaitList WHERE Token == ?',
                (submitted_user_token,),
            ).fetchall()

            # Ensure user provided token validity
            match len(matching_tokens):
                # Valid single token in the proper table
                case 1:
                    # Remove the token from the wait list and add it to the validated list
                    cursor_oisol_core.execute(
                        'DELETE FROM NewTokensWaitList WHERE Token == ?',
                        (submitted_user_token,),
                    )
                    conn_oisol_core.execute(
                        'INSERT INTO NetworkTokens (Token, AuthorizedNetwork) VALUES (?, ?)',
                        (submitted_user_token, self.__association_id),
                    )
                    conn_oisol_core.commit()
                # 0 -> Invalid token
                # More than one token -> this case should not be possible
                case _:
                    if len(matching_tokens) > 1:
                        OISOL_LOGGER.warning(f'A duplicated token was found: {submitted_user_token}')
                    await interaction.response.send_message(
                        '> The token you provided is invalid, you can try to generate another one from the API',
                        ephemeral=True,
                        delete_after=5,
                    )
                    return
        await interaction.response.send_message(
            '> The token was properly added, the stockpile network can now be interacted with using the API',
            ephemeral=True,
            delete_after=5,
        )

    async def __remove_api_token(self, interaction: Interaction) -> None:
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol_core.db') as conn:
            delete_result = conn.cursor().execute(
                'DELETE FROM NetworkTokens WHERE Token == ? AND AuthorizedNetwork == ? RETURNING *',
                (self.__token, self.__association_id),
            ).fetchall()
        if not delete_result:
            await interaction.response.send_message(
                '> This network was not linked to the API, so nothing happened',
                ephemeral=True,
                delete_after=5,
            )
        else:
            await interaction.response.send_message(
                '> The network was properly unlinked to the API',
                ephemeral=True,
                delete_after=5,
            )

    async def on_submit(self, interaction: Interaction) -> None:
        if self.__user_token_input_field.value:
            await self.__add_api_token(interaction, self.__user_token_input_field.value)
        else:
            await self.__remove_api_token(interaction)


class StockpileEditInterfaceContentModal(discord.ui.Modal, title='Edit interface content'):
    __desc = discord.ui.TextDisplay(content='Edit the interface title and description.')
    __user_title_edit_field = discord.ui.TextInput(label='Edit Title', required=False)
    __user_description_edit_field = discord.ui.TextInput(
        label='Edit description (support markdown)',
        style=TextStyle.long,
        required=False,
    )

    def __init__(self, main_interaction: discord.Interaction):
        super().__init__()

        self.__main_interface_interaction = main_interaction
        self.__user_title_edit_field.default = main_interaction.message.components[0].children[0].content.split('| ')[2]
        self.__user_description_edit_field.default = main_interaction.message.components[0].children[2].content


    async def on_submit(self, interaction: Interaction) -> None:
        interface_owner = self.__main_interface_interaction.message.components[0].children[4].content.split('<@')[1].removesuffix('>')
        interface_color = self.__main_interface_interaction.message.components[0].accent_colour

        new_title = self.__user_title_edit_field.value
        new_desc = self.__user_description_edit_field.value

        # Discord does not allow no chars titles/descs, this ensures it stays a possibility
        if len(new_title) < 1:
            new_title += 'ㅤ'
        if len(new_desc) < 1:
            new_desc += 'ㅤ'

        updated_interface = StockpileMainInterface()
        updated_interface.reset_interface(
            self.__main_interface_interaction.client.app_emojis_dict,
            new_title,
            interface_owner,
            interface_color.value,
            new_desc,
        )
        await self.__main_interface_interaction.message.edit(view=updated_interface)
        await interaction.response.send_message('> The interface was properly edited', ephemeral=True, delete_after=5)

class StockpileMainInterfaceEditorPanel(discord.ui.LayoutView):
    __editor_panel_buttons = discord.ui.ActionRow()

    def __init__(self, main_interface_interaction: discord.Interaction):
        super().__init__(timeout=None)
        self.__main_interaction = main_interface_interaction

        self.clear_items()
        self.add_item(
            discord.ui.Container(
                # Title
                discord.ui.TextDisplay(content='## Editor Panel'),
                discord.ui.Separator(),
                # Main content
                discord.ui.TextDisplay(
                    content='- **Edit Interface Content**: edit title and description of the interface\n'
                            '- **Edit Roles**: edit access levels of the interface by assigning role(s) to levels 1 to 5\n'
                            '- **Network Settings**: View connected stockpiles, share ID and edit the API token\n',
                ),
                discord.ui.Separator(),
                # Buttons row
                self.__editor_panel_buttons,
                accent_colour=discord.Colour.red(),
            ),
        )

    @__editor_panel_buttons.button(
        style=discord.ButtonStyle.blurple,
        custom_id='stockpiles_edit_interface',
        label='Interface Content Settings',
        emoji='✏️',
    )
    async def edit_interface_content(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        await interaction.response.send_modal(StockpileEditInterfaceContentModal(self.__main_interaction))

    @__editor_panel_buttons.button(
        style=discord.ButtonStyle.blurple,
        custom_id='stockpiles_edit_roles',
        label='Roles Settings',
        emoji='🔰',
    )
    async def edit_interface_roles(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        await interaction.response.send_modal(StockpileEditRolesModal(self.__main_interaction))

    @__editor_panel_buttons.button(
        style=discord.ButtonStyle.blurple,
        custom_id='stockpile_edit_network',
        label='Network Settings',
        emoji='📡',
    )
    async def get_stockpile_association_id(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        """
        Interaction when the Share button is clicked. Since only the user that created the interface can do this action,
        a check is made to ensure the interaction author is the same as the username in the interface footer.
        Then the association id is retrieved and sent in an ephemeral message.
        """
        await OISOL_LOGGER.interface(
            f'share id interaction by {interaction.user.name} on {interaction.guild.name}',
            action_interaction=interaction,
        )

        # Retrieve the association id using the interface guild, channel & message ids
        with sqlite3.connect(OISOL_HOME_PATH / 'oisol.db') as conn:
            association_id = conn.cursor().execute(
                'SELECT AssociationId FROM AllInterfacesReferences WHERE GroupId == ? AND ChannelId == ? AND MessageId == ? AND InterfaceType == ?',
                (self.__main_interaction.guild_id, self.__main_interaction.channel_id, self.__main_interaction.message.id, InterfacesTypes.STOCKPILE.value),
            ).fetchone()
        await interaction.response.send_message(f'> The association id is: `{association_id[0]}`', ephemeral=True)

    @__editor_panel_buttons.button(
        style=discord.ButtonStyle.blurple,
        custom_id='stockpile_api_settings',
        label='Stockpile Network API Settings',
        emoji='🤖',
    )
    async def api_settings(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        OISOL_LOGGER.api_log(f'API token interaction by {interaction.user.name} on {interaction.guild.name}')

        await interaction.response.send_modal(StockpileAddAPIModal(
            self.__main_interaction.guild_id,
            self.__main_interaction.channel_id,
            self.__main_interaction.message.id,
        ))


class StockpileMainInterfaceViewStockpiles(discord.ui.LayoutView):
    def __init__(
        self,
        stockpile_data: str,
        guild_faction: str,
        user_access_level: int,
    ):
        super().__init__(timeout=None)
        stockpiles_content = discord.ui.TextDisplay(stockpile_data)
        display_stockpiles_container = discord.ui.Container(
            # Title
            discord.ui.TextDisplay(content=f'## Access Level {user_access_level}'),
            discord.ui.Separator(),
            stockpiles_content,
        )

        # Color cannot be set as named parameter after a star expression
        faction_color_code = Faction[guild_faction].value
        display_stockpiles_container.accent_colour = faction_color_code

        self.add_item(display_stockpiles_container)


class StockpileMainInterface(discord.ui.LayoutView):
    __stockpile_main_interface_buttons = discord.ui.ActionRow()

    def __init__(self):
        super().__init__(timeout=None)

    @staticmethod
    def __generate_stockpile_embed_fields(
        emojis_dict: dict,
        guild_stockpiles: list[tuple],
        guild_faction: str,
    ) -> list[str]:
        # List of formatted stockpiles, with each string in the list corresponding to a foxhole region
        region_strings = []

        # Region string can be updated on multiple loop iterations, as there can be multiple stockpiles on a given subregion,
        # hence the var declaration outside the loop
        region_string = ''

        # Buffers for titles reset
        previous_region = None
        previous_subregion = None

        for region_name, subregion_name, code, stockpile_name, stockpile_building_type, access_level, owner_id in guild_stockpiles:
            # Main region changed, new "field"
            if region_name != previous_region:
                region_strings.append(region_string)
                region_string = f'## __{region_name.upper()}__\n'
            # Subregion change, new subtitle
            if subregion_name != previous_subregion:
                region_string += f'### {subregion_name} ({emojis_dict[f'{stockpile_building_type}_{guild_faction}'.lower()]})\n'

            # Singular stockpile addition, owner can be null, order is Name (level) | owner id (optional) | code
            region_string += f'> {stockpile_name} ({access_level})'
            if owner_id:
                region_string += f' | <@{owner_id}>'
            region_string += f' | `{code}`\n'

            # Update buffers
            previous_region = region_name
            previous_subregion = subregion_name

        # Ensure the last region worked on is also added
        region_strings.append(region_string)

        return region_strings

    def reset_interface(
        self,
        emojis_dict: dict,
        stockpile_interface_name: str,
        user: discord.User | discord.Member | str,
        guild_faction: str | int,
        stockpile_interface_desc: str | None = None,
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
                # By default, the content is as below, but the user can pass a custom content here
                discord.ui.TextDisplay(
                    content=('- **View Stockpiles**: will display more or less stockpiles to the user depending on its level of access to the interface (5-1), 5 being the highest level and 1 the lowest\n'
                            '- **Editor Panel**: available only to the creator of the interface, contains various settings (Title, Description, Roles, ...)\n')
                    if stockpile_interface_desc is None else stockpile_interface_desc,
                ),
                discord.ui.Separator(),
                # Interface editor
                discord.ui.TextDisplay(
                    content=f'> Interface editor: {f'<@{user}>' if isinstance(user, str) else user.mention}',
                    id=STOCKPILE_MAIN_INTERFACE_EDITOR_COMPONENT_ID,
                ),
                discord.ui.Separator(),
                # Buttons row
                self.__stockpile_main_interface_buttons,
                accent_colour=Faction[guild_faction].value if isinstance(guild_faction, str) else guild_faction,
            ),
        )

    @__stockpile_main_interface_buttons.button(
        style=discord.ButtonStyle.blurple,
        custom_id='view_stockpiles',
        label='View Stockpiles',
        emoji='📥',
    )
    async def display_stockpiles(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
        await OISOL_LOGGER.interface(
            f'stockpiles view interaction by {interaction.user.name} on {interaction.guild.name}',
            action_interaction=interaction,
        )
        await interaction.response.defer(ephemeral=True)

        # TODO: TMP check if the API settings button exists, and reset the interface otherwise
        # for c_check in interaction.message.components[0].children:
        #     if isinstance(c_check, discord.ActionRow) and not any(button for button in c_check.children if button.label == 'API Settings'):
        #         await OISOL_LOGGER.interface(f'stockpiles migration interaction by {interaction.user.name} on {interaction.guild.name}')
        #         for c in interaction.message.components[0].children:
        #             if isinstance(c, discord.TextDisplay) and c.id == STOCKPILE_MAIN_INTERFACE_EDITOR_COMPONENT_ID:
        #                 user_editor = c.content.removesuffix('>').removeprefix('> Interface editor: <@')
        #             # DEV OISOL
        #             if isinstance(c, discord.TextDisplay) and '## <:region:1443657827724820621> | Stockpiles | ' in c.content:
        #                 interface_title = c.content.removeprefix('## <:region:1443657827724820621> | Stockpiles | ')
        #             # OISOL
        #             if isinstance(c, discord.TextDisplay) and '## <:region:1443660028098646218> | Stockpiles | ' in c.content:
        #                 interface_title = c.content.removeprefix('## <:region:1443660028098646218> | Stockpiles | ')
        #
        #         faction_color = interaction.message.components[0].accent_colour
        #
        #         # This should not raise any errors as these var should be guaranteed
        #         # If not it should raise an error instead of overwriting data
        #         new_interface = StockpileMainInterface()
        #         new_interface.reset_interface(
        #             interaction.client.app_emojis_dict,
        #             interface_title,
        #             user_editor,
        #             faction_color.value)
        #         await interaction.message.edit(view=new_interface)

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
                'SELECT Region, Subregion, Code, Name, Type, Level, Owner From GroupsStockpilesList WHERE Level <= ? AND AssociationId == ? ORDER BY Region ASC, Subregion ASC, Name ASC',
                (user_level, association_id),
            ).fetchall()

        if not access_level_stockpiles:
            await interaction.followup.send(
                '> There are currently no stockpiles for your access level',
                ephemeral=True,
            )
            return

        # Get group faction
        config = configparser.ConfigParser()
        config.read(OISOL_HOME_PATH / DataFilesPath.CONFIG_DIR.value / f'{interaction.guild_id}.ini')
        group_faction = config.get('regiment', 'faction', fallback='NEUTRAL')

        # Create list of formatted strings, each string containing the stockpiles of a specific region
        stockpiles_regions_strings = self.__generate_stockpile_embed_fields(
            interaction.client.app_emojis_dict,
            access_level_stockpiles,
            group_faction,
        )

        # Merge strings into chunks of 3900 characters, each chunk will be a separate message due to discord limitation
        merged_strings = []
        buffer = ''
        for region_string in stockpiles_regions_strings:
            if len(buffer) + len(region_string) >= 3900:
                merged_strings.append(buffer)
                buffer = region_string
            else:
                buffer += region_string
        merged_strings.append(buffer)

        # Send a view per message
        for view_content in merged_strings:
            await interaction.followup.send(
                view=StockpileMainInterfaceViewStockpiles(
                    view_content,
                    group_faction,
                    user_level,
                ),
                ephemeral=True,
                silent=True,
            )

    @__stockpile_main_interface_buttons.button(
        style=discord.ButtonStyle.grey,
        custom_id='editor_panel',
        label='Editor Panel',
        emoji='🛠️',
    )
    async def display_editor_panel(self, interaction: discord.Interaction, _button: discord.ui.Button) -> None:
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

        await interaction.response.send_message(
            view=StockpileMainInterfaceEditorPanel(main_interface_interaction=interaction),
            ephemeral=True,
        )
