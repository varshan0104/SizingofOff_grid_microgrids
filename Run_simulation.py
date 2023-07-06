#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 17:01:22 2022

@author: Varshan Erik Shankar
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os
import prosumpy as pros


#demand = pd.read_csv('output_file_aggregated.csv', index_col=0, header=None, parse_dates=True, squeeze=True)


demand = pd.read_csv('output_file_aggregated.csv',index_col=0, header=None, parse_dates=True, squeeze=True, nrows=525541)

#pv_1kW = pd.read_csv('tests\data\pv_example.csv', index_col=0, header=None, parse_dates=True, squeeze=True)

#Converts index to every minute for a year
demand.index = pd.date_range(start='2023-01-01 00:00', end='2023-12-31 23:00', freq='min')


#Changing index from every minute to every 15 minute with interpolation
demand = demand.resample('15min').interpolate(method='linear')

#Converting from [Wh] to [kWh]
demand = demand.loc[:].div(1000)

#Year 2019 
pv_1kW = pd.read_csv('pvlib_result.csv',
                     index_col=0, header=None, parse_dates=True, skiprows=1).squeeze("columns")

#Converts index from hourly to every 15 minutes with interpolation
pv_1kW = pv_1kW.resample('15min').interpolate(method='linear')


#Normalizing to 1 kW
pv_1kW = pv_1kW.loc[:].div(1000)




pv_size = (7 * 450)/1000                                   #kW
#pv_size = 7
param_tech = {'BatteryCapacity': 4*200*12/1000,            #kWh
              'BatteryEfficiency': .9,
              'InverterEfficiency': .93,
              'timestep': .25,
              'MaxPower': 3500/1000                        #kWh (maximum output of the inverter)
             }



pv = pv_1kW * pv_size

E1 = pros.dispatch_max_sc(pv, demand, param_tech, return_series=False)

E1.keys()

pros.print_analysis(pv, demand, param_tech, E1)

pros.plot_dispatch(pv, demand, E1, week=13)