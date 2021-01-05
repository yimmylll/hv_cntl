import csv
import logging
import coloredlogs

from lib.defines import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
coloredlogs.install(level='INFO', logger=log)


class HvCntl:
    def __init__(self, cmd_parse, config_file):
        self._cmd_parse = cmd_parse
        self._config_file = config_file

    def w_en(self):
        """ Write enable """
        log.debug("Write enable")
        self._cmd_parse.write_pulse_reg(0x0001)

    def start_working(self):
        log.debug("Start working...")
        self._cmd_parse.write_pulse_reg(0x0002)

    def send_one_config(self, config):
        """ Send one configuration to FPGA FIFO
        @param head + delay_cnt + work_cnt
        """
        
        ch_en = int(config[0])
        order = int(config[1])
        delay_cnt = int(config[2])
        duty_cnt = int(config[3])
    
        config_data = (ch_en << 47) | (delay_cnt << 12) + duty_cnt
        # config_data_reg = config_data
        log.debug("addr: {:d} config: {:#x}".format(order, config_data))
        
        """ send address """
        self._cmd_parse.write_config_reg(3, order)
        read_addr = self._cmd_parse.read_config_reg(3)
        if read_addr != order:
            log.error("read addr: {} is not equal send addr {}".format(read_addr, order))
        
        """ send config """
        read_config = 0
        for i in range(3):
            reg_data = config_data & 0xFFFF
            config_data = config_data >> 16
            self._cmd_parse.write_config_reg(i, reg_data)
            read_config = (read_config<<16) + self._cmd_parse.read_config_reg(i)
            log.debug("Read data {0:d}: {1:#04x}".format(i, self._cmd_parse.read_config_reg(i)))

        # if read_config != config_data:
        #     log.error("read config: {:#012x} is not equal send config {:#012x}".format(read_config, config_data_reg))

        """ send write enable """
        self.w_en()


    def send_all_config(self):
        """ Send all configuration to FPGA FIFO """
        with open(self._config_file, newline='') as csvfile:
            config_reader = csv.reader(csvfile, delimiter=' ', quotechar=' ')
            for config in config_reader:
                self.send_one_config(config)

