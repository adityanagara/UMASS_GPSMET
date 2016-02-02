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

site='cnvl'

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


'''
    At hour 1 you need to download 2 files. 
'''
def download_from_node():
    global alpha,sigma,site,initial
    if time.gmtime().tm_hour == 0:
        doy = str(time.gmtime().tm_yday -1).zfill(3)
        file_to_get=site + doy + alpha[24] + '.' +  str(time.gmtime().tm_year)[-2:] + 'o'
        file_to_get_2=site + str(time.gmtime().tm_yday) + alpha[0] + '.' + str(time.gmtime().tm_year)[-2:] + 'o'
        file_to_get_2_nav=site + str(time.gmtime().tm_yday) + alpha[0] + '.' + str(time.gmtime().tm_year)[-2:] + 'n'
        file_to_get_nav=site + doy + alpha[24] + '.' + str(time.gmtime().tm_year)[-2:]+'n'
        file_to_get_met=site + doy + '0.' + str(time.gmtime().tm_year)[-2:]+ 'm'
    else:    
        doy = str(time.gmtime().tm_yday).zfill(3)
        file_to_get=site + doy + alpha[time.gmtime().tm_hour] + '.' + str(time.gmtime().tm_year)[-2:] + 'o'
        file_to_get_nav=site + doy + alpha[time.gmtime().tm_hour] + '.' + str(time.gmtime().tm_year)[-2:] + 'n'
        file_to_get_met=site + doy + '0.' + str(time.gmtime().tm_year)[-2:] + 'm'
    #ip_adr='50.187.48.43'
    #ip_adr='10.0.0.17'
    ip_adr='129.107.93.30'
    ftp2=ftplib.FTP(ip_adr,'GPSMET1','aditya')
    ftp2.set_pasv(False)
    dyna_folder_2 = 'RINEX_files' + os.sep + str(time.gmtime().tm_year) + os.sep + doy 
    ftp2.cwd(dyna_folder_2)
    file_list=ftp2.nlst()
    print 'logged in to node!'
    download_file_to(doy,'obs')
    if file_to_get in file_list:
        nfile= open(file_to_get,'wb')
        print file_to_get
        ftp2.retrbinary('RETR '+file_to_get,nfile.write)
        nfile.close()
        print 'We got the file >>>>>> ' + file_to_get
    else:
        print file_to_get + ' Not found!'
    download_file_to(doy,'nav')
    if file_to_get_nav in file_list:
        nfile_nav=open(file_to_get_nav,'wb')
        ftp2.retrbinary('RETR '+file_to_get_nav,nfile_nav.write)
        nfile_nav.close()
        print 'we got the file >>>>>>>> ' + file_to_get_nav
    else:
        print file_to_get_nav + 'Not found!'
    download_file_to(doy,'met')
    if file_to_get_met in file_list:
        nfile_met=open(file_to_get_met,'wb')
        ftp2.retrbinary('RETR '+file_to_get_met,nfile_met.write)
        nfile_met.close()
        print 'we got the file >>>>>>>> ' + file_to_get_met
    else:
        print file_to_get_met + ' Not found!'
    ftp2.close()
    if time.gmtime().tm_hour == 0:
        ftp2=ftplib.FTP(ip_adr,'GPSMET1','aditya')
        ftp2.set_pasv(False)
        print 'logged onto node again'
        os.chdir(initial)
        dyna_folder_once= 'RINEX_files' + os.sep + str(time.gmtime().tm_year) + os.sep  + str(time.gmtime().tm_yday)  
        ftp2.cwd(dyna_folder_once) 
        file_list=ftp2.nlst()
        download_file_to(str(time.gmtime().tm_yday),'obs')                
        if file_to_get_2 in file_list:
            nfile2=open(file_to_get_2,'wb')
            ftp2.retrbinary('RETR '+file_to_get_2,nfile2.write)
            nfile2.close()
            print 'We got the file >>>>>>>> ' + file_to_get_2
        else:
            print file_to_get_2 + 'Not found!'
        download_file_to(str(time.gmtime().tm_yday),'nav')
        if file_to_get_2_nav in file_list:
            nfile2_nav=open(file_to_get_2_nav,'wb')
            ftp2.retrbinary('RETR '+file_to_get_2_nav,nfile2_nav.write)
            nfile2_nav.close()
            print 'We got the file >>>>>>>>> ' + file_to_get_2_nav
        else:
            print file_to_get_2_nav + ' Not found!'
    print 'We got the file from the node'
    ftp2.close()

# This function changes the header of the RINEX files so that
# the antenna and receiver can be read by GAMIT and adds other details to it
def change_cnvl_header(doy):
    global site
    base_path = '/var/www/html/gpsmet/CASA/Rinex/'
    yr = str(time.gmtime().tm_year)
    cnvl = base_path + yr + os.sep +site + os.sep +'obs' + os.sep + doy +os.sep + site + doy + '0.' + str(time.gmtime().tm_year)[-2:] + 'o'
    k=open(cnvl,'r')
    p=k.readlines()
    k.close()
    k=open(cnvl,'w')
    replace_1='     2.10           OBSERVATION DATA    GPS                 RINEX VERSION / TYPE\n'
    replace_2='UTA                                                         MARKER NAME         \n'    
    replace_3='Aditya N            UMASS                                   OBSERVER / AGENCY   \n'    
    replace_5='200021              HEMA42          NONE                    ANT # / TYPE\n'
    replace_6='1862964             HEM P320 ECLIPSE II MFA_1.2Qe           REC # / TYPE / VERS \n'    
    p[0]=replace_1
    p[2]=replace_2
    p[3]=replace_3
    p[4]=replace_6
    p[5]=replace_5
    k.writelines(p)
    k.close()
    DFWnet_path = '/home/aditya/UMASS/DFWnet/net1/' +str(time.gmtime().tm_year) + '/rinex/'    
    subprocess.call(['mv','-f',cnvl,DFWnet_path])

# Call GAMIT command to merge all hourly files to single day file
def merge_rinex_o(doy,site):
    download_file_to(doy,'obs')
    subprocess.call(['sh_merge_rinex','-site',site,'-year',str(time.gmtime().tm_year),'-days',doy])

# Comy met file from common database to experiment folder for IPW processing
def copy_met_file(doy):
    source_cnvl = '/var/www/html/gpsmet/CASA/Rinex/' + str(time.gmtime().tm_year) + '/cnvl/met/' + doy + os.sep + 'cnvl' + doy + '0.' + str(time.gmtime().tm_year)[-2:] + 'm'
    dest_cnvl = '/home/aditya/UMASS/DFWnet/net1/' + str(time.gmtime().tm_year) + os.sep + 'met/'  
    subprocess.call(['cp','-f',source_cnvl,dest_cnvl])

download_from_node()
merge_rinex_o(doy,site)
change_cnvl_header(doy)
copy_met_file(doy)
os.chdir(initial)


