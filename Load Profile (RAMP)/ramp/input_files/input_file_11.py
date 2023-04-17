# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition
'''

from ramp.core.core import User, np, pd
User_list = []

"""-----------Vacation, hot season; 16.november-31.december, 46 days (vacation, high visitor activity)---------------"""

#Kitchen
K = User("kitchen",1,3)
User_list.append(K)

#Storage kitchen
Stor_K = User("Storage Kitchen",1,3)
User_list.append(Stor_K)

#Security
SEC = User("security",1,3)
User_list.append(SEC)

#Residential building 1 in Director's housing area
RB1 = User("Residential Building 1",1,3)
User_list.append(RB1)

#Residential building 2 in Director's housing area
RB2 = User("Residential Building 2",1,3)
User_list.append(RB2)

#storage in Director's housing area
Stor_Dir = User("Storage",1,3)
User_list.append(Stor_Dir)

SR = User("Staff room",1,3)
User_list.append(SR)

#Workshop
WS = User("Workshop",1,3)
User_list.append(WS)

#Computer lab
CL = User("Computer lab",1,3)
User_list.append(CL)

#Multiple purpose building
MPB = User("Multiple Purpose Building",1,3)
User_list.append(MPB)

"""-----Appliances Multiple Purpose Building----"""

#using r_t = 0.2 and r_w = 0.35
Indoor_LED_MPB = MPB.Appliance(MPB,10,9,1,10*60,0.2,5)
#time window: 12:00-21:00
Indoor_LED_MPB.windows([12*60,21*60],r_w=0.35)

#using r_t = 0.2 and r_w = 0.35
Outdoor_LED_MPB = MPB.Appliance(MPB,10,9,1,1*60,0.2,5)
#time window: 19:00-21:00
Outdoor_LED_MPB.windows([19*60,21*60],r_w=0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_MPB = MPB.Appliance(MPB,5,50,1,6*60,0.2,5)
#time window: 12:00-21:00
Fan_MPB.windows([12*60,21*60],r_w=0.35)

Phone_MPB = MPB.Appliance(MPB,5,7,1,2*60,0.2,5,occasional_use=0.5)
#time window: 12:00-21:00
Phone_MPB.windows([12*60,21*60],r_w =0.35)

#using r_t = 0.1 and r_w = 0.35
Speaker_MPB = MPB.Appliance(MPB,1,50,1,1*60,0.1,5,occasional_use=0.5)
#time window: 12:00-21:00
Speaker_MPB.windows([12*60,21*60],r_w=0.35)

"""-----------Appliances computer lab----------"""
#sporadic user behavior on all appliances
#assume only 5 laptops because there is no school

PC_CL = CL.Appliance(CL,5,60,1,3*60,0.1,5,occasional_use =  0.5)
#time window: 07:00-17:00
PC_CL.windows([7*60,17*60],r_w = 0.35)

LED_CL = CL.Appliance(CL,4,9,1,5*60,0.2,5,occasional_use =  0.5)
#time window: 07:00-17:00
LED_CL.windows([7*60,17*60],r_w=0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_CL = CL.Appliance(CL,2,50,1,5*60,0.2,5,occasional_use =  0.5)
#time window: 07:00-17:00
Fan_CL.windows([7*60,17*60],r_w=0.35)

"""-----Expanded visitor area--------"""

#five regular visitor huts (boys and girl huts)
VH1 = User("visitor hut type 1",5,3)
User_list.append(VH1)

#Lindsays house/visitor hut
VH2 = User("visitor hut type 2",1,3)
User_list.append(VH2)

#Visitor showers (2 of this building)
VS = User("visitor showers",2,3)
User_list.append(VS)

#Visitor toilets (2 of this building)
VT = User("visitor toilets",2,3)
User_list.append(VT)

#Hangout area for visitors
HA = User("Hangout area",1,3)
User_list.append(HA)

"""------Appliances kitchen------"""
#using r_t = 0.2 and r_w = 0.35
Indoor_LED_K = K.Appliance(K,8,9,2,5*60,0.2,5)
#time window 1: 06:00-07:00
#time window 2: 19:00-23:59
Indoor_LED_K.windows([6*60,7*60],[19*60,23*60+59],0.35)

#using r_t = 0.2 and r_w = 0.35
Outdoor_LED_K = K.Appliance(K,1,9,2,2*60,0.2,5)
#time window 1: 06:00-07:00
#time window 2: 19:00-23:59
Outdoor_LED_K.windows([6*60,7*60],[19*60,23*60+59],0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_K = K.Appliance(K,3,50,2,7*60,0.2,5)
#time window 1: 12:00-15:00
#time window 2: 19:00-23:59
Fan_K.windows([12*60,15*60],[19*60,23*60+59],0.35)

#using r_t = 0.2, r_w = 0.35
Phone_K = K.Appliance(K,8,7,1,2*60,0.2,5)
#time window: 07:00-23:59
Phone_K.windows([7*60,1439],r_w =0.35)

#using r_t = 0.1 and r_w = 0.35
PC_K = K.Appliance(K,8,60,1,4*60,0.1,5)
#time window: 07:00-23:59
PC_K.windows([7*60,1439],r_w = 0.35)

#setter occasional use = 0.33 pga input_file1 i RAMP gjør det for mixer
Blender_K = K.Appliance(K,1,400,1,0.5*60,0.1,5,occasional_use = 0.33)
#time window: 07:00-19:00
Blender_K.windows([7*60,19*60],r_w = 0.35)

#using r_t = 0.1 and r_w = 0.35
Speaker_K = K.Appliance(K,1,10,2,1*60,0.1,5)
#time window 1: 12:00-15:00
#time window 2: 19:00-23:59
Speaker_K.windows([12*60,15*60],[19*60,23*60+59],0.35)

#Fridge hot season

Fridge_K = K.Appliance(K,1,150,1,1440,0,30, 'yes',3)
Fridge_K.windows([0,1440],[0,0])
#intensive
#time window: 08:00-20:00
Fridge_K.specific_cycle_1(150,20,5,10)
#intermediate
#time window: 05:00-07:59
Fridge_K.specific_cycle_2(150,15,5,15)
#standard
#time window: 00:00-04:59 and 20:01-23:59
Fridge_K.specific_cycle_3(150,10,5,20)

Fridge_K.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1439])

"""-------------Appliances Storage by kitchen-------------"""

#Storage by kitchen
LED_Stor_K = Stor_K.Appliance(Stor_K,3,9,1,0.5*60,0.2,5,occasional_use = 0.2)
#time window:19:00-21:00
LED_Stor_K.windows([19*60,21*60],r_w=0.35)

"""-----------Appliances Security----------"""

#using r_t = 0.2 and r_w = 0.35
Indoor_LED_SEC = SEC.Appliance(SEC,1,9,2,6*60,0.2,5)
#time window: 19:00-07:00
Indoor_LED_SEC.windows([19*60,23*60+59],[0,7*60],0.35)

#using r_t = 0.2 and r_w = 0.35
Outdoor_LED_SEC = SEC.Appliance(SEC,1,9,2,4*60,0.2,5)
#time window: 19:00-07:00
Outdoor_LED_SEC.windows([19*60,23*60+59],[0,7*60],0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_SEC = SEC.Appliance(SEC,1,50,2,9*60,0.2,5)
#time window: 19:00-07:00
Fan_SEC.windows([19*60,23*60+59],[0,7*60],0.35)

#using r_t = 0.2, r_w = 0.35
Phone_SEC = SEC.Appliance(SEC,1,7,2,2*60,0.2,5)
#time window: 19:00-07:00
Phone_SEC.windows([19*60,23*60+59],[0,7*60],0.35)

"""-------Appliances RB1 in Director's housing area---------"""

#using r_t = 0.2 and r_w = 0.35
Indoor_LED_RB1 = RB1.Appliance(RB1,3,9,2,7*60,0.2,5)
#time window 1: 06:00-07:00
#time window 2: 17:00-23:59
Indoor_LED_RB1.windows([6*60,7*60],[17*60,23*60+59],0.35)

#using r_t = 0.2 and r_w = 0.35
Outdoor_LED_RB1 = RB1.Appliance(RB1,1,9,2,1*60,0.2,5)
#time window 2: 19:00-07:00
Outdoor_LED_RB1.windows([19*60,23*60+59],[0,7*60],0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_RB1 = RB1.Appliance(RB1,1,50,2,10*60,0.2,5)
#time window: 17:00-07:00
Fan_RB1.windows([17*60,23*60+59],[0,7*60],0.35)

#using r_t = 0.2, r_w = 0.35
Phone_RB1 = RB1.Appliance(RB1,1,7,1,2*60,0.2,5)
#time window: 17:00-23:59
Phone_RB1.windows([17*60,23*60+59],r_w=0.35)

#using r_t = 0.1 and r_w = 0.35
PC_RB1 = RB1.Appliance(RB1,1,60,1,4*60,0.1,5)
#time window: 17:00-23:59
PC_RB1.windows([17*60,23*60+59],r_w=0.35)

#Fridge hot season

Fridge_RB1 = RB1.Appliance(RB1,1,150,1,1440,0,30, 'yes',3)
Fridge_RB1.windows([0,1440],[0,0])
#intensive
#time window: 08:00-20:00
Fridge_RB1.specific_cycle_1(150,20,5,10)
#intermediate
#time window: 05:00-07:59
Fridge_RB1.specific_cycle_2(150,15,5,15)
#standard
#time window: 00:00-04:59 and 20:01-23:59
Fridge_RB1.specific_cycle_3(150,10,5,20)

Fridge_RB1.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1439])


"""-------Appliances RB2 Director's housing area----------"""

#using r_t = 0.2 and r_w = 0.35
Indoor_LED_RB2 = RB2.Appliance(RB2,6,9,2,5*60,0.2,5)
#time window 1: 06:00-07:00
#time window 2: 19:00-23:59
Indoor_LED_RB2.windows([6*60,7*60],[19*60,23*60+59],0.35)

#using r_t = 0.2 and r_w = 0.35
Outdoor_LED_RB2 = RB2.Appliance(RB2,3,9,2,1*60,0.2,5)
#time window 1: 19:00-07:00
Outdoor_LED_RB2.windows([19*60,23*60+59],[0,7*60],0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_RB2 = RB2.Appliance(RB2,2,50,2,9*60,0.2,5)
#time window: 21:00-07:00
Fan_RB2.windows([21*60,23*60+59],[0,7*60],0.35)

#using r_t = 0.1 and r_w = 0.35
PC_RB2 = RB2.Appliance(RB2,1,60,1,2*60,0.1,5)
#time window: 13:00-21:00
PC_RB2.windows([13*60,21*60],r_w=0.35)

#using r_t = 0.2, r_w = 0.35
Phone_RB2 = RB2.Appliance(RB2,4,7,1,2*60,0.2,5)
#time window: 07:00-23:59
Phone_RB2.windows([7*60,23*60+59],r_w=0.35)

#Fridge hot season

Fridge_RB2 = RB2.Appliance(RB2,1,150,1,1440,0,30, 'yes',3)
Fridge_RB2.windows([0,1440],[0,0])
#intensive
#time window: 08:00-20:00
Fridge_RB2.specific_cycle_1(150,20,5,10)
#intermediate
#time window: 05:00-07:59
Fridge_RB2.specific_cycle_2(150,15,5,15)
#standard
#time window: 00:00-04:59 and 20:01-23:59
Fridge_RB2.specific_cycle_3(150,10,5,20)

Fridge_RB2.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1439])

"""--------------Appliances storage by director's housing area"""

LED_Stor_Dir = Stor_Dir.Appliance(Stor_Dir,2,9,1,0.5*60,0.2,5,occasional_use = 0.2)
#time window:07:00-21:00
LED_Stor_Dir.windows([7*60,21*60],r_w=0.35)

"""----------Expanded visitor area------------------"""

"""--------------Appliances Visitor hut type 1-----------"""

#using r_t = 0.2, r_w = 0.35
Phone_VH1 = VH1.Appliance(VH1,6,7,1,2*60,0.2,5)
#time window: 07:00-23:59
Phone_VH1.windows([7*60,1439],r_w =0.35)

#using r_t = 0.1 and r_w = 0.35
PC_VH1 = VH1.Appliance(VH1,3,60,1,4*60,0.1,5)
#time window: 07:00-23:59
PC_VH1.windows([7*60,23*60+59],r_w = 0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_VH1 = VH1.Appliance(VH1,2,50,3,9*60,0.2,5)
#time window 1: 12:00-14:00
#time window 2: 21:00-07:00
Fan_VH1.windows([12*60,14*60],[21*60,23*60+59],0.35,[0,7*60])

#using r_t = 0.2 and r_w = 0.35
Indoor_LED_VH1 = VH1.Appliance(VH1,2,9,2,2*60,0.2,5)
#time window 1: 06:00-07:00
#time window 2: 19:00-23:59
Indoor_LED_VH1.windows([6*60,7*60],[19*60,23*60+59],0.35)

#using r_t = 0.2 and r_w = 0.35
Outdoor_LED_VH1 = VH1.Appliance(VH1,3,9,2,1*60,0.2,5)
#time window: 19:00-07:00
Outdoor_LED_VH1.windows([19*60,23*60+59],[0,7*60],0.35)

#using r_t = 0.1 and r_w = 0.35
Speaker_VH1 = VH1.Appliance(VH1,1,10,1,1*60,0.1,5,occasional_use=0.5)
#time window: 07:00-23:59
Speaker_VH1.windows([7*60,23*60+59],r_w =0.35)

#Fridge hot season

Fridge_VH1 = VH1.Appliance(VH1,1,150,1,1440,0,30, 'yes',3)
Fridge_VH1.windows([0,1440],[0,0])
#intensive
#time window: 08:00-20:00
Fridge_VH1.specific_cycle_1(150,20,5,10)
#intermediate
#time window: 05:00-07:59
Fridge_VH1.specific_cycle_2(150,15,5,15)
#standard
#time window: 00:00-04:59 and 20:01-23:59
Fridge_VH1.specific_cycle_3(150,10,5,20)

Fridge_VH1.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1439])

"""--------------Appliances Visitor hut type 2----------"""

#using r_t = 0.2, r_w = 0.35
Phone_VH2 = VH2.Appliance(VH2,3,7,1,2*60,0.2,5)
#time window: 07:00-23:59
Phone_VH2.windows([7*60,1439],r_w =0.35)

#using r_t = 0.1 and r_w = 0.35
PC_VH2 = VH2.Appliance(VH2,2,60,1,4*60,0.1,5)
#time window: 07:00-23:59
PC_VH2.windows([7*60,23*60+59],r_w = 0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_VH2 = VH2.Appliance(VH2,1,50,3,9*60,0.2,5)
#time window 1: 12:00-14:00
#time window 2: 21:00-07:00
Fan_VH2.windows([12*60,14*60],[21*60,23*60+59],0.35,[0,7*60])

#using r_t = 0.2 and r_w = 0.35
Indoor_LED_VH2 = VH2.Appliance(VH2,6,9,2,2*60,0.2,5)
#time window 1: 06:00-07:00
#time window 2: 19:00-23:59
Indoor_LED_VH2.windows([6*60,7*60],[19*60,23*60+59],0.35)

#using r_t = 0.2 and r_w = 0.35
Outdoor_LED_VH2 = VH2.Appliance(VH2,1,9,2,1*60,0.2,5)
#time window: 19:00-07:00
Outdoor_LED_VH2.windows([19*60,23*60+59],[0,7*60],0.35)

#using r_t = 0.1 and r_w = 0.35
Speaker_VH2 = VH2.Appliance(VH2,1,10,1,1*60,0.1,5,occasional_use=0.5)
#time window: 07:00-23:59
Speaker_VH2.windows([7*60,23*60+59],r_w =0.35)

#Fridge hot season

Fridge_VH2 = VH2.Appliance(VH2,1,150,1,1440,0,30, 'yes',3)
Fridge_VH2.windows([0,1440],[0,0])
#intensive
#time window: 08:00-20:00
Fridge_VH2.specific_cycle_1(150,20,5,10)
#intermediate
#time window: 05:00-07:59
Fridge_VH2.specific_cycle_2(150,15,5,15)
#standard
#time window: 00:00-04:59 and 20:01-23:59
Fridge_VH2.specific_cycle_3(150,10,5,20)

Fridge_VH2.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1439])

"""-----------Appliances visitor showers and visitor toilets----------"""

"""showers"""
#using r_t = 0.2 and r_w = 0.35
Indoor_LED_VS = VS.Appliance(VS,5,9,2,1*60,0.2,5)
#time window 1: 06:00-07:00
#time window 2: 19:00-23:59
Indoor_LED_VS.windows([6*60,7*60],[19*60,23*60+59],0.35)

"""toilets"""
#using r_t = 0.2 and r_w = 0.35
Indoor_LED_VT = VT.Appliance(VT,2,9,2,1*60,0.2,5)
#time window : 19:00-07:00
Indoor_LED_VT.windows([19*60,23*60+59],[0,7*60],0.35)

#using r_t = 0.2 and r_w = 0.35
Outdoor_LED_VT = VT.Appliance(VT,1,9,2,1*60,0.2,5)
#time window : 19:00-07:00
Outdoor_LED_VT.windows([19*60,23*60+59],[0,7*60],0.35)

"""------------Appliances visitor hangout area-------------"""
#using r_t = 0.2 and r_w = 0.35
Indoor_LED_HA = HA.Appliance(HA,4,9,2,4*60,0.2,5)
#time window 1: 06:00-07:00
#time window 2: 19:00-23:59
Indoor_LED_HA.windows([6*60,7*60],[19*60,23*60+59],0.35)

#using r_t = 0.2 and r_w = 0.35
Outdoor_LED_HA = HA.Appliance(HA,1,9,2,2*60,0.2,5)
#time window 1: 06:00-07:00
#time window 2: 19:00-23:59
Outdoor_LED_HA.windows([6*60,7*60],[19*60,23*60+59],0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_HA = HA.Appliance(HA,2,50,2,7*60,0.2,5,occasional_use = 0.5)
#time window 1: 12:00-15:00
#time window 2: 19:00-23:59
Fan_HA.windows([12*60,15*60],[19*60,23*60+59],0.35)

#using r_t = 0.2, r_w = 0.35
Phone_HA = HA.Appliance(HA,6,7,1,2*60,0.2,5,occasional_use = 0.5)
#time window: 07:00-23:59
Phone_HA.windows([7*60,1439],r_w =0.35)

#using r_t = 0.1 and r_w = 0.35
PC_HA = HA.Appliance(HA,10,60,1,2*60,0.1,5,occasional_use = 0.5)
#time window: 07:00-23:59
PC_HA.windows([7*60,1439],r_w = 0.35)

#using r_t = 0.1 and r_w = 0.35
Speaker_HA = HA.Appliance(HA,1,10,2,1*60,0.1,5,occasional_use = 0.5)
#time window 1: 12:00-15:00
#time window 2: 19:00-23:59
Speaker_HA.windows([12*60,15*60],[19*60,23*60+59],0.35)

#Fridge hot season

Fridge_HA = HA.Appliance(HA,1,150,1,1440,0,30, 'yes',3)
Fridge_HA.windows([0,1440],[0,0])
#intensive
#time window: 08:00-20:00
Fridge_HA.specific_cycle_1(150,20,5,10)
#intermediate
#time window: 05:00-07:59
Fridge_HA.specific_cycle_2(150,15,5,15)
#standard
#time window: 00:00-04:59 and 20:01-23:59
Fridge_HA.specific_cycle_3(150,10,5,20)

Fridge_HA.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1439])

"""-------Appliances Staff Room-------------"""

"""--------All week--------"""
Fan_SR = SR.Appliance(SR,2,50,1,10*60,0.2,5)
#time window 1: 12:00-23:59
Fan_SR.windows([12*60,23*60+59],r_w=0.35)

Small_Speaker_SR = SR.Appliance(SR,1,10,1,1*60,0.1,5,occasional_use=0.5)
#time window: 07:00-21:00
Small_Speaker_SR.windows([7*60,21*60],r_w = 0.35)

Medium_Speaker_SR = SR.Appliance(SR,1,50,1,1*60,0.1,5,occasional_use=0.5)
#time window:07:00-21:00
Medium_Speaker_SR.windows([7*60,21*60],r_w = 0.35)

Indoor_LED_SR = SR.Appliance(SR,2,9,2,5*60,0.2,5)
#time window: 06:00-07:00
#time window 2: 19:00-23:59
Indoor_LED_SR.windows([6*60,7*60],[19*60,23*60+59],0.35)

Outdoor_LED_SR = SR.Appliance(SR,2,9,2,2*60,0.2,5)
#time window: 06:00-07:00
#time window: 19:00-23:59
Outdoor_LED_SR.windows([6*60,7*60],[19*60,23*60+59],0.35)

#Fridge hot season

Fridge_SR = SR.Appliance(SR,1,150,1,1440,0,30, 'yes',3)
Fridge_SR.windows([0,1440],[0,0])
#intensive
#time window: 08:00-20:00
Fridge_SR.specific_cycle_1(150,20,5,10)
#intermediate
#time window: 05:00-07:59
Fridge_SR.specific_cycle_2(150,15,5,15)
#standard
#time window: 00:00-04:59 and 20:01-23:59
Fridge_SR.specific_cycle_3(150,10,5,20)

Fridge_SR.cycle_behaviour([480,1200],[0,0],[300,479],[0,0],[0,299],[1201,1439])

Projector_SR = SR.Appliance(SR,1,220,1,1*60,0.2,5,occasional_use =  0.5)
#time window: 07:00-19:00
Projector_SR.windows([7*60,19*60],r_w = 0.35)

Phone_SR = SR.Appliance(SR,2,8,1,2*60,0.2,5)
#time window: 10:00-19:00
Phone_SR.windows([10*60,19*60],r_w =0.35)

PC_SR = SR.Appliance(SR,2,60,1,2*60,0.1,5)
#time window: 10:00-19:00
PC_SR.windows([10*60,19*60],r_w = 0.35)

TV_SR = SR.Appliance(SR,1,60,1,6*60,0.1,5)
#time window: 10:00-23:59
TV_SR.windows([10*60,23*60+59],r_w = 0.35)

Decoder_SR = SR.Appliance(SR,1,7,1,6*60,0.1,5)
#time window: 10:00-23:59
Decoder_SR.windows([10*60,23*60+59],r_w=0.35)

Printer_SR = SR.Appliance(SR,1,150,1,0.5*60,0.1,5,occasional_use = 0.2)
#time window: 07:00-19:00
Printer_SR.windows([7*60,19*60],r_w = 0.35)

"""---------Appliances workshop---------"""
#using r_t = 0.2 and r_w = 0.35
Indoor_LED_WS = WS.Appliance(WS,8,9,1,4*60,0.2,5,occasional_use = 0.5,wd_we_type = 1)
#time window: 12:00-19:00
Indoor_LED_WS.windows([12*60,19*60],r_w=0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_WS = WS.Appliance(WS,4,50,2,4*60,0.2,5,occasional_use = 0.2)
#time window: 12:00-19:00
Fan_WS.windows([12*60,19*60],r_w=0.35)

Tablet_WS = WS.Appliance(WS,4,15,1,2*60,0.1,5,occasional_use = 0.2)
#[12:00-19:00]
Tablet_WS.windows([12*60,19*60],r_w = 0.35)

Drill_WS = WS.Appliance(WS,1,100,1,0.5*60,0.1,5,occasional_use = 0.1)
#[12:00-19:00]
Drill_WS.windows([12*60,19*60],r_w = 0.35)

Saw_WS = WS.Appliance(WS,1,2400,1,0.5*60,0.1,5,fixed_cycle = 1,occasional_use = 0.1)
#time window: [12:00-19:00]
Saw_WS.windows([12*60,19*60],r_w = 0.35)
Saw_WS.specific_cycle_1(2400,5,720,25,0.1)

Saw_WS.cycle_behaviour([12*60,19*60])

Angle_grinder_WS = WS.Appliance(WS,1,1050,1,0.5*60,0.1,5,occasional_use = 0.1)
#time window: 12:00-19:00
Angle_grinder_WS.windows([12*60,19*60],r_w = 0.35)
