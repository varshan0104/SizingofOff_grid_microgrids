import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy.optimize as optimize

# Load the demand data
demand = pd.read_csv('Production_Profile\output_file_aggregated.csv', index_col=0, header=None, parse_dates=True, squeeze=True, nrows=525541)
demand.index = pd.date_range(start='2023-01-01 00:00', end='2023-12-31 23:00', freq='min')
demand = demand.resample('15min').interpolate(method='linear')
demand = demand.loc[:].div(1000)  # Convert from Wh to kWh

# Load the PV production data
pv_1kW = pd.read_csv('Production_Profile\pvlib_result.csv', index_col=0, header=None, parse_dates=True, skiprows=1).squeeze("columns")
pv_1kW = pv_1kW.resample('15min').interpolate(method='linear')
pv_1kW = pv_1kW.loc[:].div(1000)  # Normalize to 1 kW

# Define the battery parameters
param_tech = {'BatteryCapacity': 4*200*24/1000,            #kWh
              'BatteryEfficiency': .9,
              'InverterEfficiency': .93,
              'timestep': .25,
              'MaxPower': 3500/1000,                       #kWh (maximum output of the inverter)
              'BatteryDegradation': 0.02                   # Assume 2% capacity loss per year
             }

# Calculate the total energy demand for a year
total_demand = demand.sum()

# Calculate the total energy output from a PV panel for a year
total_pv_output = pv_1kW.sum()

# Calculate the number of PV panels needed
num_pv = int(np.ceil(total_demand / total_pv_output))

# Calculate the maximum energy demand for a day
max_daily_demand = demand.resample('D').sum().max()

# Calculate the energy capacity of a battery, considering degradation
battery_capacity = param_tech['BatteryCapacity'] * (1 - param_tech['BatteryDegradation']) * param_tech['BatteryEfficiency'] * 0.8

# Calculate the number of batteries needed
num_batteries = int(np.ceil(max_daily_demand / battery_capacity))

print(f'Number of PV panels needed: {num_pv}')
print(f'Number of batteries needed: {num_batteries}')

# Calculate the total PV production for each time step
total_pv_production = num_pv * pv_1kW

# Initialize the state of charge of the batteries
soc = num_batteries * param_tech['BatteryCapacity']

# Initialize lists to store the battery charge and discharge for each time step
battery_charge = []
battery_discharge = []

#Scen1

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

# Create a figure with two subplots, specify the figure size
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(10,8))

# Set an overall title for the figure, make it bold and larger
fig.suptitle('Basic coverage of demand', weight='bold', fontsize=14)

# Plot the production, demand and battery coverage on the first subplot with transparency
ax[0].plot(demand.index, demand.values, label='Demand', alpha=0.5)
ax[0].plot(total_pv_production.index, total_pv_production.values, label='Production', alpha=0.5)
ax[0].legend(loc='best') # 'best' for automatic placement that doesn't overlap the plot
ax[0].set_ylabel('Power (kW)')

# Plot the battery charge and discharge on the second subplot with specified colors
ax[1].fill_between(total_pv_production.index, battery_discharge, color='red', alpha=0.5, label='Battery discharge')
ax[1].fill_between(total_pv_production.index, battery_charge, color='green', alpha=0.5, label='Battery charge')
ax[1].legend(loc='best') # 'best' for automatic placement that doesn't overlap the plot
ax[1].set_ylabel('Power (kW)')
ax[1].set_xlabel('Time')

# Format the x-axis to show months and rotate labels
months = mdates.MonthLocator()  # every month
months_fmt = mdates.DateFormatter('%B')
ax[1].xaxis.set_major_locator(months)
ax[1].xaxis.set_major_formatter(months_fmt)
plt.xticks(rotation='vertical')

# Improve layout
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust for the suptitle

# Add text with the number of PV panels and batteries
pv_batteries_info = f'Number of PV panels needed: {num_pv}\nNumber of batteries needed: {num_batteries}'
fig.text(0.5, -0.05, pv_batteries_info, ha='center', va='center', fontsize=12, fontname='Times New Roman')

# Show the figure
plt.show()


#Scen2

def optimize_and_curtail(x):
    num_pv, num_batteries = x
    num_pv = int(num_pv)
    num_batteries = int(num_batteries)

    # Calculate the total PV production for each time step
    total_pv_production = num_pv * pv_1kW

    # Initialize the state of charge of the batteries
    soc = num_batteries * param_tech['BatteryCapacity']

    # Initialize curtailed energy
    curtailed_energy = 0

    # For each time step...
    for t in range(len(demand)):
        # Calculate the net power (production minus demand)
        net_power = total_pv_production.iloc[t] - demand.iloc[t]

        # If there is a surplus of power...
        if net_power > 0:
            # Charge the batteries, but don't exceed their total capacity
            charge = min(net_power, (num_batteries * param_tech['BatteryCapacity'] - soc) / param_tech['BatteryEfficiency'])
            soc += charge * param_tech['BatteryEfficiency']
            curtailed_energy += net_power - charge
        # If there is a deficit of power...
        else:
            # Discharge the batteries, but don't go below the minimum state of charge
            discharge = min(-net_power, soc - num_batteries * param_tech['BatteryCapacity'] * 0.3)
            soc -= discharge * param_tech['BatteryEfficiency']
    
    return curtailed_energy

# Optimize the number of PV panels and batteries to minimize curtailed energy
x0 = [num_pv, num_batteries]  # Initial guess
bounds = [(1, 100), (1, 100)]  # Bounds for the number of PV panels and batteries
result = optimize.minimize(optimize_and_curtail, x0, bounds=bounds, method='TNC')

opt_num_pv, opt_num_batteries = map(int, result.x)
opt_curtailed_energy = result.fun

print(f'Optimal number of PV panels: {opt_num_pv}')
print(f'Optimal number of batteries: {opt_num_batteries}')
print(f'Optimal curtailed energy: {opt_curtailed_energy}')

#Scen3

# Let's simulate a scenario where battery size is increased based on curtailed energy
curtailed_energy_threshold = 0.05 * total_demand  # Set your curtailed energy threshold here
while curtailed_energy > curtailed_energy_threshold:
    num_batteries += 1  # Increment the number of batteries
    total_battery_capacity = num_batteries * battery_capacity  # Recalculate total battery capacity
    soc = total_battery_capacity  # Reset the state of charge
    curtailed_energy = 0  # Reset the curtailed energy
    battery_charge = []  # Reset battery charge
    battery_discharge = []  # Reset battery discharge

    # Repeat the same loop for calculating battery charge and discharge
    for t in range(len(demand)):
        net_power = total_pv_production.iloc[t] - demand.iloc[t]
        if net_power > 0:
            remaining_space = total_battery_capacity - soc
            if net_power <= remaining_space:
                soc += net_power * param_tech['BatteryEfficiency']
                battery_charge.append(net_power * param_tech['BatteryEfficiency'])
            else:
                soc += remaining_space * param_tech['BatteryEfficiency']
                battery_charge.append(remaining_space * param_tech['BatteryEfficiency'])
                curtailed_energy += net_power - remaining_space
            battery_discharge.append(0)
        else:
            soc = max(soc + net_power / param_tech['BatteryEfficiency'], total_battery_capacity * 0.3)
            battery_charge.append(0)
            battery_discharge.append(-net_power / param_tech['BatteryEfficiency'])

print(f'Number of batteries needed to reduce curtailed energy below the threshold: {num_batteries}')
print(f'Curtailed energy with optimized number of batteries: {curtailed_energy} kWh')


#Scen4

# Let's simulate a scenario where number of PV panels is decreased based on curtailed energy
curtailed_energy_threshold = 0.05 * total_demand  # Set your curtailed energy threshold here
while curtailed_energy < curtailed_energy_threshold and num_pv > 1:
    num_pv -= 1  # Decrement the number of PV panels
    total_pv_production = num_pv * total_pv_output  # Recalculate total PV production
    soc = total_battery_capacity  # Reset the state of charge
    curtailed_energy = 0  # Reset the curtailed energy
    battery_charge = []  # Reset battery charge
    battery_discharge = []  # Reset battery discharge

    # Repeat the same loop for calculating battery charge and discharge
    for t in range(len(demand)):
        net_power = pv_1kW[t] - demand[t]
        if net_power > 0:
            remaining_space = total_battery_capacity - soc
            if net_power <= remaining_space:
                soc += net_power * param_tech['BatteryEfficiency']
                battery_charge.append(net_power * param_tech['BatteryEfficiency'])
            else:
                soc += remaining_space * param_tech['BatteryEfficiency']
                battery_charge.append(remaining_space * param_tech['BatteryEfficiency'])
                curtailed_energy += net_power - remaining_space
            battery_discharge.append(0)
        else:
            soc = max(soc + net_power / param_tech['BatteryEfficiency'], total_battery_capacity * 0.3)
            battery_charge.append(0)
            battery_discharge.append(-net_power / param_tech['BatteryEfficiency'])

print(f'Number of PV panels needed to increase curtailed energy above the threshold: {num_pv}')
print(f'Curtailed energy with optimized number of PV panels: {curtailed_energy} kWh')
