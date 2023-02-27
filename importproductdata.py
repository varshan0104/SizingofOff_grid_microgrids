import pandas as pd
import pytz
from pvlib.location import Location

'''
def read_pv_data(file_path):
    # Read the Excel file
    data_pv = pd.read_excel(file_path, sheet_name='PV')

    # Extract the PV panel data
    pv1 = list(data_pv['PV1'])
    pv2 = list(data_pv['PV2'])
    pv3 = list(data_pv['PV3'])

    return [pv1, pv2, pv3]
'''


def read_pv_data(file_path):
    # Read the Excel file and extract the PV panel data and technical parameters
    data_pv = pd.read_excel(file_path, sheet_name='PV')
    technical_data = data_pv.loc[:, 'Enhet'].to_dict()

    # Initialize a dictionary to store the data for each PV panel
    pv_data = {}

    # Loop through the columns of the data to extract the values for each PV panel
    for col in data_pv.columns[1:]:
        panel_data = data_pv.loc[:, col].to_list()
        pv_data[col] = panel_data

    return technical_data, pv_data

def read_battery_data(file_path):
    data_battery = pd.read_excel(file_path, sheet_name='Battery')
    # Extract the battery data
    bat1 = list(data_battery['Battery1'])
    bat2 = list(data_battery['Battery2'])
    bat3 = list(data_battery['Battery3'])

    # Return the PV panel and battery data as lists
    return [bat1, bat2, bat3]

def read_location_data(file_path):
    df = pd.read_excel(file_path, sheet_name='Location')

    # extract individual values from DataFrame and assign to variables

    latitude = df.loc[0, 'latitude']
    longitude = df.loc[0, 'longtitude']
    tz_name = df.loc[0, 'timezone'].strip()  # remove leading/trailing whitespace
    altitude = df.loc[0, 'altitude']

    # convert time zone name to pytz time zone object
    tz = pytz.timezone(tz_name)

    location = Location(latitude, longitude, tz, altitude)

    return location
