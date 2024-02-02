import os
import csv


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
