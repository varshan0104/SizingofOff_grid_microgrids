# -*- coding: utf-8 -*-
"""
Part of masterthesis; Off-Grid Microgrid Design Consideration for Rural Electrification.
Please read the README file before running the code. Make sure to download all the necessary packages.
It would be beneficial to read the Microgrid Sizing guide provided in a PDF format in the same folder as this file.

Author: Varshan Erik Shankar
GridVille NTNU
"""

# All relevant packages
from Load_Profile.ramp.load_profile_run import load_profile
from Production_Profile.PV_production_data import PV_production_data

"""
The following code shows the directory from which this code is being executed, to ensure that you are in the correct directory,
which should be ...SizingOff_grid_microgrids.
Also, it includes a check to verify the threading is correct.
"""

import os

if not os.path.exists('results'):
    os.makedirs('results')

# Check for threading
import threading
if threading.current_thread() is threading.main_thread():
    print("This is the main thread.")
else:
    print("This is not the main thread.")

# Make sure the "Appliances_and_users" excel file is filled out.
# File location: C:\Users\...\SizingofOff_grid_microgrids\Load_Profile\ramp\input_files
load_profile()

# Function for Solar Production Profile
PV_production_data()

# Run simulation
file_path = 'Production_Profile/Run_simulation.py'
with open(file_path, 'r') as file:
    code = file.read()
exec(code)
