"""
Part of masterthesis; Optimal sizing of offgrid microgrids.
@author: Varshan Erik Shankar

GridVille NTNU
"""

#All relevant packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#imports all functions from importproductdata.py
from importproductdata import *

ProductData = read_input_data('productdata.xlsx')

print("Dette er fra main:")
print(ProductData)
print(ProductData[1])
print(ProductData[1][1])
print(ProductData[1][1][2])

from analysis import *

