# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition
'''

import pandas as pd
from Load_Profile.ramp.core.core import User

from Load_Profile.ramp.core.core import User

# Create an instance of User
user_instance = User(name="user1", n_users=1, us_pref=0)

# Now you can access Appliance through the user_instance
appliance_instance = user_instance.Appliance(user="user1", n=1, P=0, w=1, t=0, r_t=0, c=1, fixed='no', fixed_cycle=0, occasional_use=1, flat='no', thermal_P_var=0, pref_index=0, wd_we_type=2, P_series=False)


def load_from_excel(file_path):
    df = pd.read_excel(file_path, sheet_name='Spring')
    users = []
    appliances = []
    for _, row in df.iterrows():
        user = User(row['User Name'], row['Number of Users'], row['User Preference'])
        users.append(user)
        appliance = user.Appliance(
            user,
            row['Number of Appliances'],
            row['Power of Appliance'],
            row['Number of Functioning Windows'],
            row['Function Time'],
            row['Random Variability Percentage'],
            row['Function Cycle'],
            row['Fixed'],
            row['Fixed Cycle'],
            row['Occasional Use'],
            row['Flat'],
            row['Thermal Power Variation'],
            row['Preference Index'],
            row['Weekday/Weekend Type'],
            row['Year Minimum'],
            row['Initial Share']
        )
        appliances.append(appliance)
    return users, appliances

users, appliances = load_from_excel('C:/Users/varsh/PycharmProjects/SizingOffGridMicrogrids/Load_Profile/ramp/input_files/Appliances_and_users.xlsx')

User_list = users
