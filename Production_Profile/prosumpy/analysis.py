"""This module contains functions to analyze the results of the dispatch algorithm"""

import numpy as np

def print_analysis(pv, demand, param, E):
    """ Print statistics and information of the dispatched solution

    Arguments
        pv (pd.Series): PV timeseries
        demand (pd.Series): demand timeseries
        param (dict): dictionary of technical parameters
        E (dict): dictionary of energy flows as estimated by the algorithm
    Returns
        none

    """
    timestep = param['timestep']
    SelfConsumption = np.sum(E['inv2load']) * timestep
    TotalUncoveredDemand = np.sum(E['notCoveredDemand']) * timestep         #Energi som batteriet ikke dekker
    TotalSurplus = np.sum(E['energySurplus']) * timestep                    #Overskuddsenergi som går tapt
    TotalLoad = demand.sum() * timestep
    TotalPV = pv.sum() * timestep
    TotalBatteryGeneration = np.sum(E['store2inv']) * timestep
    TotalBatteryConsumption = np.sum(E['pv2store']) * timestep
    BatteryLosses = TotalBatteryConsumption - TotalBatteryGeneration
    InverterLosses = (TotalPV - BatteryLosses) * (1 - param['InverterEfficiency'])
    SelfConsumptionRate = SelfConsumption / TotalPV * 100             # in %
    SelfSufficiencyRate = SelfConsumption / TotalLoad * 100
    AverageDepth = TotalBatteryGeneration / (365 * param['BatteryCapacity'])
    Nfullcycles = 365 * AverageDepth
    residue = TotalPV + TotalUncoveredDemand - TotalSurplus - BatteryLosses - InverterLosses - TotalLoad



    print ('Total yearly consumption: {:.3g} kWh'.format(TotalLoad))
    print ('Total PV production: {:.3g} kWh'.format(TotalPV))
    print ('Self Consumption: {:.3g} kWh'.format(SelfConsumption))
    print ('Total energy surplus: {:.3g} kWh'.format(TotalSurplus))
    print ('Total uncovered demand: {:.3} kWh'.format(TotalUncoveredDemand))
    print ('Self consumption rate (SCR): {:.3g}%'.format(SelfConsumptionRate))
    print ('Self sufficiency rate (SSR): {:.3g}%'.format(SelfSufficiencyRate))
    print ('Amount of energy provided by the battery: {:.3} kWh'.format(TotalBatteryGeneration))
    print ('Average Charging/Discharging depth: {:.3g}'.format(AverageDepth))
    print ('Number of equivalent full cycles per year: {:.3g} '.format(Nfullcycles))
    print ('Total battery losses: {:.3g} kWh'.format(BatteryLosses))
    print ('Total inverter losses: {:.3g} kWh'.format(InverterLosses))
    print ('Residue (check): {:.3g} kWh'.format(residue))
