# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition
'''

from ramp.core.core import User, np, pd
User_list = []

# Read the Excel file
df = pd.read_excel('Load_Profile/ramp/input_files/Appliances_and_users.xlsx', sheet_name='User')

for index, row in df.iterrows():

    # Hent innholdet i cellene A, B og C i den gjeldende raden
    cell_a_value = row['user']
    cell_b_value = row['n_users']
    cell_c_value = row['us_pref']

    # Opprett og skriv ut brukerinformasjon
    User_info = User(cell_a_value, cell_b_value, cell_c_value)
    User_list.append(User_info)




df2 = pd.read_excel('Load_Profile/ramp/input_files/Appliances_and_users.xlsx', sheet_name='Appliances_Spring')

def appliance_iterate(df2, User_list):

    Appliance_buffer_list = []
    User_buffer_list = []
    Time_window_list = []

    # For appliances
    for index, row in df2.iterrows():
        cell_a_value2 = row['user']
        cell_b_value2 = row['appliance_name']
        cell_c_value2 = row['number']
        cell_d_value2 = row['P']
        cell_e_value2 = row['num_windows']
        cell_f_value2 = row['func_time']
        cell_g_value2 = row['r_t']
        cell_h_value2 = row['func_cycle']
        cell_j_value2 = row['fixed']
        cell_k_value2 = row['fixed_cycle']
        cell_l_value2 = row['occasional_use']
        cell_m_value2 = row['flat']
        cell_n_value2 = row['thermal_P_var']
        cell_o_value2 = row['pref_index']
        cell_p_value2 = row['wd_we_type']
        cell_q_value2 = row['year_min']
        cell_r_value2 = row['initial_share']
        cell_s_value2 = row['From_time']
        cell_t_value2 = row['To_time']
        cell_u_value2 = row['r_w']

        key_user_buffer = cell_a_value2
        key_appliance = []
        time_window_buffer_list = []


        key_appliance.append(cell_b_value2)
        key_appliance.append(cell_c_value2)
        key_appliance.append(cell_d_value2)
        key_appliance.append(cell_e_value2)
        key_appliance.append(cell_f_value2)
        key_appliance.append(cell_g_value2)
        key_appliance.append(cell_h_value2)
        key_appliance.append(cell_j_value2)
        key_appliance.append(cell_k_value2)
        key_appliance.append(cell_l_value2)
        key_appliance.append(cell_m_value2)
        key_appliance.append(cell_n_value2)
        key_appliance.append(cell_o_value2)
        key_appliance.append(cell_p_value2)
        key_appliance.append(cell_q_value2)
        key_appliance.append(cell_r_value2)
        time_window_buffer_list.append(cell_s_value2)
        time_window_buffer_list.append(cell_t_value2)
        time_window_buffer_list.append(cell_u_value2)

        User_buffer_list.append(key_user_buffer)
        Appliance_buffer_list.append(key_appliance)
        Time_window_list.append(time_window_buffer_list)

    return Appliance_buffer_list, User_buffer_list, Time_window_list


run_appliance_iterate = appliance_iterate(df2, User_list)

i = 0
for object_appliance in run_appliance_iterate[1]:

    user_check = next((u for u in User_list if u.user_name == object_appliance), None)
    cell_b_value3 = run_appliance_iterate[0][i][0]
    cell_c_value3 = run_appliance_iterate[0][i][1]
    cell_d_value3 = run_appliance_iterate[0][i][2]
    cell_e_value3 = run_appliance_iterate[0][i][3]
    cell_f_value3 = run_appliance_iterate[0][i][4]
    cell_g_value3 = run_appliance_iterate[0][i][5]
    cell_h_value3 = run_appliance_iterate[0][i][6]
    cell_i_value3 = run_appliance_iterate[0][i][7]
    cell_j_value3 = run_appliance_iterate[0][i][8]
    cell_k_value3 = run_appliance_iterate[0][i][9]
    cell_l_value3 = run_appliance_iterate[0][i][10]
    cell_m_value3 = run_appliance_iterate[0][i][11]
    cell_n_value3 = run_appliance_iterate[0][i][12]
    cell_o_value3 = run_appliance_iterate[0][i][13]
    cell_p_value3 = run_appliance_iterate[0][i][14]
    cell_q_value3 = run_appliance_iterate[0][i][15]
    window_time_from = run_appliance_iterate[2][i][0]
    window_time_to = run_appliance_iterate[2][i][1]
    window_time_r_t = run_appliance_iterate[2][i][2]

    cell_b_value3 = user_check.Appliance(user_check, cell_c_value3, cell_d_value3, cell_e_value3,cell_f_value3,cell_g_value3,cell_h_value3)
    cell_b_value3.windows([window_time_from, window_time_to], r_w=window_time_r_t)

    i += 1