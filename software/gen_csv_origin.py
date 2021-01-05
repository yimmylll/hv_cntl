#!/usr/bin/env python3

import math

from lib.send_array import SendArray
from lib.send_element import SendElement
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

    # k = 1

    for index in range(num2Send):
        dist = calc_distance(index, mysendArray, tx, ty, tz)
        log.debug("index: {:d} \tdist: {:f}".format(index, dist))

        res = dist/wavelength - int(dist/wavelength)
        phase = (1 - res) * cycle

        arr[index].phase = int(phase)*0 + 100
        arr[index].duty = 1250
        # if (index>82) and (index<125):#下盖
        #     arr[index].phase = int(phase)*0 + 100 + 5*k
        # else:
        #     arr[index].phase = int(phase)*0 + 100 - 5*k

    mysendArray.write()


if __name__ == "__main__":
    main()
