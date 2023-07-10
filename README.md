# Sizing of Off-Grid Microgrids

This repository contains Python scripts for sizing off-grid microgrids. The scripts are organized as follows:

- `main.py`: This is the main script that runs the entire process.
- `Load_Profile/ramp/load_profile_run.py`: This script is responsible for handling the load profile.
- `Production_Profile/PV_production_data.py`: This script manages the PV production data.
- `Production_Profile/Run_simulation.py`: This script runs the simulation for the production profile.
- `importproductdata.py`: This script is used for importing product data.

## Getting Started

This project is part of a master's thesis on the optimal sizing of off-grid microgrids. It is run under the GridVille NTNU. To get started, clone the repository and install the required Python packages.

## Getting Started

Before running the code, ensure that you're in the correct directory. The directory should be `...SizingOff_grid_microgrids`.

### Prerequisites

1. **Python**: The code is written in Python. Make sure you have it installed on your machine.

2. **Packages**: This project requires specific Python packages. Ensure you've installed all necessary packages before running the code.

    ```python
    import os
    import threading
    ```

3. **Data files**: The project uses data from specific Excel files. Ensure the "Appliances_and_users" Excel file in the directory `Load_Profile/ramp/input_files` is filled out.

### Execution

The code can be run by executing the `main.py` file. 

If everything is set up correctly, it should print "This is the main thread" to the console. If you see the message "This is not the main thread", then the threading is not set up correctly.

The program also creates a `results` directory if it doesn't already exist, where the results of the computation can be stored.

### Modules

There are several components to this codebase:

- `load_profile`: This function (currently commented out) is likely responsible for handling load profiles.
- `PV_production_data`: This function appears to handle photovoltaic production data.
- `Run_simulation.py`: The code from this file is being read and executed. Make sure this file exists in the `Production_Profile` directory.

### Note

There's a section of the code that's commented out, which seems to involve analysis functions. If you plan to use this part of the code, make sure you uncomment it and that all the necessary data files and functions are available.

## Author

The codebase was developed by Varshan Erik Shankar as part of his master's thesis.


## Import Module

In addition to the main script, the project also includes a module for importing product data. This module, `importproductdata.py`, contains the following functions:

- `read_pv_data(file_path)`: This function reads data from an Excel file about photovoltaic (PV) panels. It returns a dictionary of technical data and a nested dictionary for each PV panel's data.

- `read_battery_data(file_path)`: This function reads data from an Excel file about batteries. It returns a list of battery data.

- `read_location_data(file_path)`: This function reads location data from an Excel file. It returns a `Location` object (from the `pvlib` library) containing the latitude, longitude, timezone, and altitude of the location.

### Prerequisites

To run `importproductdata.py`, you'll need the following Python packages:

```python
import pandas as pd
import pytz
from pvlib.location import Location
```
## Data Files

The `importproductdata.py` module expects Excel files with specific sheet names and formats. For each function, the Excel file should have:

- `read_pv_data(file_path)`: A sheet named 'PV' with columns for each PV panel and a row for each parameter.
- `read_battery_data(file_path)`: A sheet named 'Battery' with columns for each battery type and a row for each parameter.
- `read_location_data(file_path)`: A sheet named 'Location' with columns 'latitude', 'longitude', 'timezone', and 'altitude'.


## Load Profile Generation

The module `load_profile_run.py` is part of an open-source stochastic model, RAMP, for the generation of multi-energy load profiles in off-grid areas.

### Authors

This module was created by:

- Francesco Lombardi, Politecnico di Milano
- Sergio Balderrama, Université de Liège
- Sylvain Quoilin, KU Leuven
- Emanuela Colombo, Politecnico di Milano

### Prerequisites

To run `load_profile_run.py`, you'll need the following Python packages:

```python
import sys
import os
import numpy as np
import pandas as pd
```
## Function

The main function in this module is `load_profile()`, which generates a total number of specified days' load profiles, post-processes the results, generates plots, and saves the data in CSV files in the results folder.

The function considers several input files, which are Python scripts defined as numbers in a list. The number of days a load profile for each input file will have is defined in a dictionary. The function then calls the stochastic process and saves the results in a list of stochastic profiles.

The `load_profile()` function also depends on two other modules: `stochastic_process` and `post_process`. Make sure these modules are accessible and correctly functioning.


## Input Data Handling

The module `input_file_1.py` reads and processes input data for the load profiles. The data is read from an Excel file, `Appliances_and_users.xlsx`, which contains user and appliance information.

### Prerequisites

To run `input_file_1.py`, you'll need the following Python packages:

```python
import pandas as pd
from ramp.core.core import User, np
```
## Functionality

The module contains the function `appliance_iterate(df2, User_list)`, which iterates over the rows of the 'Appliances_Spring' sheet in the Excel file, creating a list of user-appliance data. The function returns three lists: one for appliance data, one for user data, and one for time window data.

The module also creates a User object for each user, stored in User_list. Each User object also has an Appliance object, representing the appliances the user uses.

## Data Files

The `input_file_1.py` module expects an Excel file with the name `Appliances_and_users.xlsx`, which should contain two sheets: 'User' and 'Appliances_Spring'.

The 'User' sheet should have columns 'user', 'n_users', and 'us_pref'. The 'Appliances_Spring' sheet should have the columns 'user', 'appliance_name', 'number', 'P', 'num_windows', 'func_time', 'r_t', 'func_cycle', 'fixed', 'fixed_cycle', 'occasional_use', 'flat', 'thermal_P_var', 'pref_index', 'wd_we_type', 'year_min', 'initial_share', 'From_time', 'To_time', 'r_w'.


## PV Production Data Handling

The module `PV_production_data.py` processes input data for photovoltaic (PV) production and creates a plot of the DC output. 

### Prerequisites

To run `PV_production_data.py`, you'll need the following Python packages:

```python
import pvlib
from pvlib.iotools import get_pvgis_tmy
import pandas as pd
import matplotlib.pyplot as plt
import pytz
from pvlib.location import Location
```

## Functionality

The main function in this module is `PV_production_data()`, which reads PV data from an Excel file `productdata.xlsx` and location data from another Excel file `Locationandload_data.xlsx` using the `read_pv_data(file_path)` and `read_location_data(file_path)` functions respectively.

The function then obtains meteorological data from the PVGIS database for the given location, processes this data into the format required by pvlib, calculates the module temperature using the Faiman model, and calculates the DC output of the PV system using the PVWatts model.

The final DC output data is saved in a CSV file `pvlib_result.csv`, and a plot of the DC output is created and saved as a PDF file `results/DCOutput.pdf`.

## Data Files

The `PV_production_data.py` module expects two Excel files:

- `productdata.xlsx` which should have a sheet named 'PV' with the following columns: 'P_max', 'v_oc', 'i_sc', 'alpha_sc', 'beta_voc', 'gamma_pmp', 'temp_ref', 'surface_tilt', 'surface_azimuth'.
- `Locationandload_data.xlsx` which should have a sheet named 'Location' with the following columns: 'latitude', 'longitude', 'timezone', 'altitude'.



## Simulation Run

The module `Run_simulation.py` runs a simulation to determine the optimal number of photovoltaic (PV) panels and batteries needed to meet demand.

### Prerequisites

To run `Run_simulation.py`, you'll need the following Python packages:

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy.optimize as optimize
```

## Functionality

The module first reads demand data from `Load_Profile/ramp/results/output_file_ecomoyu.csv` and PV production data from `pvlib_result.csv`. It then calculates the total energy demand and the total energy output from a PV panel for a year.

Based on these values, the module calculates the number of PV panels and batteries needed. It also calculates the battery's state of charge at each time step, as well as the battery charge and discharge.

After these initial calculations, the module runs a simulation that iteratively reduces the number of batteries and calculates the percentage of unmet demand. The results are plotted.

The module also contains a function, `iteratively_change_pv_and_batteries(num_pv_initial, num_batteries_initial)`, which runs a simulation for different numbers of PV panels and batteries and plots the results.

## Data Files

The `Run_simulation.py` module expects two CSV files:

- `Load_Profile/ramp/results/output_file_ecomoyu.csv` which should contain the load profile.
- `pvlib_result.csv` which should contain the PV production data.
