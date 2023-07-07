import pandas as pd
import numpy as np

# Load the demand data
demand = pd.read_csv('output_file_aggregated.csv', index_col=0, header=None, parse_dates=True, squeeze=True, nrows=525541)
demand.index = pd.date_range(start='2023-01-01 00:00', end='2023-12-31 23:00', freq='min')
demand = demand.resample('15min').interpolate(method='linear')
demand = demand.loc[:].div(1000)  # Convert from Wh to kWh

# Load the PV production data
pv_1kW = pd.read_csv('pvlib_result.csv', index_col=0, header=None, parse_dates=True, skiprows=1).squeeze("columns")
pv_1kW = pv_1kW.resample('15min').interpolate(method='linear')
pv_1kW = pv_1kW.loc[:].div(1000)  # Normalize to 1 kW

# Define the battery parameters
param_tech = {'BatteryCapacity': 4*200*12/1000,            #kWh
              'BatteryEfficiency': .9,
              'InverterEfficiency': .93,
              'timestep': .25,
              'MaxPower': 3500/1000                        #kWh (maximum output of the inverter)
             }

# Calculate the total energy demand for a year
total_demand = demand.sum()

# Calculate the total energy output from a PV panel for a year
total_pv_output = pv_1kW.sum()

# Calculate the number of PV panels needed
num_pv = int(np.ceil(total_demand / total_pv_output))

# Calculate the maximum energy demand for a day
max_daily_demand = demand.resample('D').sum().max()

# Calculate the energy capacity of a battery
battery_capacity = param_tech['BatteryCapacity'] * param_tech['BatteryEfficiency'] * 0.7

# Calculate the number of batteries needed
num_batteries = int(np.ceil(max_daily_demand / battery_capacity))

print(f'Number of PV panels needed: {num_pv}')
print(f'Number of batteries needed: {num_batteries}')


import matplotlib.pyplot as plt

# Calculate the total PV production for each time step
total_pv_production = num_pv * pv_1kW

# Initialize the state of charge of the batteries
soc = num_batteries * param_tech['BatteryCapacity']

# Initialize lists to store the battery charge and discharge for each time step
battery_charge = []
battery_discharge = []

# For each time step...
for t in range(len(demand)):
    # Calculate the net power (production minus demand)
    net_power = total_pv_production.iloc[t] - demand.iloc[t]

    # If there is a surplus of power...
    if net_power > 0:
        # Charge the batteries, but don't exceed their total capacity
        soc = min(soc + net_power * param_tech['BatteryEfficiency'], num_batteries * param_tech['BatteryCapacity'])
        battery_charge.append(net_power * param_tech['BatteryEfficiency'])
        battery_discharge.append(0)
    # If there is a deficit of power...
    else:
        # Discharge the batteries, but don't go below the minimum state of charge
        soc = max(soc + net_power / param_tech['BatteryEfficiency'], num_batteries * param_tech['BatteryCapacity'] * 0.3)
        battery_charge.append(0)
        battery_discharge.append(-net_power / param_tech['BatteryEfficiency'])

# Create a figure with two subplots
fig, ax = plt.subplots(2, 1, sharex=True)

# Plot the production, demand and battery coverage on the first subplot
ax[0].plot(total_pv_production.index, total_pv_production.values, label='Production')
ax[0].plot(demand.index, demand.values, label='Demand')
ax[0].legend()
ax[0].set_ylabel('Power (kW)')

# Plot the battery charge and discharge on the second subplot
ax[1].plot(total_pv_production.index, battery_charge, label='Battery charge')
ax[1].plot(total_pv_production.index, battery_discharge, label='Battery discharge')
ax[1].legend()
ax[1].set_ylabel('Power (kW)')
ax[1].set_xlabel('Time')

# Show the figure
plt.show()

