import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy.optimize as optimize

# Load the demand data
demand = pd.read_csv(r'Load_Profile\ramp\results\output_file_aggregated.csv', index_col=0, header=None, parse_dates=True, squeeze=True, nrows=525541)
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


# Optimize the number of PV panels and batteries to minimize total curtailed energy
def optimize_and_curtail(x):
    num_pv, num_batteries = x
    num_pv = int(num_pv)
    num_batteries = int(num_batteries)

    # Calculate the total PV production for each time step
    total_pv_production = num_pv * pv_1kW

    # Initialize the state of charge of the batteries
    soc = num_batteries * param_tech['BatteryCapacity']

    # Initialize curtailed energy
    curtailed_energy = []

    # For each time step...
    for t in range(len(demand)):
        # Calculate the net power (production minus demand)
        net_power = total_pv_production.iloc[t] - demand.iloc[t]

        # If there is a surplus of power...
        if net_power > 0:
            # Charge the batteries, but don't exceed their total capacity
            charge = min(net_power, (num_batteries * param_tech['BatteryCapacity'] - soc) / param_tech['BatteryEfficiency'])
            soc += charge * param_tech['BatteryEfficiency']
            curtailed_energy.append(net_power - charge)
        # If there is a deficit of power...
        else:
            # Discharge the batteries, but don't go below the minimum state of charge
            discharge = min(-net_power, soc - num_batteries * param_tech['BatteryCapacity'] * 0.3)
            soc -= discharge * param_tech['BatteryEfficiency']
            curtailed_energy.append(0)
    
    return curtailed_energy


x0 = [num_pv, num_batteries]  # Initial guess
bounds = [(1, 100), (1, 100)]  # Bounds for the number of PV panels and batteries
result = optimize.minimize(lambda x: sum(optimize_and_curtail(x)), x0, bounds=bounds, method='TNC')

opt_num_pv, opt_num_batteries = map(int, result.x)
opt_curtailed_energy = optimize_and_curtail(result.x)

total_curtailed_energy = sum(opt_curtailed_energy)

# Create a figure with two subplots, specify the figure size
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(10,8))

# Set an overall title for the figure, make it bold and larger
fig.suptitle('Optimization Results', weight='bold', fontsize=14)

# Plot the production and demand on the first subplot
ax[0].plot(demand.index, demand.values, label='Demand', alpha=0.5)
ax[0].plot(total_pv_production.index, total_pv_production.values, label='Production', alpha=0.5)
ax[0].legend(loc='best') # 'best' for automatic placement that doesn't overlap the plot
ax[0].set_ylabel('Power (kW)')

# Plot the curtailed energy on the second subplot
ax[1].plot(demand.index, opt_curtailed_energy, label='Curtailed Energy', alpha=0.5)
ax[1].legend(loc='best') # 'best' for automatic placement that doesn't overlap the plot
ax[1].set_ylabel('Power (kW)')
ax[1].set_xlabel('Time')

# Format the x-axis to show months and rotate labels
months = mdates.MonthLocator()  # every month
months_fmt = mdates.DateFormatter('%B')
ax[1].xaxis.set_major_locator(months)
ax[1].xaxis.set_major_formatter(months_fmt)
plt.xticks(rotation='vertical')

# Add text with the optimal number of PV panels, batteries, and curtailed energy
opt_info = f'Optimal number of PV panels: {opt_num_pv}\nOptimal number of batteries: {opt_num_batteries}\nTotal curtailed energy ila året: {total_curtailed_energy}kW\n'
fig.text(0.5, -0.05, opt_info, ha='center', va='center', fontsize=12, fontname='Times New Roman')

# Show the figure
plt.show()

def increase_additional_batteries():
    global num_batteries, param_tech, num_pv, pv_1kW, demand

    # Initialize the state of charge of the main batteries
    soc = num_batteries * param_tech['BatteryCapacity']

    # Initialize the maximum number of additional batteries
    max_additional_batteries = 0

    # Initialize curtailed energy and additional batteries per day
    curtailed_energy_per_day = []
    additional_batteries_per_day = []

    # Iterate over each day
    for day in range(int(len(demand) / 24)):
        # Initialize the state of charge and the number of the additional batteries for this day
        soc_additional = 0
        num_additional_batteries = 0

        # Initialize curtail for this day
        curtail = 0

        # Iterate over each hour in this day
        for hour in range(24):
            t = day * 24 + hour

            # Calculate the total PV production for this hour
            total_pv_production = num_pv * pv_1kW.iloc[t]

            # Calculate the net power (production minus demand) for this hour
            net_power = total_pv_production - demand.iloc[t]

            # If there is a surplus of power...
            if net_power > 0:
                # Charge the main batteries, but don't exceed their total capacity
                charge = min(net_power, (num_batteries * param_tech['BatteryCapacity'] - soc) / param_tech['BatteryEfficiency'])
                soc += charge * param_tech['BatteryEfficiency']
                curtail = net_power - charge

                # If there's curtailed energy, charge the additional batteries
                if curtail > 0:
                    # If the current additional battery is full, add a new one
                    if soc_additional + curtail / param_tech['BatteryEfficiency'] > param_tech['BatteryCapacity']:
                        num_additional_batteries += 1
                        soc_additional = 0

                    # Charge the additional batteries
                    charge_additional = min(curtail, (param_tech['BatteryCapacity'] - soc_additional) / param_tech['BatteryEfficiency'])
                    soc_additional += charge_additional * param_tech['BatteryEfficiency']

            # If there is a deficit of power...
            else:
                # Discharge the main batteries, but don't go below the minimum state of charge
                discharge = min(-net_power, soc - num_batteries * param_tech['BatteryCapacity'] * 0.3)
                soc -= discharge * param_tech['BatteryEfficiency']

        # Update the maximum number of additional batteries if necessary
        max_additional_batteries = max(max_additional_batteries, num_additional_batteries)

        # Store the curtailed energy and the number of additional batteries for this day
        curtailed_energy_per_day.append(curtail)
        additional_batteries_per_day.append(num_additional_batteries)

    return curtailed_energy_per_day, additional_batteries_per_day, max_additional_batteries


curtailed_energy, additional_batteries, max_batteries = increase_additional_batteries()

print(f'Maksimalt antall ekstra batterier som trengs for å lagre all curtailed energy: {max_batteries}')

curtailed_energy, additional_batteries, max_batteries = increase_additional_batteries()

# Create a figure with two subplots, specify the figure size
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(10,8))

# Set an overall title for the figure, make it bold and larger
fig.suptitle('Basic coverage of demand', weight='bold', fontsize=14)

# Plot the production, demand and battery coverage on the first subplot with transparency
ax[0].plot(demand.index, demand.values, label='Demand', alpha=0.5)
ax[0].plot(total_pv_production.index, total_pv_production.values, label='Production', alpha=0.5)
ax[0].legend(loc='best') # 'best' for automatic placement that doesn't overlap the plot
ax[0].set_ylabel('Power (kW)')


if len(demand.index[::24]) > len(additional_batteries):
    x_data = demand.index[::24][:-1]
else:
    x_data = demand.index[::24]

ax[1].plot(x_data, additional_batteries, color='blue', label='Additional batteries')
ax[1].legend(loc='best') # 'best' for automatic placement that doesn't overlap the plot
ax[1].set_ylabel('Number of batteries')
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
pv_batteries_info = f'Number of PV panels needed: {num_pv}\nNumber of batteries needed: {num_batteries}\nMax additional batteries needed: {max_batteries}'
fig.text(0.5, -0.05, pv_batteries_info, ha='center', va='center', fontsize=12, fontname='Times New Roman')

# Show the figure
plt.show()

def reduce_pv_panels(max_attempts=100):
    global num_batteries, param_tech, num_pv, pv_1kW, demand

    # Initialize the state of charge of the batteries
    soc = num_batteries * param_tech['BatteryCapacity']

    # Initialize the number of PV panels
    num_pv_reduced = num_pv

    # Initialize the attempt counter
    attempts = 0

    # Iterate until demand is not met or the maximum number of attempts is reached
    while attempts < max_attempts:
        # Initialize variables for tracking whether demand is met and the total curtailed energy
        demand_met = True
        curtailed_energy = 0

        # Iterate over each time step
        for t in range(len(demand)):
            # Calculate the total PV production for this time step
            total_pv_production = num_pv_reduced * pv_1kW.iloc[t]

            # Calculate the net power (production minus demand)
            net_power = total_pv_production - demand.iloc[t]

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

                # If the batteries can't cover the deficit, the demand is not met
                if -net_power > discharge:
                    demand_met = False
                    break

        # If the demand was met, we can stop reducing the number of PV panels
        if demand_met:
            break

        # Otherwise, increase the attempt counter, reduce the number of PV panels and repeat the simulation
        attempts += 1
        num_pv_reduced -= 1
        
        # Ensure the number of PV panels doesn't go below zero
        if num_pv_reduced < 0:
            num_pv_reduced = 0
            break

    return num_pv_reduced, curtailed_energy


num_pv_reduced, curtailed_energy = reduce_pv_panels()

print(f'Number of PV panels needed to meet demand with increased battery usage: {num_pv_reduced}')
print(f'Total curtailed energy with reduced number of PV panels: {curtailed_energy}')

def reduce_pv_panels():
    global num_batteries, param_tech, num_pv, pv_1kW, demand

    # Reduce the number of PV panels by one
    num_pv_reduced = num_pv - 1
    if num_pv_reduced < 0:
        num_pv_reduced = 0

    # Initialize the state of charge of the batteries
    soc = num_batteries * param_tech['BatteryCapacity']

    # Initialize variables for tracking the total demand and the amount of unmet demand
    total_demand = 0
    unmet_demand = 0

    # Initialize lists to store the charge, discharge, and unmet demand for each time step
    charge_list = [0]*len(demand)
    discharge_list = [0]*len(demand)
    unmet_demand_list = [0]*len(demand)

    # Iterate over each time step
    for t in range(len(demand)):
        # Calculate the total PV production for this time step
        total_pv_production = num_pv_reduced * pv_1kW.iloc[t]

        # Calculate the net power (production minus demand)
        net_power = total_pv_production - demand.iloc[t]

        # Add the demand for this time step to the total demand
        total_demand += demand.iloc[t]

        # If there is a surplus of power...
        if net_power > 0:
            # Charge the batteries, but don't exceed their total capacity
            charge = min(net_power, (num_batteries * param_tech['BatteryCapacity'] - soc) / param_tech['BatteryEfficiency'])
            soc += charge * param_tech['BatteryEfficiency']
            charge_list[t] = charge
        # If there is a deficit of power...
        else:
            # Discharge the batteries, but don't go below the minimum state of charge
            discharge = min(-net_power, soc - num_batteries * param_tech['BatteryCapacity'] * 0.3)
            soc -= discharge * param_tech['BatteryEfficiency']
            discharge_list[t] = discharge

            # If the batteries can't cover the deficit, add it to the unmet demand
            if -net_power > discharge:
                unmet_demand += -net_power - discharge
                unmet_demand_list[t] = -net_power - discharge

    # Calculate the percentage of unmet demand
    percentage_unmet = (unmet_demand / total_demand) * 100

    return num_pv_reduced, percentage_unmet, charge_list, discharge_list, unmet_demand_list


num_pv_reduced, percentage_unmet, charge_list, discharge_list, unmet_demand_list = reduce_pv_panels()

# Create a figure with two subplots, specify the figure size
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(10,8))

# Set an overall title for the figure, make it bold and larger
fig.suptitle('Basic coverage of demand', weight='bold', fontsize=14)

# Plot the production, demand and battery coverage on the first subplot with transparency
ax[0].plot(demand.index, demand.values, label='Demand', alpha=0.5)
ax[0].plot(demand.index, num_pv_reduced * pv_1kW, label='Production', alpha=0.5)
ax[0].legend(loc='best') # 'best' for automatic placement that doesn't overlap the plot
ax[0].set_ylabel('Power (kW)')

# Plot the battery charge, discharge and unmet demand on the second subplot
ax[1].plot(demand.index, charge_list, color='green', label='Battery charge')
ax[1].plot(demand.index, discharge_list, color='red', label='Battery discharge')
ax[1].scatter(demand.index, unmet_demand_list, color='red')
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
pv_batteries_info = f'Number of PV panels needed: {num_pv_reduced}\nNumber of batteries needed: {num_batteries}\nPercentage of unmet demand: {percentage_unmet}%'
fig.text(0.5, -0.05, pv_batteries_info, ha='center', va='center', fontsize=12, fontname='Times New Roman')

# Show the figure
plt.show()

def reduce_batteries():
    global num_batteries, param_tech, num_pv, pv_1kW, demand

    # Reduce the number of batteries by one
    num_batteries_reduced = num_batteries - 1
    if num_batteries_reduced < 0:
        num_batteries_reduced = 0

    # Initialize the state of charge of the batteries
    soc = num_batteries_reduced * param_tech['BatteryCapacity']

    # Initialize variables for tracking the total demand and the amount of unmet demand
    total_demand = 0
    unmet_demand = 0

    # Initialize lists to store the charge, discharge, and unmet demand for each time step
    charge_list = [0]*len(demand)
    discharge_list = [0]*len(demand)
    unmet_demand_list = [0]*len(demand)

    # Iterate over each time step
    for t in range(len(demand)):
        # Calculate the total PV production for this time step
        total_pv_production = num_pv * pv_1kW.iloc[t]

        # Calculate the net power (production minus demand)
        net_power = total_pv_production - demand.iloc[t]

        # Add the demand for this time step to the total demand
        total_demand += demand.iloc[t]

        # If there is a surplus of power...
        if net_power > 0:
            # Charge the batteries, but don't exceed their total capacity
            charge = min(net_power, (num_batteries_reduced * param_tech['BatteryCapacity'] - soc) / param_tech['BatteryEfficiency'])
            soc += charge * param_tech['BatteryEfficiency']
            charge_list[t] = charge
        # If there is a deficit of power...
        else:
            # Discharge the batteries, but don't go below the minimum state of charge
            discharge = min(-net_power, soc - num_batteries_reduced * param_tech['BatteryCapacity'] * 0.3)
            soc -= discharge * param_tech['BatteryEfficiency']
            discharge_list[t] = discharge

            # If the batteries can't cover the deficit, add it to the unmet demand
            if -net_power > discharge:
                unmet_demand += -net_power - discharge
                unmet_demand_list[t] = -net_power - discharge

    # Calculate the percentage of unmet demand
    percentage_unmet = (unmet_demand / total_demand) * 100

    return num_batteries_reduced, percentage_unmet, charge_list, discharge_list, unmet_demand_list

num_batteries_reduced, percentage_unmet, charge_list, discharge_list, unmet_demand_list = reduce_batteries()

# Create a figure with two subplots, specify the figure size
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(10,8))

# Set an overall title for the figure, make it bold and larger
fig.suptitle('Basic coverage of demand', weight='bold', fontsize=14)

# Plot the production, demand and battery coverage on the first subplot with transparency
ax[0].plot(demand.index, demand.values, label='Demand', alpha=0.5)
ax[0].plot(demand.index, num_pv * pv_1kW, label='Production', alpha=0.5)
ax[0].legend(loc='best') # 'best' for automatic placement that doesn't overlap the plot
ax[0].set_ylabel('Power (kW)')

# Plot the battery charge, discharge and unmet demand on the second subplot
ax[1].plot(demand.index, charge_list, color='green', label='Battery charge')
ax[1].plot(demand.index, discharge_list, color='red', label='Battery discharge')
ax[1].scatter(demand.index, unmet_demand_list, color='red')
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
pv_batteries_info = f'Number of PV panels needed: {num_pv}\nNumber of batteries needed: {num_batteries_reduced}\nPercentage of unmet demand: {percentage_unmet}%'
fig.text(0.5, -0.05, pv_batteries_info, ha='center', va='center', fontsize=12, fontname='Times New Roman')

# Show the figure
plt.show()

