import csv

import logging
import coloredlogs

from lib.command_interpret import CommandInterpret
from lib.hv_cntl import HvCntl

from lib.send_element import SendElement

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
coloredlogs.install(level='DEBUG', logger=log)


class SendArray:
    def __init__(self, num=0, array=None):
        # self.order = order
        self._num = num
        self._array = array
        self.config_file = "./etc/config_array.csv"
        log.debug("num: {} num_of_arr: {}".format(self._num, len(self._array)))

    def write(self):
        with open(self.config_file, 'w+', newline='') as csvfile:
            config_writer = csv.writer(
                csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            for i in range(self._num):
                config_writer.writerow(
                    [self._array[i].inUse, self._array[i].order, self._array[i].phase, self._array[i].duty])
