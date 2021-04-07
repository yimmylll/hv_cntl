#!/usr/bin/env python3

import math
import os
import sys
import time
import socket

import logging
import coloredlogs

from lib.command_interpret import CommandInterpret
from lib.hv_cntl import HvCntl 
from lib.defines import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
coloredlogs.install(level='DEBUG', logger=log)

from lib.send_array import SendArray
from lib.send_element import SendElement


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
coloredlogs.install(level='DEBUG', logger=log)

cycle=2500
gap=0.0105    #unit: meter
soundSpeed=340 #unit: meter per second
freq=40000 #unit: Hz
wavelength=soundSpeed/freq

def calc_distance(index, send_array, tx,ty,tz):
    return math.sqrt(pow(send_array._array[index].x-tx, 2) + pow(send_array._array[index].y-ty,2)+ pow(send_array._array[index].z-tz,2))

def main():
    num2Send=200
    arr = []

    kk = 0
    P_CHANGE = 27#169 221
    P_FIRST = 100
    TIME_BREAK = 1#SECOND
    right_flag = True

    for i in range(num2Send):
        ########### only for test ############
        # if i>=72 and i<=117 and (i % 2)==0:
        # # if i==26:
        #     inUse = 1
        # else:
        #     inUse = 0
        #######################
        if i == 33 or i == 57 or i==48:##ill port
            inUse = 0
        elif i>=24 and i<=68:
            inUse = 1
        elif i>=72 and i<=117:
            inUse = 1
        else:
            inUse = 0
        
        phase = 0
        
        new_element = SendElement()
        new_element.inUse = inUse
        if i == 66:
            new_element.order = 33
        elif i == 68:
            new_element.order = 57
        elif i == 67:
            new_element.order = 48
        elif i == 33 or i == 57 or i==48:##ill port
            new_element.order = num2Send+1#disable
        else:
            new_element.order = i
        new_element.x = (int(i/ARRAY_LENGTH)%ARRAY_LENGTH)*gap
        new_element.y = int(i%ARRAY_LENGTH) *gap
        new_element.z = 0


        arr.append(new_element)
    
        # tmp = [5, 6, 8, 15, 21, 49]
        # for i, j in zip(tmp, range(len(tmp))):
        #     #arr[i-1].order = 7 * 12 + j
        #     log.debug("new order: {}".format(arr[i-1].order))


    tx=gap*2 
    ty=gap*2  #unit: meter
    tz=0.03 #unit: meter

    mysendArray = SendArray(num2Send, arr)
####################################################
    while kk < 1:#for test
    #while k != -6:
        for i in range(num2Send):
            dist = calc_distance(i, mysendArray, tx, ty, tz)
            log.debug("i: {:d} \tdist: {:f}".format(i, dist))

            res = dist/wavelength - int(dist/wavelength)
            phase = (1 - res) * cycle

            index = arr[i].order
            #half work
            if index>=72 and index<=117 and (index % 2) == 0:
                arr[i].inUse = 1
            elif index>=60 and index<=65 and (index % 2) == 0:
                arr[i].inUse = 1
            elif index>=49 and index<=59 and (index % 2) == 1:
                arr[i].inUse = 1
            elif index>=24 and index<=41 and (index % 2) == 0:
                arr[i].inUse = 1
            else:
                arr[i].inUse = 0

            #change phase
            if kk==0:
                arr[i].phase = int(phase)*0 + P_FIRST
            else:
                if index>=77 and index<=85:
                    arr[i].phase += kk*(index-81)*P_CHANGE 
                elif index>=72 and index<=76:
                    arr[i].phase = kk*(72-index)*P_CHANGE
                elif index>=86 and index<=89:
                    arr[i].phase = kk*(90-index)*P_CHANGE
                elif index>=103 and index<=109:
                    arr[i].phase += kk*(index-106)*P_CHANGE
                elif index==102:
                    arr[i].phase += kk*2*P_CHANGE
                elif index==97:
                    arr[i].phase += kk*P_CHANGE
                elif index>=109 and index<=111:
                    arr[i].phase += kk*(112-index)*P_CHANGE
                #upper
                elif index>=29 and index<=37:
                    arr[i].phase += kk*(33-index)*P_CHANGE
                elif index>=24 and index<=28:
                    arr[i].phase += kk*(index-24)*P_CHANGE
                elif index>=38 and index<=41:
                    arr[i].phase += kk*(index-42)*P_CHANGE
                elif index>=51 and index<=56:
                    arr[i].phase += kk*(54-index)*P_CHANGE
                elif index>=49 and index<=50:
                    arr[i].phase += kk*(index-48)*P_CHANGE
                elif index>=58 and index<=59:
                    arr[i].phase += kk*(60-index)*P_CHANGE
                else:
                    arr[i].phase = 0
                    arr[i].inUse = 0

                arr[i].duty = 1250

        mysendArray.write()
        time.sleep(TIME_BREAK)
        # kk+=1
        if right_flag:
            kk+=1
        else:
            kk-=1
        if kk==3:
            right_flag = False


        # ba run.py bing guo lai
            # host socket
        # @param[in] AF_UNIX:AF_Local, base on the local
        # @param[in] AF_NETLINK:linux operating system support socket
        # @param[in] AF_INET:base on IPV4 network TCP/UDP socket
        # @param[in] AF_INET6:base on IPV6 network TCP/UDP socket
        # establish socket
        hostname = "192.168.3.2"  # server ip address
        port = 1024  # server port number
        log.info("Target IP address: {:s} \t port: {:d}".format(hostname, port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, port))  # connet socket

        # config_file = "etc/config.csv"
        # log.info("Try a configuration file: {:s}...".format(config_file))
        # HvCntl(CommandInterpret(s), config_file).send_all_config()
        
        config_file = "etc/config_array.csv"
        log.info("Try a configuration file: {:s}...".format(config_file))
        
        control_inst = HvCntl(CommandInterpret(s), config_file)
        control_inst.send_all_config()
        control_inst.start_working()

        s.close()
        print('kk=%d\n'%(kk))
        if (kk == 1) and right_flag:# and rise_flag:
            print('time sleep 20 s ...\n')
            time.sleep(10)
            print("ready? ...\n")
            time.sleep(10)
            print("go! ...\n")
            time.sleep(3)
        else:
            time.sleep(TIME_BREAK)

    print('kk=%d break'%(kk))

if __name__ == "__main__":
    main()