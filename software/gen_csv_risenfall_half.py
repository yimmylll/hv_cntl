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

# element相关
cycle=2500
gap=0.0105    #unit: meter
soundSpeed=340 #unit: meter per second
freq=40000 #unit: Hz
wavelength=soundSpeed/freq

# socket相关
hostname = "192.168.3.2"  # server ip address
port = 1024  # server port number
config_file = "etc/config_array.csv"


def calc_distance(index, send_array, tx,ty,tz):
    return math.sqrt(pow(send_array._array[index].x-tx, 2) + pow(send_array._array[index].y-ty,2)+ pow(send_array._array[index].z-tz,2))

def main():
    num2Send=200
    arr = []

    k = 0
    P_CHANGE = 90#221
    P_FIRST = 100
    TIME_BREAK = 0.4#SECOND
    rise_flag = True

    # 把new_element配置好，并逐个放入arr
    for i in range(num2Send):
        ########### only for test ############
        # if i>=118 and i<=199:
        # if i==31:
        #     inUse = 1
        # else:
        #     inUse = 0
        #######################

        # 初始化元素
        new_element = SendElement()

        # 初始化new_element的编号
        # --由于有的端口是坏的，所以本来应该按顺序的
        # --注意硬件端口号与软件编号不同
        if i == 66:
            new_element.order = 33
        elif i == 68:
            new_element.order = 57
        elif i == 67:
            new_element.order = 48
        # --这几次扫描的没有对应的超声探头：33 57 48
        # --所以把它们的编号空出来让给别人
        elif i == 33 or i == 57 or i==48:##ill port
            new_element.order = num2Send+1#disable
        else:
            new_element.order = i


        # 初始化一半工作
        index = new_element.order
        if index>=72 and index<=117 and (index % 2) == 0:#xia gai
            inUse = 1
        elif index>=60 and index<=65 and (index % 2) == 0:
            inUse = 1
        elif index>=49 and index<=59 and (index % 2) == 1:
            inUse = 1
        elif index>=24 and index<=41 and (index % 2) == 0:
            inUse = 1
        else:
            inUse = 0
        new_element.inUse = inUse

         # 初始化new_element的初相位
        new_element.phase = P_FIRST

        # 初始化new_element的高电平时间
        new_element.duty = 1250
        
        new_element.x = (int(i/ARRAY_LENGTH)%ARRAY_LENGTH)*gap
        new_element.y = int(i%ARRAY_LENGTH) *gap
        new_element.z = 0

        # 放入arr
        arr.append(new_element)
        
        # tmp = [5, 6, 8, 15, 21, 49]
        # for i, j in zip(tmp, range(len(tmp))):
        #     #arr[i-1].order = 7 * 12 + j
        #     log.debug("new order: {}".format(arr[i-1].order))


    # tx=gap*2 
    # ty=gap*2  #unit: meter
    # tz=0.03 #unit: meter

    # 初始化mysendArray
    mysendArray = SendArray(num2Send, arr)
    # 初始配置写入csv文件
    mysendArray.write()

        # while k < 1:#for test
    while k != -1:# while k != -6:
        for i in range(num2Send):
            # dist = calc_distance(i, mysendArray, tx, ty, tz)
            # log.debug("i: {:d} \tdist: {:f}".format(i, dist))

            # res = dist/wavelength - int(dist/wavelength)
            # phase = (1 - res) * cycle

            index = arr[i].order

            # 根据软件编号来确定上下盖的相位变化
            if (index>=72) and (index<=89):
                arr[i].phase = int(phase)*0 + P_FIRST - P_CHANGE*k
            elif (index>=96) and (index<=97):
                arr[i].phase = int(phase)*0 + P_FIRST - P_CHANGE*k
            elif (index>=102) and (index<=117):
                arr[i].phase = int(phase)*0 + P_FIRST - P_CHANGE*k
            else:
                arr[i].phase = int(phase)*0 + P_FIRST + P_CHANGE*k
                # arr[index].phase = int(phase)*0 + P_FIRST

        # 修改相位后的mysendArray数据逐行写入CSV文件
        mysendArray.write()
        # time.sleep(TIME_BREAK)

        # rise_flag用于展示上升、下降
        if rise_flag:
            k+=1
        else:
            k-=1
        if k==10:
            rise_flag = False

        # 建立通信，把配置发过去
        # ...to do 是否可以不在循环里每次都

        # ba run.py bing guo lai
            # host socket
        # @param[in] AF_UNIX:AF_Local, base on the local
        # @param[in] AF_NETLINK:linux operating system support socket
        # @param[in] AF_INET:base on IPV4 network TCP/UDP socket
        # @param[in] AF_INET6:base on IPV6 network TCP/UDP socket
        # establish socket
        log.info("Target IP address: {:s} \t port: {:d}".format(hostname, port))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, port))  # connet socket

        # config_file = "etc/config.csv"
        # log.info("Try a configuration file: {:s}...".format(config_file))
        # HvCntl(CommandInterpret(s), config_file).send_all_config()
        log.info("Try a configuration file: {:s}...".format(config_file))
        
        control_inst = HvCntl(CommandInterpret(s), config_file)
        control_inst.send_all_config()
        control_inst.start_working()

        s.close()

        print('k=%d\n'%(k))

        # 开始延时久一点，便于把泡沫球放进去
        if (k == 1) and rise_flag:
            print('time sleep 20 s ...\n')
            time.sleep(10)
            print("ready? ...\n")
            time.sleep(10)
            print("go! ...\n")
            time.sleep(3)
        else:
            time.sleep(TIME_BREAK)

    print('k=%d break'%(k))

if __name__ == "__main__":
    main()