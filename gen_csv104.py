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

    k = 0
    P_CHANGE = 80
    P_FIRST = 500
    TIME_BREAK = 0.5#SECOND
    while k < 10:
        for i in range(num2Send):
            if(i<50):
                inUse = 1
            else:
                inUse = 1

            phase = 0
            
            new_element = SendElement()
            new_element.inUse = inUse
            new_element.order = i
            new_element.x = (int(i/ARRAY_LENGTH)%ARRAY_LENGTH)*gap
            new_element.y = int(i%ARRAY_LENGTH) *gap
            new_element.z = 0


            arr.append(new_element)
        
        tmp = [5, 6, 8, 15, 21, 49]
        for i, j in zip(tmp, range(len(tmp))):
            #arr[i-1].order = 7 * 12 + j
            log.debug("new order: {}".format(arr[i-1].order))


        tx=gap*2 
        ty=gap*2  #unit: meter
        tz=0.03 #unit: meter

        mysendArray = SendArray(num2Send, arr)

        for index in range(num2Send):
            dist = calc_distance(index, mysendArray, tx, ty, tz)
            log.debug("index: {:d} \tdist: {:f}".format(index, dist))

            res = dist/wavelength - int(dist/wavelength)
            phase = (1 - res) * cycle

            if (index>82) and (index<125):
                arr[index].phase = int(phase)*0 + P_FIRST + P_CHANGE*k
            else:
                arr[index].phase = int(phase)*0 + P_FIRST - P_CHANGE*k
            arr[index].duty = 1250

        mysendArray.write()
        time.sleep(TIME_BREAK)
        k+=1
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
        print('k=%d\n'%(k))
        if int(k) is 1:
            print('time sleep 10 s ...\n')
            time.sleep(20)
            print("10s finish\n")
        else:
            time.sleep(TIME_BREAK)

    print('k=%d break'%(k))

if __name__ == "__main__":
    main()