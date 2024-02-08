import csv
import os
from modules.CsvHandler import CsvHandler


class CsvHandlerStockpiles(CsvHandler):
    def __init__(self, csv_file_keys: list):
        super().__init__(csv_file_keys)

    def csv_append_data(self, file_path: str, data_to_be_appended: dict):
        if os.stat(file_path).st_size == 0:
            with open(file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow(self.csv_file_keys)
        with open(file_path, 'a', newline='') as csv_file:
            row = []
            for key in self.csv_file_keys:
                row.append(data_to_be_appended[key])
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(row)

    def csv_get_all_data(self, file_path: str) -> [dict]:
        dict_list = []
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            next(reader, None)  # Used to skip header row

            for row in reader:
                dict_list.append(
                    {
                        self.csv_file_keys[0]: row[0],
                        self.csv_file_keys[1]: row[1],
                        self.csv_file_keys[2]: row[2],
                        self.csv_file_keys[3]: row[3],
                        self.csv_file_keys[4]: row[4]
                    }
                )
        return dict_list
