# -*- coding: utf-8 -*-

#%% Definition of the inputs
'''
Input data definition
'''

import pandas as pd
from Load_Profile.ramp.core.core import User

from Load_Profile.ramp.core.core import User


User_list = []

"""------------- BASE LOAD STAFF COURT -------------"""

"""-------------Hot season; January, 31 days (regular school, high visitor activity)-------------"""

#Staff Court
SC = User("Staff Court",1,3)
User_list.append(SC)





"""-------- LIGHTNING --------"""

Indoor_LED_SC_DAY_wd = SC.Appliance(SC,12,9,1,1*60,0,1*60, wd_we_type = 0)
#time window: 06:00-07:00
Indoor_LED_SC_DAY_wd.windows([6*60,7*60])

Indoor_LED_SC_DAY_we = SC.Appliance(SC,6,9,1,1*60,0,1*60, wd_we_type = 1)
#time window: 06:00-07:00
Indoor_LED_SC_DAY_we.windows([6*60,7*60])

Indoor_LED_SC_NIGHT_wd = SC.Appliance(SC,12,9,1,5*60,0,5*60, wd_we_type = 0)
#time window: 18:00-23:59
Indoor_LED_SC_NIGHT_wd.windows([18*60,23*60+59])

Indoor_LED_SC_NIGHT_we = SC.Appliance(SC,6,9,1,5*60,0,5*60, wd_we_type = 0)
#time window: 18:00-23:59
Indoor_LED_SC_NIGHT_we.windows([18*60,23*60+59])

Outdoor_LED_SC_DAY = SC.Appliance(SC,6,9,1,1*60,0,1*60)
#time window: 06:00-07:00
Outdoor_LED_SC_DAY.windows([6*60,7*60])

Outdoor_LED_SC_NIGHT = SC.Appliance(SC,6,9,1,5*60,0,5*60)
#time window: 18:00-23:59
Outdoor_LED_SC_NIGHT.windows([18*60,23*60+59])