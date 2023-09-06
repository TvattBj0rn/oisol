import csv
import os

CSV_FILE_KEYS = ['member', 'timer']

def csv_try_create_file(file_path: str):
    splited_path = os.path.split(file_path)
    os.makedirs(splited_path[0], exist_ok=True)
    try:
        with open(file_path, 'x') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(CSV_FILE_KEYS)
    except FileExistsError:
        pass


def csv_clear_data(file_path: str):
    with open(file_path, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(CSV_FILE_KEYS)


def csv_delete_data(file_path: str, key_to_del):
    new_row_list = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        next(reader, None)
        for row in reader:
            if not row[2] == key_to_del:
                new_row_list.append(row)
    with open(file_path, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(CSV_FILE_KEYS)
        for row in new_row_list:
            writer.writerow(row)

def csv_append_data(file_path: str, data_to_be_appended: dict):
    if os.stat(file_path).st_size == 0:
        with open(file_path, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(CSV_FILE_KEYS)
    with open(file_path, 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow([data_to_be_appended['member'], data_to_be_appended['timer']])


def csv_get_all_data(file_path: str) -> [dict]:
    dict_list = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        next(reader, None) # Used to skip header row
        for row in reader:
            dict_list.append(
                {
                    'member': row[0],
                    'timer': row[1],
                }
            )

    return dict_list
