#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      GPSMET1
#
# Created:     31/07/2014
# Copyright:   (c) GPSMET1 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import time
import serial
import sys
import os

'''
ser1 --> Vaisala
ser2 --> Paros
'''
def check_serial_ports(ser1,ser2):
    if ser2.isOpen():
        ser2.close()
    ser2.open()
    ser2.isOpen()
    if ser1.isOpen:
        ser1.close()
    ser1.open()
    k = '*0100P3' + '\r\n'
    r = '0R2!'
    ser2.write(k)
    ser1.write(r)
    time.sleep(0.025)
    p = ser2.readline()
    q = ser1.readline()
    if p[:5] == '*0001' and q[:3] == '0R2':
        print 'The response is right'
        ser2.close()
        ser1.close()
    else:
        ser2.close()
        ser1.close()
        sys.exit('The response is incorrect check the serial ports')

def Open_Serial(ser):
    if ser.isOpen():
        ser.close()
    ser.open()
    ser.isOpen()

def Query_Msg(ser1,ser2):
    vaisala = '0R2!'
    paros = '*0100P3' + '\r\n'
    ser1.write(vaisala)
    ser2.write(paros)
    time.sleep(0.025)
    v = ser1.readline()
    p = ser2.readline()
    return (v,p)

def Close_Serial(ser):
    if ser.isOpen():
        ser.close()

def Check_Day_File(day):
    file_path = 'C:\Daily_Met_Data' + os.sep + str(time.gmtime().tm_year) + os.sep + 'cnvl' + str(day).zfill(3) + '0.' + str(time.gmtime().tm_year)[-2:] + 'm'
    k = os.path.exists(file_path)
    return k

def make_RINEX_met():
    time_stamp = '\n ' + str(int(str(time.gmtime().tm_year)[-2:])).rjust(2)  + str((time.gmtime().tm_mon)).rjust(3) + str(time.gmtime().tm_mday).rjust(4)[-3:] + str(time.gmtime().tm_hour).rjust(5)[-3:] + str(time.gmtime().tm_min).rjust(6)[-3:] + str(time.gmtime().tm_sec).rjust(7)[-3:]
    ser_vaisala = serial.Serial(
    port='COM4',
    baudrate=4800,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
    )
    ser_paros = serial.Serial(
    port='COM7',
    baudrate=19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
    )
    templet_file = 'C:\Daily_Met_Data\Templet.txt'
    position = 1099
    t_file = open(templet_file,'r')
    templet_data = t_file.read()
    t_file.close()
    try:
        print 'Windows Scheduler has Started this Program!'
        Open_Serial(ser_vaisala)
        Open_Serial(ser_paros)
        file2 = 'C:\Daily_Met_Data' + os.sep + str(time.gmtime().tm_year) + os.sep + 'cnvl' + str(time.gmtime().tm_yday).zfill(3)  + '0.' + str(time.gmtime().tm_year)[-2:] + 'm'
        if not Check_Day_File(time.gmtime().tm_yday):
            g = open(file2,'w+')
            g.write(templet_data)
            g.close()
        with open(file2,'a') as f:
            PTU = Query_Msg(ser_vaisala,ser_paros)
            print PTU
            vai = PTU[0]
            par = PTU[1]
            tai=vai.index('Ta=')
            rai=vai.index('Ua=')
            tai_end=vai.index('C')
            rai_end=vai.index('P,')
            ta =vai[tai+3:tai_end]
            rh=vai[rai+3:rai_end]
            pr1 = float(par[7:15]) * 1000
            pr = '%.1f'%pr1
            print time_stamp + ''.rjust(1) + pr + ''.rjust(3) + str(ta) + ''.rjust(3) + str(rh)
            print time.gmtime()
            f.write(time_stamp + ''.rjust(1) + pr + ''.rjust(3) + str(ta) + ''.rjust(3)  + str(rh))
            time.sleep(1)
            Close_Serial(ser_vaisala)
            Close_Serial(ser_paros)
    except KeyboardInterrupt:
        print 'We Should Never reach here!'
        Close_Serial(ser_vaisala)
        Close_Serial(ser_paros)
    finally:
        Close_Serial(ser_vaisala)
        Close_Serial(ser_paros)
        print 'We will never reach this place!'

make_RINEX_met()