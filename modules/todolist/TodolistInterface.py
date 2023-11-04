import discord
from modules.todolist.CsvHandlerTodolist import CsvHandlerTodolist
from modules.todolist.TodolistEnums import PriorityType
from modules.utils.path import generate_path


EMOTES_CUSTOM_ID = {
    '🇦': 'TodoButtonA',
    '🇧': 'TodoButtonB',
    '🇨': 'TodoButtonC',
    '🇩': 'TodoButtonD',
    '🇪': 'TodoButtonE',
    '🇫': 'TodoButtonF',
    '🇬': 'TodoButtonG',
    '🇭': 'TodoButtonH',
    '🇮': 'TodoButtonI',
    '🇯': 'TodoButtonJ',
    '🇰': 'TodoButtonK',
    '🇱': 'TodoButtonL',
    '🇲': 'TodoButtonM',
    '🇳': 'TodoButtonN',
    '🇴': 'TodoButtonO',
    '🇵': 'TodoButtonP',
    '🇶': 'TodoButtonQ',
    '🇷': 'TodoButtonR',
    '🇸': 'TodoButtonS',
    '🇹': 'TodoButtonT',
    '🇺': 'TodoButtonU',
    '🇻': 'TodoButtonV',
    '🇼': 'TodoButtonW',
    '🇽': 'TodoButtonX',
    '🇾': 'TodoButtonY',
    '🇿': 'TodoButtonZ'
}


class TodolistInterface(discord.ui.View):
    def __init__(self, message: discord.Message, message_embed: dict, csv_keys: list, embed_uuid):
        super().__init__(timeout=None)
        self.csv_keys = csv_keys
        self.message_embed = message_embed
        self.embed_uuid = embed_uuid
        self.message = message
        self.data_dict = CsvHandlerTodolist(self.csv_keys).csv_get_all_data(generate_path(message.guild.id, f'todolists/{embed_uuid}.csv'))
        self.data_list = []

        for key in self.data_dict.keys():
            for elem in self.data_dict[key]:
                self.data_list.append([elem, key])
        self.buttons_list = [TodolistButtonCheckmark(self, self.embed_uuid, self.message_embed, self.data_list, emote, EMOTES_CUSTOM_ID[emote]) for emote in '🇦🇧🇨🇩🇪🇫🇬🇭🇮🇯🇰🇱🇲🇳🇴🇵🇶🇷🇸🇹🇺🇻🇼🇽🇾🇿']
        self.resetInterface()

    def resetInterface(self):
        self.clear_items()
        self.data_dict = CsvHandlerTodolist(self.csv_keys).csv_get_all_data(generate_path(self.message.guild.id, f'todolists/{self.embed_uuid}.csv'))
        self.data_list = []
        for key in self.data_dict.keys():
            for elem in self.data_dict[key]:
                self.data_list.append([elem, key])
        self.interface_embed = self.generateInterfaceEmbed()
        for index in range(len(self.data_list)):
            if index == 24:
                break
            self.add_item(self.buttons_list[index])


    def generateInterfaceEmbed(self) -> discord.Embed:
        generated_embed = discord.Embed(title=self.message_embed['title'])
        alphabet_list = [x for x in 'abcdefghijklmnopqrstuvwxyz']
        global_index = 0
        high_priority = ''

        for order in self.data_dict[PriorityType.HAUTE.value]:
            if global_index > len(alphabet_list):
                break
            high_priority += f':regional_indicator_{alphabet_list[global_index]}: **|** {order}\n'
            global_index += 1

        medium_priority = ''
        for order in self.data_dict[PriorityType.MOYENNE.value]:
            if global_index > len(alphabet_list):
                break
            medium_priority += f':regional_indicator_{alphabet_list[global_index]}: **|** {order}\n'
            global_index += 1

        low_priority = ''
        for order in self.data_dict[PriorityType.BASSE.value]:
            if global_index > len(alphabet_list):
                break
            low_priority += f':regional_indicator_{alphabet_list[global_index]}: **|** {order}\n'
            global_index += 1

        generated_embed.set_footer(text=self.message_embed['footer']['text'])
        generated_embed.add_field(
            name='🔴 **|** Priorité Haute',
            value=high_priority
        )
        generated_embed.add_field(
            name='🟡 **|** Priorité Moyenne',
            value=medium_priority
        )
        generated_embed.add_field(
            name='🟢 **|** Priorité Basse',
            value=low_priority
        )
        return generated_embed


def generateInterfaceEmbed(message_embed: dict, data_dict: dict) -> discord.Embed:
    generated_embed = discord.Embed(title=message_embed['title'])
    alphabet_list = [x for x in 'abcdefghijklmnopqrstuvwxyz']

    global_index = 0
    high_priority = ''
    for order in data_dict[PriorityType.HAUTE.value]:
        if global_index > len(alphabet_list):
            break
        high_priority += f':regional_indicator_{alphabet_list[global_index]}: **|** {order}\n'
        global_index += 1

    medium_priority = ''
    for order in data_dict[PriorityType.MOYENNE.value]:
        if global_index > len(alphabet_list):
            break
        medium_priority += f':regional_indicator_{alphabet_list[global_index]}: **|** {order}\n'
        global_index += 1

    low_priority = ''
    for order in data_dict[PriorityType.BASSE.value]:
        if global_index > len(alphabet_list):
            break
        low_priority += f':regional_indicator_{alphabet_list[global_index]}: **|** {order}\n'
        global_index += 1

    generated_embed.set_footer(text=message_embed['footer']['text'])
    generated_embed.add_field(
        name='🔴 **|** Priorité Haute',
        value=high_priority
    )
    generated_embed.add_field(
        name='🟡 **|** Priorité Moyenne',
        value=medium_priority
    )
    generated_embed.add_field(
        name='🟢 **|** Priorité Basse',
        value=low_priority
    )
    return generated_embed

def listToPriorityDict(data_list: list) -> dict:
    data_dict = {
        'high': [],
        'medium': [],
        'low': []
    }
    for task in data_list:
        data_dict[task[1]].append(task[0])
    return data_dict


class TodolistButtonCheckmark(discord.ui.Button):
    def __init__(self, todolist_interface: TodolistInterface, embed_uuid: str, message_embed: dict, data_list: list, emote: str, custom_id: str):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = emote
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list
        self.custom_id = custom_id

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(list(EMOTES_CUSTOM_ID.keys()).index(str(self.emoji)))
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()
