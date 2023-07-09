# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 14:35:00 2019
This is the code for the open-source stochastic model for the generation of
multi-energy load profiles in off-grid areas, called RAMP, v0.3.0.

@authors:
- Francesco Lombardi, Politecnico di Milano
- Sergio Balderrama, Université de Liège
- Sylvain Quoilin, KU Leuven
- Emanuela Colombo, Politecnico di Milano

Copyright 2019 RAMP, contributors listed above.
Licensed under the European Union Public Licence (EUPL), Version 1.2;
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations
under the License.
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


def load_profile():

    input_files_to_run = [1,2,3,4]


    #define how many days a load profile for each input file will have

    num_models_list_dict = {}
    num_models_list_dict["1"] = 90
    num_models_list_dict["2"] = 91
    num_models_list_dict["3"] = 92
    num_models_list_dict["4"] = 92
    

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
        
        print("Please Wait")

    #save the aggregated load profile in a csv-file results/output_file_aggregated.csv
    pp.export_series_year(tot_year)

    print('plots completed, the results are saved in results/output_file_yearly.csv')
    print('It has simulated the load profile of',len(tot_year),'minutes')


    pp.Profile_series_plot(tot_year)




