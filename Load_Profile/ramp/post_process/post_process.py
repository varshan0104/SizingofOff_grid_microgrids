# -*- coding: utf-8 -*-

#%% Import required libraries

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

#from Anja:

import csv

#%% Post-processing
'''
Just some additional code lines to calculate useful indicators and generate plots
'''
def Profile_formatting(stoch_profiles):
    Profile_avg = np.zeros(1440)
    for pr in stoch_profiles:
        Profile_avg = Profile_avg + pr
    Profile_avg = Profile_avg/len(stoch_profiles)
    
    Profile_kW = []
    for kW in stoch_profiles:
        Profile_kW.append(kW/1000)
    
    Profile_series = np.array([])
    for iii in stoch_profiles:
        Profile_series = np.append(Profile_series,iii)
    
    return (Profile_avg, Profile_kW, Profile_series)

def Profile_cloud_plot(stoch_profiles,stoch_profiles_avg):
    #x = np.arange(0,1440,5)
    plt.figure(figsize=(10,5))
    for n in stoch_profiles:
        plt.plot(np.arange(1440),n,'#b0c4de')
        plt.xlabel('Time (hours)')
        plt.ylabel('Power (W)')
        plt.ylim(ymin=0)
        #plt.ylim(ymax=5000)
        plt.margins(x=0)
        plt.margins(y=0)
    plt.plot(np.arange(1440),stoch_profiles_avg,'#4169e1')
    plt.xticks([0,240,480,(60*12),(60*16),(60*20),(60*24)],[0,4,8,12,16,20,24])
    #plt.savefig('profiles.eps', format='eps', dpi=1000)
    plt.show()


def Profile_series_plot(stoch_profiles_series):

    #Plots in NTNU color code (blue)
    plt.figure(figsize=(10, 5))
    plt.style.use('seaborn-whitegrid')
    plt.plot(np.arange(len(stoch_profiles_series)), stoch_profiles_series, '#00509e')

    plt.xlabel('Time [minutes]')
    plt.ylabel('Power consumption [W]')
    plt.ylim(ymin=0, ymax=10000)
    # plt.ylim(ymax=5000)
    plt.margins(x=0)
    plt.margins(y=0)

    plt.show()

# Export Profiles

def export_series(stoch_profiles_series, j):
    series_frame = pd.DataFrame(stoch_profiles_series)
    series_frame.to_csv('results/output_file_%d.csv' % (j))


"""-------From master thesis research: Save the complete (annual) load profile as csv file-------"""
def export_series_year(tot_year):
    series_frame = pd.DataFrame(tot_year)
    series_frame.to_csv('results/output_file_aggregated.csv')







