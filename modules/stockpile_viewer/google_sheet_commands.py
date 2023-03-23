import gspread
import uuid


STOCKPILE_SHEET = gspread.service_account(filename='modules/stockpile_viewer/gspread/service_account.json').open('stockpiles_slr')


def create_stockpile(location: list, code: str, name: str, stockpile_type: str):
    worksheet = STOCKPILE_SHEET.duplicate_sheet(source_sheet_id=392006361, new_sheet_name=str(uuid.uuid4()))
    cell_list = worksheet.range('C2:C5')
    cell_values = [name, f'{location[0]} - {location[1]}', code, stockpile_type]
    for i, val in enumerate(cell_values):
        cell_list[i].value = val
    worksheet.update_cells(cell_list=cell_list)

def get_stockpile_status(name: str) -> tuple:
    worksheet = STOCKPILE_SHEET.worksheet(name)
    all_values = worksheet.batch_get(['StockpileStatus', 'SmallArms', 'HeavyArms', 'HeavyAmmunition', 'Utility', 'Medical', 'Resource', 'Uniforms', 'VehiclesCrates', 'Vehicles', 'EmplacementsCrates', 'Emplacements'])
    stockpile_status = {item[0]: item[1] for item in worksheet.get('StockpileStatus')}
    del all_values[0]

    sorted_stockpile = dict()
    for category in all_values:
        sorted_stockpile[category[0][0]] = [{category[index][0]: category[index][1]} for index in range(1, len(category)) if category[index][1] != '0']

    return sorted_stockpile, stockpile_status



def get_all_stockpiles() -> dict:
    stockpiles_list = dict()
    worksheets_list = STOCKPILE_SHEET.worksheets()

    for worksheet in worksheets_list:
        raw_data = worksheet.get('StockpileStatus')
        worksheet_name = raw_data[0][1]
        if worksheet_name[:8] == 'template':
            continue
        stockpiles_list[worksheet.title] = dict()
        stockpiles_list[worksheet.title]['name'] = worksheet_name
        stockpiles_list[worksheet.title]['localisation'] = raw_data[1][1]
        stockpiles_list[worksheet.title]['code'] = raw_data[2][1]
        stockpiles_list[worksheet.title]['type'] = raw_data[3][1]
    return stockpiles_list