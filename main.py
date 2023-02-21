"""
Part of masterthesis; Optimal sizing of offgrid microgrids.
@author: Varshan Erik Shankar

GridVille NTNU
"""

#All relevant packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#imports all functions from importproductdata.py
from importproductdata import *

PVData = read_pv_data('productdata.xlsx')
BatteryData = read_battery_data('productdata.xlsx')

print("Dette er PV:")
print(PVData)

print("Dette er batteri :")
print(BatteryData)

from analysis import *

