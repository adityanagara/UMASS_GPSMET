# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 15:18:15 2015

@author: adityanagarajan
"""

import os
import ftplib
import time
import DFWnet
import shutil

import subprocess

DFW = DFWnet.CommonData()


if time.gmtime().tm_hour == 0:
    doy = str(time.gmtime().tm_yday - 1).zfill(3)
else:
    doy = str(time.gmtime().tm_yday).zfill(3)

yr = str(time.gmtime().tm_year)

site='nwsd'

def download_file_to(doy,obs_nav_met):
    
    base_path = '/var/www/html/gpsmet/CASA/Rinex/'
    
    if obs_nav_met == 'obs':
        download_file_to= base_path + yr + os.sep +site + os.sep +'obs' + os.sep + doy
    elif obs_nav_met == 'nav':
        download_file_to= base_path + yr + os.sep +site + os.sep +'nav' + os.sep + doy
    elif obs_nav_met == 'met':
        download_file_to= base_path + yr + os.sep +site + os.sep +'met' + os.sep + doy
    if not os.path.exists(download_file_to):
        os.mkdir(download_file_to)
    os.chdir(download_file_to)
    
    k = os.getcwd()
    print 'The current directory is in download files!'
    print k

initial=os.getcwd()
os.chdir(initial)
alpha,sigma = DFW.make_alpha_dict()




def change_nwsd_header(doy):
    global site
    base_path = '/var/www/html/gpsmet/CASA/Rinex/'
    yr = str(time.gmtime().tm_year)
    
    nwsd = base_path + yr + os.sep +site + os.sep +'obs' + os.sep + doy +os.sep + site + doy + '0.' + str(time.gmtime().tm_year)[-2:] + 'o'
    k=open(nwsd,'r')
    p=k.readlines()
    k.close()
    k=open(nwsd,'w')
    replace_1='     2.10           OBSERVATION DATA    GPS                 RINEX VERSION / TYPE\n'
    replace_2='WFO                                                         MARKER NAME         \n'    
    replace_3='Aditya N            UMASS                                   OBSERVER / AGENCY   \n'    
    replace_5='200022              HEM52W          NONE                    ANT # / TYPE\n'
    replace_6='1862965             HEM P307 ECLIPSE II MFA_1.2Qe           REC # / TYPE / VERS \n'    
    p[0]=replace_1
    p[2]=replace_2
    p[3]=replace_3
    p[4]=replace_6
    p[5]=replace_5
    k.writelines(p)
    k.close()
    DFWnet_path = '/home/aditya/UMASS/DFWnet/net1/2015/rinex/'
    
    subprocess.call(['mv','-f',nwsd,DFWnet_path])
    
    


def merge_rinex_o(doy,site):
    download_file_to(doy,'obs')
    subprocess.call(['sh_merge_rinex','-site',site,'-year',str(time.gmtime().tm_year),'-days',doy])

def copy_met_file(doy):
    source_ = '/var/www/html/gpsmet/CASA/Rinex/2015/nwsd/met/' + doy + os.sep + 'nwsd' + doy + '0.' + str(time.gmtime().tm_year)[-2:] + 'm'
    dest_ = '/home/aditya/UMASS/DFWnet/net1/' + str(time.gmtime().tm_year) + os.sep + 'met/'  
    subprocess.call(['cp','-f',source_,dest_])
    

merge_rinex_o(doy,site)

change_nwsd_header(doy)


copy_met_file(doy)
os.chdir(initial)


