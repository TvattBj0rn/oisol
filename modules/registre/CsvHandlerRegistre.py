import csv
import os
from modules.utils.CsvHandler import CsvHandler


class CsvHandlerRegister(CsvHandler):
    def __init__(self, csv_file_keys: list):
        super().__init__(csv_file_keys)

    def csv_append_data(self, file_path: str, data_to_be_appended: dict):
        if os.stat(file_path).st_size == 0:
            with open(file_path, 'w') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow(self.csv_file_keys)
        with open(file_path, 'a') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow([data_to_be_appended['member'], data_to_be_appended['timer']])

    def csv_get_all_data(self, file_path: str) -> [dict]:
        dict_list = []
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            next(reader, None)  # Used to skip header row
            for row in reader:
                dict_list.append(
                    {
                        'member': row[0],
                        'timer': row[1],
                    }
                )

        return dict_list