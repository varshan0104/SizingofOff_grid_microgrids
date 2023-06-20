# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 18:51:56 2023

@author: Varshan
"""

import pvlib
#from pvlib.location import Location
from pvlib.iotools import get_pvgis_tmy
import pandas as pd
import matplotlib.pyplot as plt

'''Location data for Eco Moyo '''
latitude = -3.508264023015413
longitude = 39.84054566015608
tz = 'Africa/Nairobi'
altitude = 58 
name = 'Eco Moyo Education Centre'
#location = Location(latitude, longitude, tz, altitude)

''' Data for PV-panel (GCL-M8/72H) from data sheet '''
p_max = 1000                        #[W]
v_oc = 49.84                       #[V]
i_sc = 11.34                       #[A]
alpha_sc = 0.0006 * i_sc
beta_voc = -0.003 * v_oc
gamma_pmp = -0.0039
temp_ref = 25
surface_tilt = 6.2                 #Fieldwork Kari og Anja
surface_azimuth = -50              #Fieldwork Kari og Anja


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



''' Modify the data to fit the timezone of Eco Moyo'''

result_dc.index = result_dc.index + pd.DateOffset(hours = 3)
result_dc.drop(result_dc.tail(3).index,inplace=True)
addResult = pd.Series([0,0,0])
addResult.index = pd.date_range('2023-01-01 00:00:00', '2023-01-01 02:00:00', freq = 'h')
result_dc = pd.concat([addResult, result_dc])


result_dc.to_csv('pvlib_result.csv')
result_dc.plot(figsize = (16,9))
#plt.title('DC Power output per module')
plt.ylabel('DC output [W]')
plt.savefig("DCOutput.pdf", format="pdf", bbox_inches="tight")
plt.show()
