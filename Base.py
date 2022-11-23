class Base:
    def __init__(self, name):
        self.name = name  # base name
        self.__stockpile_maintenance = [0, 0]  # bsup | gsup
        self.__consumption_maintenance = [0, 0]  # bsup | gsup

    def get_maintenance_consumption(self):
        return self.__consumption_maintenance

    def set_maintenance_consumption(self, key: int, value: int):
        self.__consumption_maintenance[key] = value

    def get_maintenance_stockpile(self):
        return self.__stockpile_maintenance

    def set_maintenance_stockpile(self, key: int, value: int):
        self.__stockpile_maintenance[key] = value
