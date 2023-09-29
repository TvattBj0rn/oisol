import csv
from modules.todolist.TodolistEnums import PriorityType
from modules.utils.CsvHandler import CsvHandler


class CsvHandlerTodolist(CsvHandler):
    def __init__(self, csv_file_keys: list):
        super().__init__(csv_file_keys)


    def csv_append_data(self, file_path: str, data_to_be_appended: dict):
        with open(file_path, 'a') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow([data_to_be_appended[self.csv_file_keys[0]], data_to_be_appended[self.csv_file_keys[1]]])


    def csv_get_all_data(self, file_path: str) -> dict:
        data_dict = {
            PriorityType.HAUTE.value : [],
            PriorityType.MOYENNE.value: [],
            PriorityType.BASSE.value: [],
        }

        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            next(reader, None) # Skip header
            for row in reader:
                data_dict[row[1]].append(row[0])
        return data_dict


    def csv_rewrite_file(self, file_path: str, data: list):
        with open(file_path, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(self.csv_file_keys)
            for task in data:
                writer.writerow(task)
