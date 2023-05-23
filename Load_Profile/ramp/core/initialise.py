# -*- coding: utf-8 -*-

#%% Initialisation of a model instance

import numpy as np 
import importlib
import pandas as pd

def yearly_pattern():
    '''
    Definition of a yearly pattern of weekends and weekdays, in case some appliances have specific wd/we behaviour
    '''
    #Yearly behaviour pattern
    Year_behaviour = np.zeros(365)
    Year_behaviour[5:365:7] = 1
    Year_behaviour[6:365:7] = 1
    
    return(Year_behaviour)

# def user_defined_inputs(j):
#     file_module = importlib.import_module(f'ramp.input_files.input_file_{j}')
#     User_list = file_module.User_list
#     return(User_list)

class User:
    def __init__(self, name, n_users, us_pref):
        self.name = name
        self.n_users = n_users
        self.us_pref = us_pref
        self.App_list = []

class Appliance:
    def __init__(self, user, number, P, num_windows, func_time, r_t, func_cycle, fixed, fixed_cycle, occasional_use, flat, thermal_P_var, pref_index, wd_we_type, year_min, initial_share):
        self.user = user
        self.number = number
        self.P = P
        self.num_windows = num_windows
        self.func_time = func_time
        self.r_t = r_t
        self.func_cycle = func_cycle
        self.fixed = fixed
        self.fixed_cycle = fixed_cycle
        self.occasional_use = occasional_use
        self.flat = flat
        self.thermal_P_var = thermal_P_var
        self.pref_index = pref_index
        self.wd_we_type = wd_we_type
        self.year_min = year_min
        self.initial_share = initial_share

    def windows(self, time_window_params, r_w):
        # Define this method based on your requirements
        pass



def user_defined_inputs(j):
    # Read the Excel file
    df = pd.read_excel('Load_Profile/ramp/core/Appliances_and_users.xlsx', sheet_name=1)  # Leser første ark (indeks 0)

    # Initialize an empty list to hold all users
    all_users = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Check if the User column is not NaN (i.e., there is a user for this row)
        if pd.notna(row['User']):
            # Create a new user
            user = User(row['User'], row['n_user'], row['us-pref'])
            all_users.append(user)

        # Create a new appliance
        appliance = Appliance(user, row['number'], row['P'], row['num-windows'], row['func-time'], row['r_t'], row['func_cycle'], row['fixed'], row['fixed_cycle'], row['occasional_use'], row['flat'], row['thermal_P_var'], row['pref_index'], row['wd_we_type'], row['year_min'], row['initial_share'])

        # Add the appliance to the current user and any other users specified in the 'Connected user' column
        connected_users = row['Connected user'].split(',')
        for user_name in connected_users:
            # Find the user with this name
            for user in all_users:
                if user.name == user_name:
                    # Add the appliance to this user
                    user.App_list.append(appliance)

        # Parse the time_window string to get the parameters for the .windows() function
        time_window_str = row['time_window']
        time_window_params = time_window_str.strip('[]').split(',')
        time_window_params = [int(param.strip()) for param in time_window_params]
        r_w = float(time_window_str.split('=')[1])

        # Call the .windows() function on the appliance
        appliance.windows(time_window_params, r_w=r_w)

    return all_users


def Initialise_model(num_profiles):

    """---------master thesis changes: input (num_profiles) is only given  in ramp_run_adjusted.py----------"""
    '''
    The model is ready to be initialised
    '''
   # num_profiles = int(input(
   #     "please indicate the number of profiles to be generated: "))  # asks the user how many profiles (i.e. code runs) he wants
    print('Please wait...')
    Profile = []  # creates an empty list to store the results of each code run, i.e. each stochastically generated profile

    return (Profile, num_profiles)


"""
def Initialise_model():
    '''
    The model is ready to be initialised
    '''
    num_profiles = int(input("please indicate the number of profiles to be generated: ")) #asks the user how many profiles (i.e. code runs) he wants
    print('Please wait...') 
    Profile = [] #creates an empty list to store the results of each code run, i.e. each stochastically generated profile
    
    return (Profile, num_profiles)"""
    
def Initialise_inputs(j):
    Year_behaviour = yearly_pattern()
    user_defined_inputs(j)
    user_list = user_defined_inputs(j)
    
    # Calibration parameters
    '''
    Calibration parameters. These can be changed in case the user has some real data against which the model can be calibrated
    They regulate the probabilities defining the largeness of the peak window and the probability of coincident switch-on within the peak window
    '''
    peak_enlarg = 0.15 #percentage random enlargement or reduction of peak time range length
    mu_peak = 0.5 #median value of gaussian distribution [0,1] by which the number of coincident switch_ons is randomly selected
    s_peak = 0.5 #standard deviation (as percentage of the median value) of the gaussian distribution [0,1] above mentioned
    op_factor = 0.5 #off-peak coincidence calculation parameter

    return (peak_enlarg, mu_peak, s_peak, op_factor, Year_behaviour, user_list)

