# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 23:18:01 2015

@author: adityanagarajan

This script calls sh_gamit and sh_metutil commands from the project folders
Usage 

python run_gamit_nrt.py [network]

network = net1,net2,net3,net4 
"""

import os
import sys
import subprocess
import time

net = sys.argv[1]

if time.gmtime().tm_hour == 0:
    doy = str(time.gmtime().tm_yday - 1).zfill(3)
else:
    doy = str(time.gmtime().tm_yday).zfill(3)

def run_gamit(doy,net,year):
    # Change to project directory
    os.chdir('/home/aditya/UMASS/DFWnet' + os.sep + net + os.sep + year)
    # Call the GAMIT commands like you would in the terminal
    subprocess.call(['sh_gamit','-expt',net,'-d',year,'-orbit','IGSU','-met'])

def run_metutil(doy,net,year):
    
    base_folder = '/home/aditya/UMASS/DFWnet' + os.sep + net + os.sep + year + os.sep + doy
    os.chdir(base_folder)
    # Run met util commands for each site 
    subprocess.call(['sh_metutil','-f','onet1a.' + doy,'-z','zcnvl' + year[-1:] + '.' + doy,'-i','300'])
    subprocess.call(['sh_metutil','-f','onet1a.' + doy,'-z','znwsd' + year[-1:] + '.' + doy,'-i','300'])
    # Copy output IPW files to the WV directory for plotting
    subprocess.call(['cp','-f','met_cnvl.' + year[-2:] + doy,'/home/aditya/UMASS/DFWnet/net1/' + year + '/WV/'])
    subprocess.call(['cp','-f','met_nwsd.' + year[-2:] + doy,'/home/aditya/UMASS/DFWnet/net1/' + year + '/WV/'])
    base_folder_2 = '/home/aditya/UMASS/DFWnet' + os.sep + net + os.sep + year + os.sep
    os.chdir(base_folder_2)

year = str(time.gmtime().tm_year)

initial = os.getcwd()
os.chdir(initial)
# Run gamit and metutil
run_gamit(doy,net,year)
run_metutil(doy,net,year)


