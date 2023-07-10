# -*- coding: utf-8 -*-
"""
Part of masterthesis; Off-Grid Microgrid Design Consideration for Rural Electrification.
Please read the README file before running the code. Make sure to download all the necessary packages.

Author: Varshan Erik Shankar
GridVille NTNU
"""

import pvlib
from pvlib.iotools import get_pvgis_tmy
import pandas as pd
import matplotlib.pyplot as plt
import pytz
from pvlib.location import Location

def read_pv_data(file_path):
    df = pd.read_excel(file_path, sheet_name='PV')
    p_max = df.loc[0,'P_max']                    #[W]
    v_oc = df.loc[0,'v_oc']                       #[V]
    i_sc = df.loc[0,'i_sc']                       #[A]
    alpha_sc = df.loc[0,'alpha_sc']
    beta_voc = df.loc[0,'beta_voc']
    gamma_pmp = df.loc[0,'gamma_pmp']
    temp_ref = df.loc[0,'temp_ref']
    surface_tilt = df.loc[0,'surface_tilt']                
    surface_azimuth = df.loc[0,'surface_azimuth']
    
    data_dict=[p_max,v_oc,i_sc,alpha_sc,beta_voc,gamma_pmp,temp_ref,surface_tilt,surface_azimuth]
    
    return data_dict


def read_location_data(file_path):
    df = pd.read_excel(file_path, sheet_name='Location')

    # extract individual values from DataFrame and assign to variables

    latitude = df.loc[0, 'latitude']
    longitude = df.loc[0, 'longtitude']
    tz_name = df.loc[0, 'timezone'].strip()  # remove leading/trailing whitespace
    altitude = df.loc[0, 'altitude']

    # convert time zone name to pytz time zone object
    tz = pytz.timezone(tz_name)

    location = Location(latitude, longitude, tz, altitude)

    return location

def PV_production_data(): 
    PVData = read_pv_data('productdata.xlsx')
    LocationData = read_location_data('Location_data.xlsx')
    
    latitude = LocationData.latitude
    longitude = LocationData.longitude
    tz = LocationData.tz
    altitude = LocationData.altitude 
    name = 'GridVille Customer'
    #location = Location(latitude, longitude, tz, altitude)
    
    p_max = PVData[0]                    #[W]
    v_oc = PVData[1]                       #[V]
    i_sc = PVData[2]                       #[A]
    alpha_sc = PVData[3]
    beta_voc = PVData[4]
    gamma_pmp = PVData[5]
    temp_ref = PVData[6]
    surface_tilt = PVData[7]                
    surface_azimuth = PVData[8]             
    
    
    start = '2023-01-01 00:00:00'
    end =   '2023-12-31 23:00:00'
    
    file = get_pvgis_tmy(latitude, longitude, outputformat='json', usehorizon=True, userhorizon=None, startyear=None, endyear=None, url='https://re.jrc.ec.europa.eu/api/', map_variables=None, timeout=30)
    
    
    poa_data = pd.DataFrame(columns = ['poa_global', 'poa_direct', 'poa_diffuse', 'temp_air', 'wind_speed'], index = file[0].index)
    
    #Processing data to the pvlib format
    #poa_data['poa_global'] = global_2020['G(i)']
    poa_data['poa_global'] = file[0]['G(h)']
    poa_data['poa_direct'] = file[0]['Gb(n)']
    #poa_data['poa_diffuse'] = components['Gd(i)'] + components['Gr(i)'] #sum of diffuse irradiance from the sky and from the ground
    poa_data['poa_diffuse'] = file[0]['Gd(h)']
    poa_data['temp_air'] = file[0]['T2m']
    poa_data['wind_speed'] = file[0]['WS10m']
    
    poa_data.index = pd.date_range(start, periods = len(poa_data.index), freq = 'h')
    poa_data.index = pd.to_datetime(poa_data.index, format = '%Y%m%d:%H%M')
    
    
    temp_cell = pvlib.temperature.faiman(poa_data['poa_global'], poa_data['temp_air'], poa_data['wind_speed']) #Calculating the module temperature using the Faiman model
    result_dc = pvlib.pvsystem.pvwatts_dc(poa_data['poa_global'] , temp_cell, p_max, gamma_pmp, temp_ref)
    
    
    result_dc.index = result_dc.index + pd.DateOffset(hours = 3)
    result_dc.drop(result_dc.tail(3).index,inplace=True)
    addResult = pd.Series([0,0,0])
    addResult.index = pd.date_range('2023-01-01 00:00:00', '2023-01-01 02:00:00', freq = 'h')
    result_dc = pd.concat([addResult, result_dc])
    
    
    result_dc.to_csv('pvlib_result.csv')
    result_dc.plot(figsize = (16,9))
    #plt.title('DC Power output per module')
    plt.ylabel('DC output [W]')
    plt.savefig("results\DCOutput.pdf", format="pdf", bbox_inches="tight")
    plt.show()
    
PV_production_data()
