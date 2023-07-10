import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy.optimize as optimize

# Load the demand data
demand = pd.read_csv(r'Load_Profile\ramp\results\output_file_ecomoyu.csv', index_col=0, header=None, parse_dates=True, squeeze=True, nrows=525541)
demand.index = pd.date_range(start='2023-01-01 00:00', end='2023-12-31 23:00', freq='min')
demand = demand.resample('15min').interpolate(method='linear')
demand = demand.loc[:].div(1000)  # Convert from Wh to kWh

# Load the PV production data
pv_1kW = pd.read_csv('pvlib_result.csv', index_col=0, header=None, parse_dates=True, skiprows=1).squeeze("columns")
pv_1kW = pv_1kW.resample('15min').interpolate(method='linear')
pv_1kW = pv_1kW.loc[:].div(1000)  # Normalize to 1 kW

# Define the battery parameters
param_tech = {'BatteryCapacity': 200*12/1000,            #kWh
              'BatteryEfficiency': .9,
              'InverterEfficiency': .93,
              'timestep': .25,
              'MaxPower': 3500/1000,                       #kWh (maximum output of the inverter)
              'BatteryDegradation': 0.02                   # Assume 2% capacity loss per year
             }

# Initialize a list to store the state of charge for each time step
soc_values = []

# Calculate the total energy demand for a year
total_demand = demand.sum()

# Calculate the total energy output from a PV panel for a year
total_pv_output = pv_1kW.sum()

# Calculate the number of PV panels needed
num_pv = int(np.ceil(total_demand / total_pv_output))

# Calculate the maximum energy demand for a day
max_daily_demand = demand.resample('D').sum().max()

# Calculate the usable energy capacity of a battery, considering degradation and minimum SoC
usable_battery_capacity = param_tech['BatteryCapacity'] * (1 - param_tech['BatteryDegradation']) * param_tech['BatteryEfficiency'] * 0.8 * 0.7

# Calculate the number of batteries needed considering the usable capacity
num_batteries = int(np.ceil(max_daily_demand / usable_battery_capacity))

# Calculate the total PV production for each time step
total_pv_production = num_pv * pv_1kW

# Initialize the state of charge of the batteries
soc = num_batteries * param_tech['BatteryCapacity']

# Initialize lists to store the battery charge and discharge for each time step
battery_charge = []
battery_discharge = []

# Calculate the maximum state of charge
max_soc = num_batteries * param_tech['BatteryCapacity']


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
        soc = max(soc + net_power / param_tech['BatteryEfficiency'], num_batteries * param_tech['BatteryCapacity'] * 0.2)
        battery_charge.append(0)
        battery_discharge.append(-net_power / param_tech['BatteryEfficiency'])

    # If there is a surplus of power...
    if net_power > 0:
        # Charge the batteries, but don't exceed their total capacity
        soc = min(soc + net_power * param_tech['BatteryEfficiency'], num_batteries * param_tech['BatteryCapacity'])
        soc_values.append(soc / max_soc * 100)
        
    # If there is a deficit of power...
    else:
        # Discharge the batteries, but don't go below the minimum state of charge
        soc = max(soc + net_power / param_tech['BatteryEfficiency'], num_batteries * param_tech['BatteryCapacity'] * 0.2)
        soc_values.append(soc / max_soc * 100)



# Create a figure with two subplots, specify the figure size
fig, ax = plt.subplots(2, 1, sharex=True, figsize=(10,8))

# Set an overall title for the figure, make it bold and larger
fig.suptitle('Basic coverage of demand', weight='bold', fontsize=14)

# Plot the production, demand and battery coverage on the first subplot with transparency
ax[0].plot(demand.index, demand.values, label='Demand', alpha=0.5)
ax[0].plot(total_pv_production.index, total_pv_production.values, label='Production', alpha=0.5)
ax[0].legend(loc='best') # 'best' for automatic placement that doesn't overlap the plot
ax[0].set_ylabel('Power (kW)')

# Plot the state of charge on the second subplot
ax[1].plot(total_pv_production.index, soc_values, color='green', alpha=0.5, label='State of Charge (%)')
ax[1].legend(loc='best') # 'best' for automatic placement that doesn't overlap the plot
ax[1].set_ylabel('State of Charge (%)')
ax[1].set_xlabel('Months')

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
plt.savefig("results/basic_coverage.pdf", format="pdf", bbox_inches="tight")
plt.show()


def iteratively_reduce_batteries():
    global num_batteries, param_tech, num_pv, pv_1kW, demand

    # Initialize a list to store the results for each number of batteries
    results = []

    # Initialize the number of batteries to be reduced
    num_batteries_reduced = num_batteries

    while True:
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

        # Add the results for this number of batteries to the list of results
        results.append((num_batteries_reduced, percentage_unmet, charge_list, discharge_list, unmet_demand_list))

        # If the percentage of unmet demand is greater than 5%, stop reducing the number of batteries
        if percentage_unmet > 5:
            break

        # Reduce the number of batteries by one
        num_batteries_reduced -= 1
        if num_batteries_reduced < 0:
            break

    return results


results = iteratively_reduce_batteries()

for num_batteries_reduced, percentage_unmet, charge_list, discharge_list, unmet_demand_list in results:
    # Create a figure with two subplots, specify the figure size
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(10,8))

    # Set an overall title for the figure, make it bold and larger
    fig.suptitle(f'Coverage of demand with {num_batteries_reduced} batteries', weight='bold', fontsize=14)

    # Plot the production, demand and battery coverage on the first subplot with transparency
    ax[0].plot(demand.index, demand.values, label='Demand', alpha=0.5)
    ax[0].plot(demand.index, num_pv * pv_1kW, label='Production', alpha=0.5)
    ax[0].legend(loc='best') # 'best' for automatic placement that doesn't overlap the plot
    ax[0].set_ylabel('Power (kW)')

    # Plot the battery charge, discharge and unmet demand on the second subplot
    #ax[1].plot(demand.index, charge_list, color='green', label='Battery charge', alpha=0.5)
    #ax[1].plot(demand.index, discharge_list, color='red', label='Battery discharge', alpha=0.5)
    scatter_color = ['blue' if value > 0 else 'white' for value in unmet_demand_list]
    ax[1].scatter(demand.index, unmet_demand_list , color=scatter_color, label='Unmet Demand', alpha=1.0, zorder=2)
    ax[1].legend(loc='best')
    ax[1].set_ylabel('Power (kW)')
    ax[1].set_xlabel('Months')


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

# Create a list of the number of batteries and the percentage of unmet demand for each result
num_batteries_list = [result[0] for result in results]
percentage_unmet_list = [result[1] for result in results]

# Create a color map where 100% demand coverage is green and 95% demand coverage is red
colors = ['green' if percentage_unmet == 0 else 'red' for percentage_unmet in percentage_unmet_list]

# Create a list of the number of batteries and the percentage of unmet demand for each result
num_batteries_list = [result[0] for result in results]
percentage_unmet_list = [result[1] for result in results]

# Create a color map where 100% demand coverage is green and 95% demand coverage is red
colors = ['green' if percentage_unmet == 0 else 'red' for percentage_unmet in percentage_unmet_list]


def iteratively_change_pv_and_batteries(num_pv_initial, num_batteries_initial):
    global param_tech, pv_1kW, demand

    # Set the range of PV panels and batteries to consider
    min_pv = max(1, num_pv_initial - 7)
    max_pv = num_pv_initial + 3
    min_batteries = max(1, num_batteries_initial - 7)
    max_batteries = num_batteries_initial + 3

    # Initialize the matrix to store the results
    matrix = np.zeros((max_pv - min_pv + 1, max_batteries - min_batteries + 1))

    # Iterate over each number of PV panels
    for num_pv in range(min_pv, max_pv + 1):
        # Iterate over each number of batteries
        print("Please wait")
        for num_batteries in range(min_batteries, max_batteries + 1):
            # Initialize the state of charge of the batteries
            soc = num_batteries * param_tech['BatteryCapacity']

            # Initialize variables for tracking the total demand and the amount of unmet demand
            total_demand = 0
            unmet_demand = 0

            # Calculate the total PV production for each time step
            total_pv_production = num_pv * pv_1kW

            # Iterate over each time step
            for t in range(len(demand)):
                # Calculate the net power (production minus demand)
                net_power = total_pv_production.iloc[t] - demand.iloc[t]

                # Add the demand for this time step to the total demand
                total_demand += demand.iloc[t]

                # If there is a surplus of power...
                if net_power > 0:
                    # Charge the batteries, but don't exceed their total capacity
                    charge = min(net_power, (num_batteries * param_tech['BatteryCapacity'] - soc) / param_tech['BatteryEfficiency'])
                    soc += charge * param_tech['BatteryEfficiency']
                # If there is a deficit of power...
                else:
                    # Discharge the batteries, but don't go below the minimum state of charge
                    discharge = min(-net_power, soc - num_batteries * param_tech['BatteryCapacity'] * 0.3)
                    soc -= discharge * param_tech['BatteryEfficiency']
                    
                    # If the batteries can't cover the deficit, add it to the unmet demand
                    if -net_power > discharge:
                        unmet_demand += -net_power - discharge

            # Calculate the percentage of unmet demand
            percentage_unmet = (unmet_demand / total_demand) * 100

            # Store the percentage of unmet demand in the matrix
            matrix[num_pv - min_pv, num_batteries - min_batteries] = percentage_unmet

    return matrix

# Define the initial number of PV panels and batteries
num_pv_initial = num_pv# Define your initial number of PV panels here
num_batteries_initial = num_batteries# Define your initial number of batteries here

# Run the simulation
matrix = iteratively_change_pv_and_batteries(num_pv_initial, num_batteries_initial)

min_pv = max(1, num_pv_initial - 7)
max_pv = num_pv_initial + 3
min_batteries = max(1, num_batteries_initial - 7)
max_batteries = num_batteries_initial + 3

# Plot the matrix
plt.figure(figsize=(10, 10))
plt.imshow(matrix, cmap='RdYlGn_r', origin='lower')
plt.colorbar(label='Unmet demand (%)')
plt.xticks(range(max_batteries - min_batteries + 1), range(min_batteries, max_batteries + 1))
plt.yticks(range(max_pv - min_pv + 1), range(min_pv, max_pv + 1))
plt.xlabel('Number of batteries')
plt.ylabel('Number of PV panels')
plt.title('Unmet demand for different numbers of PV panels and batteries')

# Add the percentage of unmet demand in each cell
for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        plt.text(j, i, f'{matrix[i, j]:.1f}', ha='center', va='center', color='black')

plt.savefig("resultmatrix.pdf", format="pdf", bbox_inches="tight")
plt.show()