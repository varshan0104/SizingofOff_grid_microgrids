#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 15:36:51 2022

@author: rikkedihle
"""

def Input_data():
    Data = {} #Dictionary
    Data[0] = "Master problem data" #Data on the master problem
    
    Data[1] = {} #Data on the subproblems
    for i in range (3): #3 scenarios 
        Data[1][i] = "Sub_problem_data_for_scenario_" + str(i)
    return(Data)



def MasterProblem(Data, iteration):
    
    print(Data)
    
    #This is the master problem variable output
    x_1 = iteration * 2
    return(x_1)
    
   
def SubProblem(Data, x_1):
    
    
    
   
a = Input_data()
    
    
X_1_data = {} 
Cuts_daata = {}
Preliminary_results = {}

"""
Initiate the Benders Decomposition problem
"""

for iteration in range (10):
    
    """
    Initiate the master problem
    """
    
    x_1 = MasterProblem(Data[0], interation)
    print(x_1)
    X_1_data[iteration] = x_1
    
    """
    Initiate the sub problem
    """
    
    for scen in range(3):
        OBJ, Dual = SubProblem(Data[1][i])