# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 13:27:34 2015

@author: adityanagarajan
"""


import ftplib
import time
import os
import subprocess
import shutil
import math
import DFWnet

def make_alpha_dict():
    alpha_dict = {}
    numa_dict = {}
    alpha_list = ['a', 'b', 'c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for i in range(0,26):
        alpha_dict[i] = alpha_list[i]
        numa_dict[i] = str(i).zfill(2)
    return alpha_dict, numa_dict

'''
Download files from SOPAC
Reference files with long baseline

'''
def download_ref_stations(station_list):
    alpha,sigma = make_alpha_dict()
    if time.gmtime().tm_hour == 0:
        doy = str(time.gmtime().tm_yday -1).zfill(3)
        real_hour = str(sigma[23])
        hour_alpha = str(alpha[23])
    else:
        doy = str(time.gmtime().tm_yday).zfill(3)
        real_hour = str(sigma[time.gmtime().tm_hour -1])
        hour_alpha = str(alpha[time.gmtime().tm_hour -1])
    # Connect to SOPAC DB
    ftp = ftplib.FTP('garner.ucsd.edu','anonymous','adityanagara@umass.edu')
    print 'logged in'
    base_folder='/pub/nrtdata' + os.sep + str(time.gmtime().tm_year) + os.sep   
    dyna_folder= base_folder + doy + os.sep + real_hour  
    ftp.cwd(dyna_folder)
    file_list=ftp.nlst()
    for stn in station_list:
        dyna_file_name = stn + doy + hour_alpha + '.' + str(time.gmtime().tm_year)[-2:] + 'd.Z'
#        dyna_file_name_nav=stn + doy + hour_alpha + '.' + str(time.gmtime().tm_year)[-2:] + 'n.Z'
        
        if dyna_file_name in file_list:
            os.chdir('/home/aditya/UMASS/DFWnet/net1/2015/temp_rinex/obs')
            gfile = open(dyna_file_name,'wb')
            ftp.retrbinary('RETR ' + dyna_file_name,gfile.write)
            gfile.close()
            subprocess.call(['uncompress','-f',dyna_file_name])
            subprocess.call(['crx2rnx',dyna_file_name.strip('.Z'),'-f'])
            subprocess.call(['rm',dyna_file_name.strip('.Z')])
        else:
            print 'WARNING: SOPAC obs file not found ' + dyna_file_name
#        if dyna_file_name_nav in file_list:
#            os.chdir('/home/aditya/UMASS/DFWnet/net1/2015/temp_rinex/nav')
#            gfile = open(dyna_file_name_nav,'wb')
#            ftp.retrbinary('RETR ' + dyna_file_name_nav,gfile.write)
#            gfile.close()
#        else:
#            print 'WARNING: SOPAC nav file not found ' + dyna_file_name_nav
    ftp.close()


'''
Download files from the NOAA CORS data base:
1. Thes files include broadcast ephemerides (brdc combination of nav files 
containing clock information)

2. net1 DFW RINEX files
'''

def download_DFW_and_nav(doy,noaa_sites):
    alpha,sigma = make_alpha_dict()
    if time.gmtime().tm_hour == 0:
        doy = str(time.gmtime().tm_yday -1).zfill(3)
        hour_alpha = str(alpha[23])
    else:
        doy = str(time.gmtime().tm_yday).zfill(3)
        hour_alpha = str(alpha[time.gmtime().tm_hour -1])

    # Connect to NOAA DB
    noaa_ftp = ftplib.FTP('geodesy.noaa.gov','anonymous','adityanagara@umass.edu')
    base_folder = '/cors/rinex/' + str(time.gmtime().tm_year) + os.sep + doy
    brdc_file = 'brdc' + doy + '0.' + str(time.gmtime().tm_year)[-2:] + 'n.gz'
    # Change to the current day in the ftp directory
    
    noaa_ftp.cwd(base_folder)
    os.chdir('/home/aditya/UMASS/DFWnet/net1/2015/brdc')
    # Get latest brdc file
    brdc_temp = open(brdc_file,'wb')
    noaa_ftp.retrbinary('RETR ' + brdc_file,brdc_temp.write)
    brdc_temp.close()
    # Uncompress the brdc file
    subprocess.call(['uncompress','-f',brdc_file])
    os.chdir('/home/aditya/UMASS/DFWnet/net1/2015/temp_rinex/obs/')
    noaa_ftp_site_list =  noaa_ftp.nlst()
    for site in noaa_sites:
        print site
        if site in noaa_ftp_site_list:
            noaa_ftp.cwd(base_folder + os.sep + site)
            temp_file_list = noaa_ftp.nlst()
            rinex_file = site + doy + hour_alpha + '.' + str(time.gmtime().tm_year)[-2:] + 'o.gz'
            print rinex_file            
            if rinex_file in temp_file_list:
                rinex_temp = open(rinex_file,'wb')
                noaa_ftp.retrbinary('RETR ' + rinex_file,rinex_temp.write)
                rinex_temp.close()
                subprocess.call(['uncompress','-f',rinex_file])
            else:
                print 'WARNING: Site not published on time ' + rinex_file
        else:
            print 'WARNING: Site folder not found ' + site
    noaa_ftp.close()

def merge_rinex_files(doy,station_list):
    base_path = '/home/aditya/UMASS/DFWnet/net1/2015/temp_rinex/obs/'
#    dest_path = '/home/aditya/UMASS/DFWnet/net1/2015/rinex'
    os.chdir(base_path)
    for site in station_list:
        subprocess.call(['sh_merge_rinex','-site',site,'-year',str(time.gmtime().tm_year),'-days',doy])
#        subprocess.call(['mv',base_path + site + doy + '0.' + str(time.gmtime().tm_year)[-2:] + 'o'],dest_path)
        
        
def remove_brdc_comments(doy):
    brdc_file = '/home/aditya/UMASS/DFWnet/net1/2015/brdc/' + 'brdc' + doy + '0.' + str(time.gmtime().tm_year)[-2:] + 'n'
    
    with open(brdc_file,'r') as f1: 
        initial_lines = f1.readlines()
    comment_lines = filter(lambda x: 'COMMENT' in x,initial_lines)
    map(lambda x: initial_lines.remove(x),comment_lines[1:])
    with open(brdc_file,'w+') as f2:
        f2.writelines(initial_lines)
  

year = str(time.gmtime().tm_year)

if time.gmtime().tm_hour == 0:
    doy = str(time.gmtime().tm_yday - 1).zfill(3)
else:
    doy = str(time.gmtime().tm_yday).zfill(3)

DFW = DFWnet.CommonData()
noaa_sites = list(DFW.sites[DFW.sites[:,-1] == 'net1'][:,0])


long_baseline_station = ['ac20','p019','conz','unbj','gold','amc2','areq','drao']
download_ref_stations(long_baseline_station)

download_DFW_and_nav(doy,noaa_sites)
list.extend(noaa_sites,long_baseline_station)
merge_rinex_files(doy,noaa_sites)
remove_brdc_comments(doy)
    
    

