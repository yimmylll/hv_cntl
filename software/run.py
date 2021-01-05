#!/usr/bin/env python3

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


def main():
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

if __name__ == "__main__":
    main()
