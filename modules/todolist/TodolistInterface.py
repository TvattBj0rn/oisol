import discord
# from modules.todolist import TodolistButtons
# from modules.todolist.TodolistButtons import TodolistButtonA, TodolistButtonB, TodolistButtonC, TodolistButtonD, TodolistButtonE, TodolistButtonF, TodolistButtonG, TodolistButtonH, TodolistButtonI, TodolistButtonJ, TodolistButtonK, TodolistButtonL, TodolistButtonM, TodolistButtonN, TodolistButtonO, TodolistButtonP, TodolistButtonQ, TodolistButtonR, TodolistButtonS, TodolistButtonT, TodolistButtonU, TodolistButtonV, TodolistButtonW, TodolistButtonX, TodolistButtonY, TodolistButtonZ 
from modules.todolist.CsvHandlerTodolist import CsvHandlerTodolist
from modules.todolist.TodolistEnums import PriorityType
from modules.utils.embed_ascii_viewer import view_ascii_embed
from modules.utils.path import generate_path


class TodolistInterface(discord.ui.View):
    def __init__(self, message: discord.Message, message_embed: dict, csv_keys: list, embed_uuid):
        super().__init__()
        self.csv_keys = csv_keys
        self.message_embed = message_embed
        self.embed_uuid = embed_uuid
        self.message = message

        self.timeout = None
        self.data_dict = CsvHandlerTodolist(self.csv_keys).csv_get_all_data(generate_path(message.guild.id, f'todolists/{embed_uuid}.csv'))
        self.data_list = []
        for key in self.data_dict.keys():
            for elem in self.data_dict[key]:
                self.data_list.append([elem, key])
        self.buttons_list = [
            TodolistButtonA(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonB(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonC(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonD(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonE(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonF(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonG(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonH(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonI(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonJ(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonK(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonL(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonM(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonN(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonO(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonP(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonQ(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonR(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonS(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonT(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonU(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonV(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonW(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonX(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonY(self, self.embed_uuid, self.message_embed, self.data_list),
            TodolistButtonZ(self, self.embed_uuid, self.message_embed, self.data_list)
        ]
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


class TodolistButtonA(discord.ui.Button):
    def __init__(self, todolist_interface: TodolistInterface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇦'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(0)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonB(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇧'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(1)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonC(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇨'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(2)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonD(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇩'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(3)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonE(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇪'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(4)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonF(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇫'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(5)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonG(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇬'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(6)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonH(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇭'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(7)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonI(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇮'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(8)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonJ(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇯'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(9)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonK(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇰'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(10)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonL(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇱'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(11)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonM(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇲'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(12)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonN(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇳'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(13)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonO(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇴'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(14)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonP(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇵'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(15)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonQ(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇶'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(16)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonR(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇷'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(17)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonS(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇸'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(18)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonT(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇹'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(19)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonU(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇺'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(20)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonV(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇻'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(21)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonW(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇼'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(22)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonX(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇽'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(23)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonY(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇾'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(24)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()

class TodolistButtonZ(discord.ui.Button):
    def __init__(self, todolist_interface, embed_uuid: str, message_embed: dict, data_list: list):
        super().__init__()
        self.todolist_interface = todolist_interface
        self.emoji = '🇿'
        self.style = discord.ButtonStyle.blurple
        self.embed_uuid = embed_uuid
        self.original_embed = message_embed
        self.data_list = data_list

    async def callback(self, interaction: discord.Interaction):
        self.data_list.pop(25)
        data_dict = listToPriorityDict(self.data_list)
        CsvHandlerTodolist(['content', 'priority']).csv_rewrite_file(generate_path(interaction.guild.id, f'todolists/{self.embed_uuid}.csv'), self.data_list)
        self.todolist_interface.resetInterface()
        await interaction.message.edit(view=self.todolist_interface, embed=generateInterfaceEmbed(self.original_embed, data_dict))
        await interaction.response.defer()
