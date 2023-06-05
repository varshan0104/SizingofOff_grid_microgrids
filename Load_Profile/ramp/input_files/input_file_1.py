# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition
'''

import pandas as pd
import numpy as np
from Load_Profile.ramp.core.core import User

User_list = []

# Read the Excel file
df = pd.read_excel('Load_Profile/ramp/input_files/Appliances_and_users.xlsx', sheet_name='Appliances')

# Group the data by user
grouped = df.groupby('user')

# Iterate over the groups
for user_name, group in grouped:
    # Create User object
    user = User(user_name, group['n_users'].iloc[0], group['us_pref'].iloc[0])

    # Iterate over the rows of the group


    # Add User object to User_list
    User_list.append(user)

    print(User_list)

for index, row in group.iterrows():
        # Convert 'P' column to DataFrame
        P_df = pd.DataFrame([row['P']])

        # Create Appliance object and add to User's App_list
        appliance = user.Appliance(row['number'], P_df, row['num_windows'], row['func_time'], row['r_t'],
                                   row['func_cycle'], row['fixed'], row['fixed_cycle'], row['occasional_use'],
                                   row['flat'], row['thermal_P_var'], row['pref_index'], row['wd_we_type'],
                                   row['year_min'], row['initial_share'])
        user.App_list.append(appliance)
