import gspread


STOCKPILE_SHEET = gspread.service_account(filename='modules/stockpile_viewer/gspread/service_account.json').open('stockpiles_slr')


def create_stockpile(location: list, code: int, name: str, stockpile_type: str):
    worksheet = STOCKPILE_SHEET.duplicate_sheet(source_sheet_id=392006361, new_sheet_name=name)
    worksheet.update('C2', name)
    worksheet.update('C3', f'{location[0]} - {location[1]}')
    worksheet.update('C4', code)
    worksheet.update('C5', stockpile_type)

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
        if worksheet.acell('C2').value == 'template':
            continue
        stockpiles_list[worksheet.acell('C2').value] = dict()
        stockpiles_list[worksheet.acell('C2').value]['localisation'] = worksheet.acell('C3').value
        stockpiles_list[worksheet.acell('C2').value]['code'] = worksheet.acell('C4').value
        stockpiles_list[worksheet.acell('C2').value]['type'] = worksheet.acell('C5').value

    return stockpiles_list