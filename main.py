"""
Part of masterthesis; Optimal sizing of offgrid microgrids.
@author: Varshan Erik Shankar

GridVille NTNU

multicommit suksessfull
"""

#All relevant packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#imports all functions from importproductdata.py
from importproductdata import *

PVData = read_pv_data('productdata.xlsx')
BatteryData = read_battery_data('productdata.xlsx')
LocationData = read_location_data('Locationandload_data.xlsx')

print("Dette er PV:")
print(PVData)

print(PVData[1]['PV2'][4])

print("Dette er batteri :")
print(BatteryData)

print("Dette er lokasjonsdata:")
print(LocationData)

from analysis import *

# read in the input data
technical_data, pv_data = read_pv_data(pv_file_path)
bat_data = read_battery_data(battery_file_path)
location = read_location_data(location_file_path)

# run the analysis code
run_analysis(technical_data, pv_data, bat_data, location)