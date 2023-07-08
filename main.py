"""

Part of masterthesis; Optimal sizing of offgrid microgrids.
@author: Varshan Erik Shankar

GridVille NTNU

"""

#All relevant packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Load_Profile.ramp.load_profile_run import load_profile

"""
Shows the directory this code is runned from, to make sure you are using the right one. 
It should be ...SizingOff_grid_microgrids
Also a check to make sure threading is correct 
"""

import os

if not os.path.exists('results'):
    os.makedirs('results')

#Check for trading
import threading
if threading.current_thread() is threading.main_thread():
    print("This is the main thread.")
else:
    print("This is not the main thread.")
    

#Function for calculating load profile, everything else happens in the folder: Load Profile
#Make sure the Appliances_and_users excel file is filled out. 
#File location: C:\Users\...\SizingofOff_grid_microgrids\Load_Profile\ramp\input_files

load_profile()



'''
from analysis import *

# read in the input data
technical_data, pv_data = read_pv_data('productdata.xlsx')
bat_data = read_battery_data('productdata.xlsx')
location = read_location_data('Locationandload_data.xlsx')

# run the analysis code
#run_analysis(technical_data, pv_data, bat_data, location)

'''