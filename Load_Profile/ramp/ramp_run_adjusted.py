def load_profile():

    # -*- coding: utf-8 -*-
    """
    This is the code for the open-source stochastic model for the generation of
    multi-energy load profiles in off-grid areas, called RAMP, v0.3.0.

    This code is inspired by the creators of RAMP:
    - Francesco Lombardi, Politecnico di Milano
    - Sergio Balderrama, Université de Liège
    - Sylvain Quoilin, KU Leuven
    - Emanuela Colombo, Politecnico di Milano
    """

    #%% Import required modules

    import sys,os
    sys.path.append(r'C:\Users\varsh\PycharmProjects\SizingOffGridMicrogrids\Load_Profile')


    from ramp.core.stochastic_process import Stochastic_Process
    from ramp.post_process import post_process as pp
    import numpy as np
    import pandas as pd

    # Define which input files should be considered and run.
    # Files are specified as numbers in a list (e.g. [1,2] will consider input_file_1.py and input_file_2.py)

    """-----Comment related to master thesis:---------"""
    """
    This file is an adjusted version of ramp_run.py. It aggregates all daily loadprofiles into one loadprofile with the 
    total amount of days that are constructed for the given input files. 
    
    To construct a whole year with its defined variations, 11 input files have been established.
    Each input denotes a season, and can be found in the folder: RAMP-master-->ramp-->input_files
    The object for all buildings at the property are included in these input files to capture the power consumption of the 
    whole school. These can be commented in/out of the code, depending on which combination of buildings is desired.
    
    The objects related to each building/area can be found in RAMP_code/Objects related to buildings
    
    The resulting minute-based load profiles are saved under results. The aggregated load profile is saved in
    results/output_file_aggregated.csv 
    
    The list called input_files_to_run is used to defined which input files that load profiles will be created for,
    which will be summarised to one complete load profile. 
    
    The following values input_files_to_run will establish a complete load profile for input file 1 to 11. 
    The aggregated load profile will summarize the days in the same order as defined in this list (i.e. pay attention
    to the order that the input files are defined in).
    """
    input_files_to_run = [1,2,3,4]

    """To illustrate, the following input_files_to_run would establish load profiles for inputfile 1,6 and 4, 
    in that order. The result would be a single load profiles consisting of all minute-based daily load profiles
    established for input file 1, followed by all minute-based daily load profiles established for input file 6, 
    and lastly the same for input file 4:
    
    input_files_to_run = [1,6,4]
    
    The following gives a summary of what the input_files represent. This is in line with the seasons that have 
    been defined in the master thesis. 
    
    num_models_dict is a dictionary that has been established so that the number of daily load profiles that are to 
    be constructed for each input file can be defined.
    """

    #define how many days a load profile for each input file will have

    num_models_list_dict = {}
    num_models_list_dict["1"] = 91
    num_models_list_dict["2"] = 91
    num_models_list_dict["3"] = 92
    num_models_list_dict["4"] = 91




    tot_number_of_days = 0

    for j in input_files_to_run:
        tot_number_of_days = tot_number_of_days + num_models_list_dict[str(j)]

    print('You are currently producing a total number of', tot_number_of_days, 'days')
    print('This corresponds to a load profile of', tot_number_of_days*60*24, 'minutes')


    #from master research: tot_year is the final load profile that will be that will be plotted and saved
    tot_year = np.array([])

    # Calls the stochastic process and saves the result in a list of stochastic profiles called Profiles_list
    for j in input_files_to_run:
        #from master research: give the number of models/days for each input file to the stochastic process
        num_models = num_models_list_dict[str(j)]
        Profiles_list = Stochastic_Process(j,num_models)

        #from master research: add the established load profile to the array with the yearly profile
        for iii in Profiles_list:
            tot_year = np.append(tot_year, iii)

    # Post-processes the results and generates plots
        Profiles_avg, Profiles_list_kW, Profiles_series = pp.Profile_formatting(Profiles_list)

        #save data for each input file in csv-files in the results-folder
        pp.export_series(Profiles_series,j)

    #save the aggregated load profile in a csv-file results/output_file_aggregated.csv
    pp.export_series_year(tot_year)

    print('plots completed, the results are saved in results/output_file_yearly.csv')
    print('It has simulated the load profile of',len(tot_year),'minutes')


    pp.Profile_series_plot(tot_year)




