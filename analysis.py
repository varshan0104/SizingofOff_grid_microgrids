import pandas as pd
import pvlib
from importproductdata import *
PVData = read_pv_data('productdata.xlsx')
LocationData = read_location_data('Locationandload_data.xlsx')
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


p_max = PVData[1]['PV1'][0]                        #[W]
v_oc = PVData[1]['PV1'][1]                       #[V]
i_sc = PVData[1]['PV1'][2]                       #[A]
alpha_sc = PVData[1]['PV1'][3]
beta_voc = PVData[1]['PV1'][4]
gamma_pmp = PVData[1]['PV1'][5]
temp_ref = PVData[1]['PV1'][6]
surface_tilt = PVData[1]['PV1'][7]
surface_azimuth = PVData[1]['PV1'][8]

# set start and end dates for the simulation
start = '2019-01-01 00:00:00'
end = '2019-12-31 23:00:00'

''' Hourly Radiation Data from PVGIS '''
#https://re.jrc.ec.europa.eu/pvg_tools/en/tools.html#PVP

# read in data from PVGIS global horizontal irradiance file
global_2020 = pd.read_csv('pvgis_global2020.csv', skiprows=8, nrows=8760, index_col=0)

# read in data from PVGIS direct and diffuse irradiance components file
components = pd.read_csv('pvgis_components2020.csv', skiprows=8, nrows=8760, index_col=0)

# create a blank dataframe to hold processed POA data
poa_data = pd.DataFrame(columns=['poa_global', 'poa_direct', 'poa_diffuse', 'temp_air', 'wind_speed'], index=global_2020.index)

# extract data from PVGIS dataframes and store it in the new dataframe
poa_data['poa_global'] = global_2020['G(i)']
poa_data['poa_direct'] = components['Gb(i)']
poa_data['poa_diffuse'] = components['Gd(i)'] + components['Gr(i)'] # sum of diffuse irradiance from the sky and from the ground
poa_data['temp_air'] = components['T2m']
poa_data['wind_speed'] = components['WS10m']

# set index to be hourly and convert to datetime format
poa_data.index = pd.date_range(start, periods=len(poa_data.index), freq='h')
poa_data.index = pd.to_datetime(poa_data.index, format='%Y%m%d:%H%M')

''' Calculating DC power output '''

# calculate module temperature using the Faiman model
temp_cell = pvlib.temperature.faiman(poa_data['poa_global'], poa_data['temp_air'], poa_data['wind_speed'])

# calculate DC power output using the PVWatts model
result_dc = pvlib.pvsystem.pvwatts_dc(poa_data['poa_global'], temp_cell, p_max, gamma_pmp, temp_ref)

''' Modify the data to fit the timezone of the location '''

# shift index to match local timezone
result_dc.index = result_dc.index + pd.DateOffset(hours=3) # Endre tallet her til timezoneoffset

# drop the last 3 rows to remove any partial hours
result_dc.drop(result_dc.tail(3).index, inplace=True)

# create a series of zeros to fill any missing hours at the beginning of the year
addResult = pd.Series([0, 0, 0])
addResult.index = pd.date_range('2019-01-01 00:00:00', '2019-01-01 02:00:00', freq='h')

# concatenate the zero series to the beginning of the result_dc dataframe
result_dc = pd.concat([addResult, result_dc])

# write results to a CSV file
result_dc.to_csv('pvlib_result.csv')

# plot the results
result_dc.plot(figsize=(16, 9))
plt.ylabel('DC output [W]')
plt.savefig("DCOutput.pdf", format="pdf", bbox_inches="tight")
plt.show()
