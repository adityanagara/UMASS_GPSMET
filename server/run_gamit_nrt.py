# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 23:18:01 2015

@author: adityanagarajan
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


def run_gamit(doy,net):
    
    os.chdir('/home/aditya/UMASS/DFWnet' + os.sep + net + '/2015')
    subprocess.call(['sh_gamit','-expt',net,'-d','2015',doy,'-orbit','IGSU','-met'])

#subprocess.call(['sh_metutil','-f',os.path.basename(o_file),'-m',os.path.basename(met_file),'-i','300'])

def run_metutil(doy,net):
    base_folder = '/home/aditya/UMASS/DFWnet' + os.sep + net + '/2015/' + doy
    os.chdir(base_folder)
    
    subprocess.call(['sh_metutil','-f','onet1a.' + doy,'-z','zcnvl' + str(time.gmtime().tm_year)[-1:] + '.' + doy,'-i','300'])
    subprocess.call(['sh_metutil','-f','onet1a.' + doy,'-z','znwsd' + str(time.gmtime().tm_year)[-1:] + '.' + doy,'-i','300'])
    #met_cnvl.15274
    subprocess.call(['cp','-f','met_cnvl.' + str(time.gmtime().tm_year)[-2:] + doy,'/home/aditya/UMASS/DFWnet/net1/2015/WV/'])
    subprocess.call(['cp','-f','met_nwsd.' + str(time.gmtime().tm_year)[-2:] + doy,'/home/aditya/UMASS/DFWnet/net1/2015/WV/'])
    base_folder_2 = '/home/aditya/UMASS/DFWnet' + os.sep + net + '/2015/'
    os.chdir(base_folder_2)
#    if time.gmtime().tm_hour == 0:
#        pass
#    else:
#        subprocess.call(['rm','-r',doy])
    
initial = os.getcwd()

os.chdir(initial)

run_gamit(doy,net)

run_metutil(doy,net)


