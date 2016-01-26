# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 16:19:34 2015

@author: adityanagarajan
"""

import os
import time
import DFWnet
import shutil

DFW = DFWnet.CommonData()

doy = str(time.gmtime().tm_yday).zfill(3)
yr = str(time.gmtime().tm_year)
site='nwsd'

def move_nwsd(site,yr,doy):
    dropbox_path = '/home/aditya/Dropbox/Final_Data/RINEX_files/' + yr + os.sep
    base_path = '/var/www/html/gpsmet/CASA/Rinex/'


    met_path = base_path + yr + os.sep +site + os.sep +'met' + os.sep + doy
    obs_path = base_path + yr + os.sep +site + os.sep +'obs' + os.sep + doy
    nav_path = base_path + yr + os.sep +site + os.sep +'nav' + os.sep + doy

    if not os.path.exists(met_path):
        os.mkdir(met_path)
    if not os.path.exists(obs_path):
        os.mkdir(obs_path)
    if not os.path.exists(nav_path):
        os.mkdir(nav_path)

    initial=os.getcwd()
    os.chdir(initial)

    files_to_move = os.listdir(dropbox_path + doy)
    print files_to_move

    met_file = filter(lambda x: x[-4:] == '.' + yr[-2:] + 'm',files_to_move)
    obs_files = filter(lambda x: x[-4:] == '.' + yr[-2:] + 'o',files_to_move)
    nav_files = filter(lambda x: x[-4:] == '.' + yr[-2:] + 'n',files_to_move)
    print obs_files
    for o in obs_files:
#        shutil.move(dropbox_path + doy + os.sep + o,obs_path + os.sep)
        print(dropbox_path + doy + os.sep + o,obs_path + os.sep)

    for n in nav_files:
#        shutil.move(dropbox_path + doy + os.sep + n,nav_path + os.sep)
        print(dropbox_path + doy + os.sep + n,nav_path + os.sep)
        


    print 'done'

doys = [str(x).zfill(3) for x in range(1,13)]

for doy in doys:
    print doy
    move_nwsd(site,yr,doy)








