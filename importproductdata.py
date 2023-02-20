import pandas as pd

def read_input_data(file_path):
    # Read the Excel file
    data = pd.read_excel(file_path, sheet_name='Input')

    # Extract the PV panel data
    pv1 = list(data['PV1'])
    pv2 = list(data['PV2'])
    pv3 = list(data['PV3'])

    # Extract the battery data
    bat1 = list(data['Battery1'])
    bat2 = list(data['Battery2'])
    bat3 = list(data['Battery3'])

    # Return the PV panel and battery data as lists
    return [pv1, pv2, pv3], [bat1, bat2, bat3]


