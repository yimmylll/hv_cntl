import os
import sys
import time
import socket

import logging
import coloredlogs

from lib.command_interpret import CommandInterpret
from lib.hv_cntl import HvCntl

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
coloredlogs.install(level='DEBUG', logger=log)


class Location:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class Direction:
    def __init__(self, vx, vy, vz):
        self.vx = vx
        self.vy = vy
        self.vz = vz


class SendElement:
    def __init__(self, inUse=0, order=0, phase=0, duty=0, duration=0, amp=0, x=0, y=0, z=0, vx=0, vy=0, vz=0):
        self.inUse = inUse
        self.order = order
        self.phase = phase
        self.duty = duty
        self.duration = duration
        self.amp = amp
        self.location = Location(x, y, z)
        self.direction = Direction(vx, vy, vz)
