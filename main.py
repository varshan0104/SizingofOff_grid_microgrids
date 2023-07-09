"""

Part of masterthesis; Optimal sizing of offgrid microgrids.
@author: Varshan Erik Shankar

GridVille NTNU

"""

#All relevant packages
from Load_Profile.ramp.load_profile_run import load_profile
from Production_Profile.PV_production_data import PV_production_data


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
    


#Make sure the "Appliances_and_users" excel file is filled out. 
#File location: C:\Users\...\SizingofOff_grid_microgrids\Load_Profile\ramp\input_files
#load_profile()


#Make sure the Excel files are. 
PV_production_data()

'''
file_path = 'Production_Profile/Run_simulation.py'
with open(file_path, 'r') as file:
    code = file.read()
exec(code)



from analysis import *

# read in the input data
technical_data, pv_data = read_pv_data('productdata.xlsx')
bat_data = read_battery_data('productdata.xlsx')
location = read_location_data('Locationandload_data.xlsx')

# run the analysis code
#run_analysis(technical_data, pv_data, bat_data, location)

'''