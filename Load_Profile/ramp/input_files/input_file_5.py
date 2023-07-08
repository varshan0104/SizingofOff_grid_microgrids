# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition 
'''

from ramp.core.core import User, np, pd
User_list = []


"""------------Hot season; 1.-7.February, 7 days (mid-term vacation, high visitor activity)--------------"""

#Computer lab
MPB = User("Computer lab",1,3)
User_list.append(MPB)


"""--Appliances Multiple Purpose Building--"""

#using r_t = 0.2 and r_w = 0.35
Indoor_LED_MPB = MPB.Appliance(MPB,10,9,1,10*60,0.2,5)
#time window: 12:00-21:00
Indoor_LED_MPB.windows([12*60,18*60],r_w=0.35)

