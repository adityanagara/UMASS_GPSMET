# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 14:04:33 2015

@author: adityanagarajan
"""

import numpy as np
import time
import os
import DFWnet

DFW = DFWnet.CommonData()

site = 'nwsd'
# /home/aditya/Dropbox/Final_Data/RINEX_files/2015/236

yr = '2015'

if time.gmtime().tm_hour == 0:
    doy = str(time.gmtime().tm_yday - 1).zfill(3)
else:
    doy = str(time.gmtime().tm_yday).zfill(3)

current_hour = time.gmtime().tm_hour

# Convert UTS to CST
current_hour_cst = current_hour-6

DFW.doytodate(int(yr[-2:]),int(doy))

# Get previous day of the month 
#if int(doy) > 1:
#    
#    DFW.doytodate(int(yr[-2:]),int(doy) - 1)
#    
#else:
#    DFW.doytodate(int(yr[-2:]) -1,365)
       

print DFW.mon,DFW.day

# Find the starting time index
data = np.loadtxt('graphs.txt',dtype='S')

#Down sample to 5 minute intervals
data = np.array(filter(lambda x: float(x[1].split(':')[1]) % 5.0 == 0,data))

# Find current time step on the JSOS file
if current_hour_cst < 0:
    DFW.doytodate(int(yr[-2:]),int(doy) - 1)
    current_date = DFW.mon + os.sep + DFW.day + os.sep + DFW.yr
    current_hour_cst = 24 + current_hour_cst
else:
    DFW.doytodate(int(yr[-2:]),int(doy))
    current_date = DFW.mon + os.sep + DFW.day + os.sep + DFW.yr

# find the starting index corresponding to the current hour
start_idx = np.where(np.logical_and(data[:,0] == current_date,data[:,1] == str(current_hour_cst -1).zfill(2) +':00'))[0][0]



end_idx = np.where(np.logical_and(data[:,0] == current_date,data[:,1] ==  str(current_hour_cst).zfill(2)+':00'))[0][0]

tempVals = filter(lambda x: float(x[1].split(':')[1]) % 5.0 == 0,data[start_idx:end_idx,:])


print 'Verify with these values here---------------------'
print tempVals
print '--------------------------------------------------'
rhs = map(lambda x: x[-2],tempVals)
temps = map(lambda x: (float(x[2]) -32) *(5.0/9.0),tempVals)

temps = map(lambda x: '%.1f'%x,temps)


# Get the input met file
base_met_path = '/home/aditya/Dropbox/Final_Data/RINEX_files/' + yr + os.sep  + doy + os.sep
met_file = site + doy + '0.' + yr[-2:] + 'm'

##/var/www/html/gpsmet/CASA/Rinex/2015/nwsd/met/238
out_base = '/var/www/html/gpsmet/CASA/Rinex/' + yr + os.sep +site + os.sep +'met' + os.sep + doy

if not os.path.exists(out_base + os.sep + met_file):
    with open('/home/aditya/UMASS/commonFiles/Templet.txt','r') as temp1: temp_data = temp1.read()
       
    tempmfile = open(out_base + os.sep + met_file,'w+')
    tempmfile.write(temp_data)
    tempmfile.write('\n')
    tempmfile.close()

# Find the index of the file to which we can append the previous hour values(12 values)
hour_to_file_index = [11 + i*12 for i in range(25)]
if current_hour ==0:
    print 'Write to previous day file'
    
    with open(base_met_path + os.sep + met_file,'rb') as m:
        metLines = m.readlines()
        start_index = hour_to_file_index[23]
        end_index = hour_to_file_index[24]
        
        with open(out_base + os.sep + met_file,'a') as mout:
            for l,t,r in zip(metLines[start_index:end_index],temps,rhs):
                l = l.strip()
                statement = ' ' + l + ''.rjust(3) + t + ''.rjust(3) + r + '\n'
                print statement
                mout.write(statement)
else:
    with open(base_met_path + os.sep + met_file,'rb') as m:
        metLines = m.readlines()
        start_index = hour_to_file_index[current_hour - 1]
        end_index = hour_to_file_index[current_hour]
        with open(out_base + os.sep + met_file,'a') as mout:
            for l, t, r in zip(metLines[start_index:end_index],temps,rhs):
                l = l.strip()
                statement = ' ' + l + ''.rjust(3) + t + ''.rjust(3) + r + '\n'
                print statement
                mout.write(statement)
    print 'Write to current days file'
    
        


 
