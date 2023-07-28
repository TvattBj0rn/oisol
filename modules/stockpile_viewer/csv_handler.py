import csv
import os


def csv_try_create_file(file_path: str, keys: list):
    splited_path = os.path.split(file_path)
    os.makedirs(splited_path[0], exist_ok=True)
    try:
        with open(file_path, 'x') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(keys)
    except FileExistsError:
        pass


def csv_clear_data(file_path: str, new_keys: list):
    with open(file_path, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(new_keys)


def csv_delete_data(file_path: str, key_to_del):
    row_list = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        next(reader, None)
        for row in reader:
            if not row[2] == key_to_del:
                row_list.append(row)
    with open(file_path, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        default_keys = ['region', 'subregion', 'code', 'name', 'type']
        for key in row_list:
            writer.writerow(key)
        for row in row_list:
            writer.writerow(row)

def csv_append_data(file_path: str, data_to_be_appended: dict):
    with open(file_path, 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow([data_to_be_appended['region'], data_to_be_appended['subregion'], data_to_be_appended['code'], data_to_be_appended['name'], data_to_be_appended['type']])


def csv_get_all_data(file_path: str) -> [dict]:
    dict_list = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        next(reader, None) ## Skip header row
        for row in reader:
            dict_list.append(
                {
                    'region': row[0],
                    'subregion': row[1],
                    'code': row[2],
                    'name': row[3],
                    'type': row[4]
                }
            )

    return dict_list
