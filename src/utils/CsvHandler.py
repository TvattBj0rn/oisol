import os
import csv
from src.utils.oisol_enums import Modules, PriorityType


class CsvHandler:
    def __init__(self, csv_file_keys: list):
        self.csv_file_keys = csv_file_keys

    def csv_try_create_file(self, file_path: str):
        separated_path = os.path.split(file_path)
        os.makedirs(separated_path[0], exist_ok=True)
        try:
            with open(file_path, 'x', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow(self.csv_file_keys)
        except FileExistsError:
            pass

    def csv_clear_data(self, file_path: str):
        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(self.csv_file_keys)

    def csv_delete_data(self, file_path: str, key_to_del):
        new_row_list = []
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            next(reader, None)
            for row in reader:
                if not row[2] == key_to_del:
                    new_row_list.append(row)
        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(self.csv_file_keys)
            for row in new_row_list:
                writer.writerow(row)

    def csv_get_all_data(self, file_path: str, module: Modules) -> [dict]:
        data = {
            PriorityType.HAUTE.value: [],
            PriorityType.MOYENNE.value: [],
            PriorityType.BASSE.value: [],
        } if module == module.TODOLIST else []

        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            next(reader, None)  # Used to skip header row
            for row in reader:
                if module == Modules.TODOLIST:
                    data[row[1]].append(row[0])
                else:
                    data.append(
                        {self.csv_file_keys[i]: row[i] for i in range(len(self.csv_file_keys))}
                    )
        return data

    def csv_rewrite_file(self, file_path: str, data: list, module: Modules):
        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(self.csv_file_keys)
            for row in data:
                writer.writerow([row[self.csv_file_keys[0]], row[self.csv_file_keys[1]]] if module == Modules.REGISTER else row)

    def csv_append_data(self, file_path: str, data_to_be_appended: dict, module: Modules):
        if os.stat(file_path).st_size == 0:
            with open(file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow(self.csv_file_keys)
        with open(file_path, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            if module in [Modules.REGISTER, Modules.TODOLIST]:
                writer.writerow([data_to_be_appended[self.csv_file_keys[0]], data_to_be_appended[self.csv_file_keys[1]]])
            elif module == Modules.STOCKPILE:
                writer.writerow([data_to_be_appended[k] for k in self.csv_file_keys])
