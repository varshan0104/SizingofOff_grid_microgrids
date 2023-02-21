import pandas as pd

def read_pv_data(file_path):
    # Read the Excel file
    data_pv = pd.read_excel(file_path, sheet_name='PV')

    # Extract the PV panel data
    pv1 = list(data_pv['PV1'])
    pv2 = list(data_pv['PV2'])
    pv3 = list(data_pv['PV3'])

    return [pv1, pv2, pv3]

def read_battery_data(file_path):
    data_battery = pd.read_excel(file_path, sheet_name='Battery')
    # Extract the battery data
    bat1 = list(data_battery['Battery1'])
    bat2 = list(data_battery['Battery2'])
    bat3 = list(data_battery['Battery3'])

    # Return the PV panel and battery data as lists
    return [bat1, bat2, bat3]

