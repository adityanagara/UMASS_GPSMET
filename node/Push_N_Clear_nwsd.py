# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      GPSMET1
#
# Created:     25/07/2014
# Copyright:   (c) GPSMET1 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

'''
    Pocket max started logging at 12:00PM 07/25/2014.
'''

import subprocess
import os
import time
import shutil

'''
    *Input File Determination:
    This function is used to determine the input file, once the file is creater 5 minutes later the file
    is processed. max(num_list) - 1.
'''
def get_file_no():
    dir = 'C:\Daily_GPS_Data' + os.sep + '20150813'
    list = os.listdir(dir)
    num_list = []
    for file in list:
        index = file.index('.')
        num_list.append(file[4:index])
    num_list = [int(i) for i in num_list]
    this_file = max(num_list) - 1
    return num_list,this_file

'''
    *Output file determination
    map each hour file to the sh_merge_rinex(a,b,c,d...) readible format. exception for hour zero,
    2 files need to be created on with 'a' current day(23-0), and
    'y'(0-23) for previous day. This exception is handled in main code.
'''

def alpha_dict():
    alpha = {}
    alpha_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    for i in range(0,26):
        alpha[i] = alpha_list[i]
    return alpha

'''
    Move the obs file from source to dest with correct formating.
'''

try:

    stn = 'nwsd'
    initial = os.getcwd()
    print 'Rinex File Manager!'
    hour = time.gmtime().tm_hour
    day = time.gmtime().tm_yday
#    os.chdir('C:\Users\GPSMET1\Desktop\RINEX\RinexSLX_v2.8.3')
    output_dir = 'C:' + os.sep + 'Users' + os.sep + 'aditya\Dropbox\Final_Data\RINEX_files' + os.sep + str(time.gmtime().tm_year) + os.sep + str(time.gmtime().tm_yday).zfill(3)
    output_dir_bin='C:' + os.sep + 'Users' + os.sep + 'aditya\Dropbox\Final_Data' + os.sep + 'binary_files' + os.sep + str(time.gmtime().tm_yday).zfill(3)
    all_files,current_file =get_file_no()
    print current_file
    input_file = 'C:\Daily_GPS_Data' + os.sep + '20150813' + os.sep + stn + str(current_file) + '.' + str(time.gmtime().tm_year)[-2:] + 'o'
    input_file_nav = 'C:\Daily_GPS_Data' + os.sep + '20150813' + os.sep + stn + str(current_file) + '.' + str(time.gmtime().tm_year)[-2:] + 'n'
    print input_file
    file_alpha=alpha_dict()
    if time.gmtime().tm_hour == 0:
        output_file_1 = 'C:' + os.sep + 'Users' + os.sep + 'aditya\Dropbox\Final_Data\RINEX_files' + os.sep + str(time.gmtime().tm_year) + os.sep + str(time.gmtime().tm_yday - 1).zfill(3)  + os.sep + stn + str(time.gmtime().tm_yday - 1).zfill(3) +'y' + '.' + str(time.gmtime().tm_year)[-2:] + 'o'
        output_file_1_nav = 'C:' + os.sep + 'Users' + os.sep + 'aditya\Dropbox\Final_Data\RINEX_files' + os.sep + str(time.gmtime().tm_year) + os.sep + str(time.gmtime().tm_yday - 1).zfill(3) + os.sep + stn + str(time.gmtime().tm_yday - 1).zfill(3) +'y' + '.' + str(time.gmtime().tm_year)[-2:] + 'n'
        output_file = 'C:' + os.sep + 'Users' + os.sep + 'aditya\Dropbox\Final_Data\RINEX_files' + os.sep + str(time.gmtime().tm_year) + os.sep + str(time.gmtime().tm_yday).zfill(3) + os.sep + stn + str(time.gmtime().tm_yday).zfill(3) + file_alpha[time.gmtime().tm_hour] + '.' + str(time.gmtime().tm_year)[-2:] + 'o'
        output_file_nav = 'C:' + os.sep + 'Users' + os.sep + 'aditya\Dropbox\Final_Data\RINEX_files' + os.sep + str(time.gmtime().tm_year) + os.sep + str(time.gmtime().tm_yday).zfill(3) + os.sep + stn + str(time.gmtime().tm_yday).zfill(3) + file_alpha[time.gmtime().tm_hour] + '.' + str(time.gmtime().tm_year)[-2:] + 'n'
    else:
        output_file= 'C:' + os.sep + 'Users' + os.sep + 'aditya\Dropbox\Final_Data\RINEX_files' + os.sep + str(time.gmtime().tm_year)  + os.sep + str(time.gmtime().tm_yday).zfill(3) + os.sep + stn + str(time.gmtime().tm_yday).zfill(3) + file_alpha[time.gmtime().tm_hour] + '.' + str(time.gmtime().tm_year)[-2:] + 'o'
        output_file_nav= 'C:' + os.sep + 'Users' + os.sep + 'aditya\Dropbox\Final_Data\RINEX_files' + os.sep + str(time.gmtime().tm_year) + os.sep + str(time.gmtime().tm_yday).zfill(3) + os.sep + stn + str(time.gmtime().tm_yday).zfill(3) + file_alpha[time.gmtime().tm_hour] + '.' + str(time.gmtime().tm_year)[-2:] + 'n'
    print 'Begin'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print 'The new directory is made!' + output_dir
        time.sleep(2)
    if not os.path.exists(output_dir_bin):
        os.makedirs(output_dir_bin)
        print 'Making Day Folder!'
        time.sleep(2)
    print '###### Following data now being created #######'
    print 'input file: ' + input_file
    print 'output file: ' + output_file
    print 'sleeping...'
    if os.path.exists(input_file):
        print 'Yes path exists Creating the files...'
        shutil.move(input_file,output_file)
        shutil.move(input_file_nav,output_file_nav)
    time.sleep(5)
    print 'processes terminated'
    met_file=  'C:\Daily_Met_Data' + os.sep  + str(time.gmtime().tm_year) + os.sep + 'nwsd' + str(time.gmtime().tm_yday).zfill(3)    + '0.' + str(time.gmtime().tm_year)[-2:] + 'm'
    out_met= 'C:' + os.sep + 'Users' + os.sep + 'aditya\Dropbox\Final_Data\RINEX_files' + os.sep + str(time.gmtime().tm_year) + os.sep + str(time.gmtime().tm_yday).zfill(3) + os.sep + stn + str(time.gmtime().tm_yday).zfill(3) + '0.' + str(time.gmtime().tm_year)[-2:] + 'm'
    shutil.copy2(met_file,out_met)
    time.sleep(10)
    if time.gmtime().tm_hour == 0:
        met_file=  'C:\Daily_Met_Data'  + os.sep + str(time.gmtime().tm_year) + os.sep + 'nwsd' + str(time.gmtime().tm_yday -1).zfill(3) + '0.' + str(time.gmtime().tm_year)[-2:] + 'm'
        out_met= 'C:' + os.sep + 'Users' + os.sep + 'aditya\Dropbox\Final_Data\RINEX_files' +  os.sep + str(time.gmtime().tm_year) + os.sep + str(time.gmtime().tm_yday -1).zfill(3) + os.sep + stn + str(time.gmtime().tm_yday -1) + '0.' + str(time.gmtime().tm_year)[-2:] + 'm'
        shutil.copy2(output_file,output_file_1)
        shutil.copy2(output_file_nav,output_file_1_nav)
        shutil.copy2(met_file,out_met)
    else:
        shutil.copy2(met_file,out_met)

except KeyboardInterrupt:
    print 'Something went wrong'
finally:
    print 'do not see this!'