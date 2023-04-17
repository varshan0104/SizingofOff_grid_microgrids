# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition
'''

from ramp.core.core import User, np, pd
User_list = []

"""------------Warm season; 24.september - 31.october, 37 days (regular school, high visitor activity)-------------"""

#Computer lab
CL = User("Computer lab",1,3)
User_list.append(CL)

#Classroom type 1 = Class 1 and 2
Class_T1 = User("Classroom type 1",2,3)
User_list.append(Class_T1)

#PP1 and PP2
PP = User("PP",2,3)
User_list.append(PP)

#Classroom toilets
CT = User("Classroom Toilets",1,3)
User_list.append(CT)

#Staff court
SC = User("Staff Court",1,3)
User_list.append(SC)

#Kitchen
K = User("kitchen",1,3)
User_list.append(K)

#Storage kitchen
Stor_K = User("Storage Kitchen",1,3)
User_list.append(Stor_K)

#student dorms (Boys and Girls)
SD = User("Student dorms",2,3)
User_list.append(SD)

#Student showers (Boys and Girls)
SS = User("Student showers",2,3)
User_list.append(SS)

#Student toilets (Boys and Girls)
ST = User("Student toilets",4,3)
User_list.append(ST)

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

#Director's office
Office = User("Director's office",1,3)
User_list.append(Office)

#Leap Learning lab
LL = User("Leap Learning",1,3)
User_list.append(LL)

#Staff room
SR = User("Staff room",1,3)
User_list.append(SR)

#Classroom type 2 = Class 3,4 and 5
Class_T2 = User("Classroom type 2",3,3)
User_list.append(Class_T2)

#Classroom type 3 = Class 6
Class_6 = User("Class 6",1,3)
User_list.append(Class_6)

#Workshop
WS = User("Workshop",1,3)
User_list.append(WS)

#Multiple purpose building
MPB = User("Multiple Purpose Building",1,3)
User_list.append(MPB)

"""----Appliances Multiple Purpise Building----"""

"""weekdays"""
#using r_t = 0.2 and r_w = 0.35
Indoor_LED_MPB = MPB.Appliance(MPB,10,9,1,10*60,0.2,5,wd_we_type = 0)
#time window: 07:00-19:00
Indoor_LED_MPB.windows([7*60,19*60],r_w=0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_MPB = MPB.Appliance(MPB,5,50,1,8*60,0.2,5,wd_we_type = 0)
#time window: 07:00-19:00
Fan_MPB.windows([7*60,19*60],r_w=0.35)

Phone_MPB = MPB.Appliance(MPB,5,7,1,2*60,0.2,5,wd_we_type = 0,occasional_use=0.5)
#time window: 07:00-19:00
Phone_MPB.windows([7*60,19*60],r_w =0.35)

#using r_t = 0.1 and r_w = 0.35
Speaker_MPB = MPB.Appliance(MPB,1,50,1,1*60,0.1,5,wd_we_type = 0,occasional_use=0.5)
#time window: 15:00-19:00
Speaker_MPB.windows([15*60,19*60],r_w=0.35)

"""weekends"""
#using r_t = 0.2 and r_w = 0.35
Indoor_LED_MPB_we = MPB.Appliance(MPB,10,9,1,10*60,0.2,5,wd_we_type = 1)
#time window: 12:00-21:00
Indoor_LED_MPB_we.windows([12*60,21*60],r_w=0.35)

#using r_t = 0.2 and r_w = 0.35
Outdoor_LED_MPB_we = MPB.Appliance(MPB,10,9,1,1*60,0.2,5,wd_we_type = 1)
#time window: 19:00-21:00
Outdoor_LED_MPB_we.windows([19*60,21*60],r_w=0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_MPB_we = MPB.Appliance(MPB,5,50,1,6*60,0.2,5,wd_we_type = 1)
#time window: 12:00-21:00
Fan_MPB_we.windows([12*60,21*60],r_w=0.35)

Phone_MPB_we = MPB.Appliance(MPB,5,7,1,2*60,0.2,5,wd_we_type = 1,occasional_use=0.5)
#time window: 12:00-21:00
Phone_MPB_we.windows([12*60,21*60],r_w =0.35)

#using r_t = 0.1 and r_w = 0.35
Speaker_MPB_we = MPB.Appliance(MPB,1,50,1,1*60,0.1,5,wd_we_type = 1,occasional_use=0.5)
#time window: 12:00-21:00
Speaker_MPB_we.windows([12*60,21*60],r_w=0.35)

"""----------Appliances Kitchen-----------------"""
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

#Using the warm season, using the same cycles as presented in the article:
#Standard cycle: w1: [00:00-04:59] w2: [18:01-23:59]-->cycle 3
#intermediate cycle: w1: [05:00-09:39] --> cycle 2
#intensive cycle: w2: [09:40 - 18:00] --> cycle 1

Fridge_K = K.Appliance(K,1,150,1,1440,0,30, 'yes',3)
Fridge_K.windows([0,1440],[0,0])
#intensive
Fridge_K.specific_cycle_1(150,20,5,10)
#intermediate
Fridge_K.specific_cycle_2(150,15,5,15)
#standard
Fridge_K.specific_cycle_3(150,10,5,20)

Fridge_K.cycle_behaviour([580,1080],[0,0],[300,579],[0,0],[0,299],[1081,1439])


"""-------------Appliances Storage by kitchen-------------"""

#Storage by kitchen
LED_Stor_K = Stor_K.Appliance(Stor_K,3,9,1,0.5*60,0.2,5,occasional_use = 0.2)
#time window:19:00-21:00
LED_Stor_K.windows([19*60,21*60],r_w=0.35)

"""-------------Appliances Student dorms---------------"""
Outdoor_LED_SD = SD.Appliance(SD,2,9,2,1*60,0.2,5)
#time window: 19:00-07:00
Outdoor_LED_SD.windows([19*60,23*60+59],[0,7*60],0.35)

""""----weekdays------"""

Indoor_LED_SD = SD.Appliance(SD,3,9,1,2*60,0.2,5,wd_we_type = 0)
#time window: 19:00-21:00
Indoor_LED_SD.windows([19*60,21*60],r_w=0.35)

Fan_SD = SD.Appliance(SD,2,50,2,9*60,0.2,5,wd_we_type = 0)
#time window 2: 21:00-06:00
Fan_SD.windows([21*60,23*60+59],[0,6*60],0.35)

"""----weekends-----"""
#students go to bed an hour later
#students sleep 1 hour longer

Indoor_LED_SD_we = SD.Appliance(SD,3,9,1,2*60,0.2,5,wd_we_type = 1)
#time window: 19:00-22:00
Indoor_LED_SD_we.windows([19*60,22*60],r_w=0.35)

Fan_SD_we = SD.Appliance(SD,2,50,3,9*60,0.2,5,wd_we_type = 1)

#time window 1: 12-00-14:00
#time window 2: 22:00-07:00

Fan_SD_we.windows([12*60,14*60],[22*60,23*60+59],0.35,[0,7*60])

"""---------Appliances Student showers-------------"""

"""_-------weekdays--------"""

Indoor_LED_SS = SS.Appliance(SS,2,9,1,2*60,0.2,5,wd_we_type = 0)
#time window: 15:00-21:00
Indoor_LED_SS.windows([15*60,21*60],r_w=0.35)

Outdoor_LED_SS = SS.Appliance(SS,2,9,1,1*60,0.2,5,wd_we_type = 0)
#time window: 15:00-21:00
Outdoor_LED_SS.windows([15*60,21*60],r_w=0.35)

"""------------weekends-----------"""
Indoor_LED_SS = SS.Appliance(SS,2,9,1,2*60,0.2,5,wd_we_type = 1)
#time window: 12:00-21:00
Indoor_LED_SS.windows([12*60,21*60],r_w=0.35)

Outdoor_LED_SS = SS.Appliance(SS,2,9,1,1*60,0.2,5,wd_we_type = 1)
#time window: 12:00-21:00
Outdoor_LED_SS.windows([12*60,21*60],r_w=0.35)

"""---------Appliances Student toilets---------------"""

Indoor_LED_ST = ST.Appliance(ST,2,9,2,2*60,0.2,5)
#time window 2: 19:00-07:00
Indoor_LED_ST.windows([19*60,23*60+59],[0,7*60],0.35)

Outdoor_LED_ST = ST.Appliance(ST,2,9,2,1*60,0.2,5)
#time window 2: 19:00-07:00
Outdoor_LED_ST.windows([19*60,23*60+59],[0,7*60],0.35)

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

"""-----------Appliances RB1 Director's housing area-----------------"""

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

#Using the warm season, using the same cycles as presented in the article:
#Standard cycle: w1: [00:00-04:59] w2: [18:01-23:59]-->cycle 3
#intermediate cycle: w1: [05:00-09:39] --> cycle 2
#intensive cycle: w2: [09:40 - 18:00] --> cycle 1

Fridge_RB1 = RB1.Appliance(RB1,1,150,1,1440,0,30, 'yes',3)
Fridge_RB1.windows([0,1440],[0,0])
#intensive
Fridge_RB1.specific_cycle_1(150,20,5,10)
#intermediate
Fridge_RB1.specific_cycle_2(150,15,5,15)
#standard
Fridge_RB1.specific_cycle_3(150,10,5,20)

Fridge_RB1.cycle_behaviour([580,1080],[0,0],[300,579],[0,0],[0,299],[1081,1439])

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
PC_RB2 = RB2.Appliance(RB2,1,60,1,2*60,0.1,5,occasional_use = 0.5)
#time window: 13:00-21:00
PC_RB2.windows([13*60,21*60],r_w=0.35)

#using r_t = 0.2, r_w = 0.35
Phone_RB2 = RB2.Appliance(RB2,1,7,1,2*60,0.2,5)
#time window: 07:00-23:59
Phone_RB2.windows([7*60,23*60+59],r_w=0.35)

#Using the warm season, using the same cycles as presented in the article:
#Standard cycle: w1: [00:00-04:59] w2: [18:01-23:59]-->cycle 3
#intermediate cycle: w1: [05:00-09:39] --> cycle 2
#intensive cycle: w2: [09:40 - 18:00] --> cycle 1

Fridge_RB2 = RB2.Appliance(RB2,1,150,1,1440,0,30, 'yes',3)
Fridge_RB2.windows([0,1440],[0,0])
#intensive
Fridge_RB2.specific_cycle_1(150,20,5,10)
#intermediate
Fridge_RB2.specific_cycle_2(150,15,5,15)
#standard
Fridge_RB2.specific_cycle_3(150,10,5,20)

Fridge_RB2.cycle_behaviour([580,1080],[0,0],[300,579],[0,0],[0,299],[1081,1439])

"""--------------Appliances storage by director's house"""

LED_Stor_Dir = Stor_Dir.Appliance(Stor_Dir,2,9,1,0.5*60,0.2,5,occasional_use = 0.2)
#time window:07:00-21:00
LED_Stor_Dir.windows([7*60,21*60],r_w=0.35)

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

#Using the warm season, using the same cycles as presented in the article:
#Standard cycle: w1: [00:00-04:59] w2: [18:01-23:59]-->cycle 3
#intermediate cycle: w1: [05:00-09:39] --> cycle 2
#intensive cycle: w2: [09:40 - 18:00] --> cycle 1

Fridge_VH1 = VH1.Appliance(VH1,1,150,1,1440,0,30, 'yes',3)
Fridge_VH1.windows([0,1440],[0,0])
#intensive
Fridge_VH1.specific_cycle_1(150,20,5,10)
#intermediate
Fridge_VH1.specific_cycle_2(150,15,5,15)
#standard
Fridge_VH1.specific_cycle_3(150,10,5,20)

Fridge_VH1.cycle_behaviour([580,1080],[0,0],[300,579],[0,0],[0,299],[1081,1439])

"""------------Appliances Visitor hut type 2------------------"""

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


#Using the warm season, using the same cycles as presented in the article:
#Standard cycle: w1: [00:00-04:59] w2: [18:01-23:59]-->cycle 3
#intermediate cycle: w1: [05:00-09:39] --> cycle 2
#intensive cycle: w2: [09:40 - 18:00] --> cycle 1

Fridge_VH2 = VH2.Appliance(VH2,1,150,1,1440,0,30, 'yes',3)
Fridge_VH2.windows([0,1440],[0,0])
#intensive
Fridge_VH2.specific_cycle_1(150,20,5,10)
#intermediate
Fridge_VH2.specific_cycle_2(150,15,5,15)
#standard
Fridge_VH2.specific_cycle_3(150,10,5,20)

Fridge_VH2.cycle_behaviour([580,1080],[0,0],[300,579],[0,0],[0,299],[1081,1439])

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

"""-----Appliances hangout area--------------"""

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

#Using the warm season, using the same cycles as presented in the article:
#Standard cycle: w1: [00:00-04:59] w2: [18:01-23:59]-->cycle 3
#intermediate cycle: w1: [05:00-09:39] --> cycle 2
#intensive cycle: w2: [09:40 - 18:00] --> cycle 1

Fridge_HA = HA.Appliance(HA,1,150,1,1440,0,30, 'yes',3)
Fridge_HA.windows([0,1440],[0,0])
#intensive
Fridge_HA.specific_cycle_1(150,20,5,10)
#intermediate
Fridge_HA.specific_cycle_2(150,15,5,15)
#standard
Fridge_HA.specific_cycle_3(150,10,5,20)

Fridge_HA.cycle_behaviour([580,1080],[0,0],[300,579],[0,0],[0,299],[1081,1439])


"""-----------Appliances Director's office----------------------------------"""

#using r_t = 0.2, r_w = 0.35
Phone_Office = Office.Appliance(Office,1,7,1,2*60,0.2,5)
#time window: 07:00-17:00
Phone_Office.windows([7*60,17*60],r_w =0.35)

#using r_t = 0.1 and r_w = 0.35
PC_Office = Office.Appliance(Office,1,60,1,5*60,0.1,5)
#time window: 07:00-17:00
PC_Office.windows([7*60,17*60],r_w = 0.35)

#using r_t = 0.2 and r_w = 0.35
Indoor_LED_Office = Office.Appliance(Office,2,9,1,8*60,0.2,5)
#time window: 07:00-17:00
Indoor_LED_Office.windows([7*60,17*60],r_w = 0.35)

#using r_t = 0.2 and r_w = 0.35
Outdoor_LED_Office = Office.Appliance(Office,2,9,1,1*60,0.2,5)
#time window: 19:00-22:00
Outdoor_LED_Office.windows([19*60,22*60],r_w = 0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_Office = Office.Appliance(Office,1,50,1,7*60,0.2,5)
#time window: 07:00-17:00
Fan_Office.windows([12*60,17*60],r_w=0.35)

"""----------------Appliances Leap Learning Lab------------------"""

Tablet_LL = LL.Appliance(LL,10,15,1,2*60,0.1,5,occasional_use = 0.8,wd_we_type = 0,fixed = 'yes')
#[10:00-16:00]
Tablet_LL.windows([10*60,16*60],r_w = 0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_LL = LL.Appliance(LL,2,50,1,5*60,0.2,5)
#time window 1: 07:00-15:00
Fan_LL.windows([7*60,15*60],r_w=0.35)


"""--------------Appliances Staff Room-----------------"""

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



#Using the warm season, using the same cycles as presented in the article:
#Standard cycle: w1: [00:00-04:59] w2: [18:01-23:59]-->cycle 3
#intermediate cycle: w1: [05:00-09:39] --> cycle 2
#intensive cycle: w2: [09:40 - 18:00] --> cycle 1

Fridge_SR = SR.Appliance(SR,1,150,1,1440,0,30, 'yes',3)
Fridge_SR.windows([0,1440],[0,0])
#intensive
Fridge_SR.specific_cycle_1(150,20,5,10)
#intermediate
Fridge_SR.specific_cycle_2(150,15,5,15)
#standard
Fridge_SR.specific_cycle_3(150,10,5,20)

Fridge_SR.cycle_behaviour([580,1080],[0,0],[300,579],[0,0],[0,299],[1081,1439])

Projector_SR = SR.Appliance(SR,1,220,1,1*60,0.2,5,occasional_use =  0.5)
#time window: 07:00-19:00
Projector_SR.windows([7*60,19*60],r_w = 0.35)

"""---------Weekdays----------"""
Phone_SR = SR.Appliance(SR,6,8,1,2*60,0.2,5,wd_we_type = 0)
#time window: 07:00-19:00
Phone_SR.windows([7*60,19*60],r_w =0.35)

PC_SR = SR.Appliance(SR,8,60,1,2*60,0.1,5,wd_we_type = 0)
#time window: 07:00-19:00
PC_SR.windows([7*60,19*60],r_w = 0.35)

TV_SR = SR.Appliance(SR,1,60,1,6*60,0.1,5,wd_we_type = 0)
#time window: 16:00-23:59
TV_SR.windows([16*60,23*60+59],r_w = 0.35)

Decoder_SR = SR.Appliance(SR,1,7,1,6*60,0.1,5,wd_we_type=0)
#time window: 16:00-23:59
Decoder_SR.windows([16*60,23*60+59],r_w=0.35)

Printer_SR = SR.Appliance(SR,1,150,1,0.5*60,0.1,5,occasional_use = 0.5,wd_we_type = 0)
#time window: 07:00-19:00
Printer_SR.windows([7*60,19*60],r_w = 0.35)

"""-----------Weekends-------------"""

TV_SR_we = SR.Appliance(SR,1,60,1,6*60,0.1,5,wd_we_type = 1)
#time window: 10:00-23:59
TV_SR_we.windows([10*60,23*60+59],r_w = 0.35)

Decoder_SR_we = SR.Appliance(SR,1,7,1,8*60,0.1,5,wd_we_type=1)
#time window: 10:00-23:59
Decoder_SR_we.windows([10*60,23*60+59],r_w=0.35)

Phone_SR_we = SR.Appliance(SR,4,7,1,2*60,0.2,5,wd_we_type = 1)
#time window: 07:00-19:00
Phone_SR_we.windows([7*60,19*60],r_w =0.35)

PC_SR_we = SR.Appliance(SR,4,60,1,2*60,0.1,5,wd_we_type = 1)
#time window: 07:00-19:00
PC_SR_we.windows([7*60,19*60],r_w = 0.35)

"""----------Appliances classrooms---------------"""

"""Classroom type 2 (Class 3,4,5):"""
LED_Class_T2 = Class_T2.Appliance(Class_T2,2,9,1,5*60,0.2,5,wd_we_type = 0)
#time window: 07:00-15:00
LED_Class_T2.windows([7*60,15*60],r_w=0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_Class_T2 = Class_T2.Appliance(Class_T2,1,50,1,5*60,0.2,5,wd_we_type = 0)
#time window: 07:00-15:00
Fan_Class_T2.windows([7*60,15*60],r_w=0.35)

"""Class 6"""
#using r_t = 0.2 and r_w = 0.35
Fan_Class_6 = Class_6.Appliance(Class_6,1,50,1,5*60,0.2,5,wd_we_type = 0)
#time window: 07:00-15:00
Fan_Class_6.windows([7*60,15*60],r_w=0.35)

"""----------Appliances workshop---------"""

#using r_t = 0.2 and r_w = 0.35
Indoor_LED_WS = WS.Appliance(WS,8,9,1,8*60,0.2,5,wd_we_type = 0)
#time window: 07:00-19:00
Indoor_LED_WS.windows([7*60,19*60],r_w=0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_WS_we = WS.Appliance(WS,4,50,1,8*60,0.2,5,wd_we_type = 0)
#time window: 07:00-19:00
Fan_WS_we.windows([7*60,19*60],r_w=0.35)

Tablet_WS = WS.Appliance(WS,10,15,1,2*60,0.1,5,occasional_use = 0.5,wd_we_type = 0)
#[07:00-19:00]
Tablet_WS.windows([7*60,19*60],r_w = 0.35)

Drill_WS = WS.Appliance(WS,1,100,1,0.5*60,0.1,5,occasional_use = 0.1,wd_we_type = 0)
#[15:00-19:00]
Drill_WS.windows([15*60,19*60],r_w = 0.35)

Saw_WS = WS.Appliance(WS,1,2400,1,0.5*60,0.1,5,fixed_cycle = 1,occasional_use = 0.1,wd_we_type = 0)
#time window: [15:00-19:00]
Saw_WS.windows([15*60,19*60],r_w = 0.35)
Saw_WS.specific_cycle_1(2400,5,720,25,0.1)

Saw_WS.cycle_behaviour([15*60,19*60])

Angle_grinder_WS = WS.Appliance(WS,1,1050,1,0.5*60,0.1,5,occasional_use = 0.1,wd_we_type = 0)
#time window: 15:00-19:00
Angle_grinder_WS.windows([15*60,19*60],r_w = 0.35)

"""weekends"""

#using r_t = 0.2 and r_w = 0.35
Indoor_LED_WS_we = WS.Appliance(WS,8,9,1,4*60,0.2,5,occasional_use = 0.5,wd_we_type = 1)
#time window: 12:00-19:00
Indoor_LED_WS_we.windows([12*60,19*60],r_w=0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_WS_we = WS.Appliance(WS,4,50,2,4*60,0.2,5,occasional_use = 0.5,wd_we_type = 1)
#time window: 12:00-19:00
Fan_WS_we.windows([12*60,19*60],r_w=0.35)

Tablet_WS_we = WS.Appliance(WS,4,15,1,2*60,0.1,5,occasional_use = 0.5,wd_we_type = 1)
#[12:00-19:00]
Tablet_WS_we.windows([12*60,19*60],r_w = 0.35)

Drill_WS_we = WS.Appliance(WS,1,100,1,0.5*60,0.1,5,occasional_use = 0.2,wd_we_type = 1)
#[12:00-19:00]
Drill_WS_we.windows([12*60,19*60],r_w = 0.35)

Saw_WS_we = WS.Appliance(WS,1,2400,1,0.5*60,0.1,5,fixed_cycle = 1,occasional_use = 0.1,wd_we_type = 1)
#time window: [12:00-19:00]
Saw_WS_we.windows([12*60,19*60],r_w = 0.35)
Saw_WS_we.specific_cycle_1(2400,5,720,25,0.1)

Saw_WS_we.cycle_behaviour([12*60,19*60])

Angle_grinder_WS_we = WS.Appliance(WS,1,1050,1,0.5*60,0.1,5,occasional_use = 0.2,wd_we_type = 1)
#time window: 12:00-19:00
Angle_grinder_WS_we.windows([12*60,19*60],r_w = 0.35)

"""---------Appliances Computer lab----------------"""

PC_CL = CL.Appliance(CL,30,60,1,6*60,0.1,5,wd_we_type = 0)
#time window: 07:00-17:00
PC_CL.windows([7*60,17*60],r_w = 0.35)

#extra appliances to simulate behavior after school hours
PC_CL_late = CL.Appliance(CL,5,60,1,1*60,0.1,5,wd_we_type = 0,occasional_use =  0.2)
#time window: 17:00-19:00
PC_CL_late.windows([17*60,19*60],r_w = 0.35)

LED_CL = CL.Appliance(CL,4,9,1,7*60,0.2,5,wd_we_type = 0)
#time window: 07:00-19:00
LED_CL.windows([7*60,19*60],r_w=0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_CL = CL.Appliance(CL,2,50,1,7*60,0.2,5,wd_we_type = 0)
#time window: 07:00-19:00
Fan_CL.windows([7*60,19*60],r_w=0.35)

"""----------Appliances classrooms---------------"""

"""Classroom type 1 (Class 1 and 2):"""
LED_Class_T1 = Class_T1.Appliance(Class_T1,4,9,1,7*60,0.2,5,wd_we_type = 0)
#time window: 07:00-17:00
LED_Class_T1.windows([7*60,17*60],r_w=0.35)

#using r_t = 0.2 and r_w = 0.35
Fan_Class_T1 = Class_T1.Appliance(Class_T1,2,50,1,7*60,0.2,5,wd_we_type = 0)
#time window: 07:00-17:00
Fan_Class_T1.windows([7*60,17*60],r_w=0.35)

"""PP1 and PP2"""
LED_PP = PP.Appliance(PP,4,9,1,7*60,0.2,5,wd_we_type = 0)
#time window: 07:00-17:00
LED_PP.windows([7*60,17*60],r_w=0.35)

"""Classroom toilets"""
LED_CT = CT.Appliance(CT,4,9,1,2*60,0.2,5,wd_we_type = 0)
#time window: 07:00-17:00
LED_CT.windows([7*60,17*60],r_w=0.35)

"""-------------Appliances Staff Court--------------"""

#using r_t = 0.2 and r_w = 0.35
Outdoor_LED_SC = SC.Appliance(SC,5,9,2,1*60,0.2,5)
#time window: 19:00-07:00
Outdoor_LED_SC.windows([19*60,23*60+59],[0,7*60],0.35)

"""----------Appliances Weekday Staff Court----------------"""

Fan_SC = SC.Appliance(SC,6,50,2,9*60,0.2,5,wd_we_type = 0)
#time window: 17:00-07:00
Fan_SC.windows([17*60,23*60+59],[0,7*60],0.35)

Phone_SC = SC.Appliance(SC,6,7,1,2*60,0.2,5,wd_we_type = 0)
#time window: 17:00-23:59
Phone_SC.windows([17*60,23*60+59],r_w =0.35)

PC_SC = SC.Appliance(SC,6,60,1,2*60,0.1,5,wd_we_type = 0)
#time window: 17:00-23:59
PC_SC.windows([17*60,23*60+59],r_w = 0.35)

Iron_SC = SC.Appliance(SC,1,1000,1,1*60,0.1,5,wd_we_type = 0,occasional_use = 0.33)
#time window: 17:00-21:00
Iron_SC.windows([17*60,21*60],r_w = 0.35)

Indoor_LED_SC = SC.Appliance(SC,12,9,2,4*60,0.2,5,wd_we_type = 0)
#time window 1: 06:00-07:00
#time window 2: 19:00-23:59
Indoor_LED_SC.windows([6*60,7*60],[19*60,23*60+59],0.35)

"""----------Appliances Weekend Staff Court----------------"""
Fan_SC_we = SC.Appliance(SC,3,50,3,10*60,0.2,5,wd_we_type = 1)
#time window 1: 12:00-14:00
#time window 2: 19:00-07:00
Fan_SC_we.windows([12*60,14*60],[19*60,23*60+59],0.35,[0,7*60])

Phone_SC_we = SC.Appliance(SC,3,7,1,2*60,0.2,5,wd_we_type = 1)
#time window: 07:00-23:59
Phone_SC_we.windows([7*60,23*60+59],r_w =0.35)

PC_SC_we = SC.Appliance(SC,3,60,1,2*60,0.1,5,wd_we_type = 1)
#time window: 07:00-23:59
PC_SC_we.windows([7*60,23*60+59],r_w = 0.35)

Iron_SC_we = SC.Appliance(SC,1,1000,1,1*60,0.1,5, wd_we_type = 1,occasional_use = 0.5)
#time window: 10:00-21:00
Iron_SC_we.windows([10*60,21*60],r_w = 0.35)

Indoor_LED_SC_we = SC.Appliance(SC,6,9,2,4*60,0.2,5,wd_we_type = 1)
#time window 1: 06:00-07:00
#time window 2: 19:00-23:59
Indoor_LED_SC_we.windows([6*60,7*60],[19*60,23*60+59],0.35)































































