import configparser

import discord

from src.utils import Faction


class ConfigViewInterface(discord.ui.LayoutView):
    def __init__(self, server_config: configparser.ConfigParser):
        super().__init__(timeout=None)
        # Retrieve wanted data from the config file
        self.__shard = server_config.get('default', 'shard', fallback='ABLE')
        self.__faction = server_config.get('regiment', 'faction', fallback='NEUTRAL')
        self.__logging_channel_id = server_config.getint('logging', 'channel', fallback=0)
        self.__recruit_role_id = server_config.getint('register', 'recruit_id', fallback=0)
        self.__recruit_symbol = server_config.get('register', 'input', fallback=None)
        self.__promoted_recruit_symbol = server_config.get('register', 'output', fallback=None)
        self.__does_promotion_gives_tag = server_config.getboolean('register', 'promoted_get_tag', fallback=False)

        # Create the interface
        self.add_item(discord.ui.Container(
            # Title
            discord.ui.TextDisplay(content='# OISOL server configuration'),
            discord.ui.Separator(),
            # Shard + Faction
            discord.ui.TextDisplay(content=f'### Game server: `{self.__shard}`\n### Faction: `{self.__faction}`'),
            discord.ui.Separator(),
            # Logging channel
            discord.ui.TextDisplay(content=f'### Current logging channel: {f'<#{self.__logging_channel_id}>' if self.__logging_channel_id != 0 else '`Not set`'}'),
            discord.ui.Separator(),
            # Register
            discord.ui.TextDisplay(content='## Register configuration\n'
                                           f'### Recruit role: {f'<@&{self.__recruit_role_id}>' if self.__recruit_role_id != 0 else '`Not set`'}\n'
                                           f'### Recruit symbol: {f'`{self.__recruit_symbol}`' if self.__recruit_symbol else '`Not set`'}\n'
                                           f'### Role above recruit symbol: {f'`{self.__promoted_recruit_symbol}`' if self.__promoted_recruit_symbol else '`Not set`'}\n'
                                           f'### Does promotion gives tag: `{'Yes' if self.__does_promotion_gives_tag else 'No'}`',
                                   ),
            accent_colour = Faction[self.__faction].value,
        ))
