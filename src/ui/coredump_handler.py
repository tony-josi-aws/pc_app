import time
import random
import logging
import threading
from random import randrange
from datetime import datetime

import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from utils.core_dump_parser import core_dump_parser

logger = logging.getLogger(__name__)

class Coredump_Handler(QtCore.QObject):

    coredump_command_completed_signal = QtCore.pyqtSignal()

    def __init__(self, comm_agent, main_win_handle) -> None:
        super(Coredump_Handler, self).__init__()
        self.comm_agent = comm_agent
        self.main_win_handle = main_win_handle
        self.coredump_command_completed_signal.connect(self.coredump_command_completed_slot)
        self.parsed_file_path = ""

    def coredump_command_completed_slot(self):
        self.main_win_handle.l_pcap_status.setText("{}: {}".format(self.info_prefix_cmnd, self.pcap_data))
        self.info_prefix_cmnd = ""

    def coredump_command_check(self):
        self.info_prefix_cmnd = "COREDUMP CHECK"
        self.comm_agent.issue_command("coredump check", self.coredump_command_check_completed_callback)

    # This callback runs in the comm agent thread's context and therefore, must
    # not manipulate the UI.
    def coredump_command_check_completed_callback(self, response):
        self.main_win_handle.l_coredump_status.setText("")

        if response is not None:
            try:
                str_resp = response.decode(encoding = 'ascii')

                if str_resp == "TRUE":
                    self.main_win_handle.l_coredump_status.setText("{}: {}".format(self.info_prefix_cmnd, "Dump Available"))
                else:
                    self.main_win_handle.l_coredump_status.setText("{}: {}".format(self.info_prefix_cmnd, "Dump Not Available"))
                
                self.coredump_command_completed_signal.emit()
            except:
                pass
    
    def coredump_set_download_file_path(self, path):
        self.parsed_file_path = path

    def coredump_command_get(self):
        self.info_prefix_cmnd = "COREDUMP GET"
        self.comm_agent.issue_command("coredump get", self.coredump_command_get_completed_callback)

    def coredump_command_get_completed_callback(self, response):
        if response is not None:
            file_pth = ""
            if self.file_path is not None:
                file_pth = self.file_path
            else:
                dump_file_name = str(hex(random.getrandbits(64)))
                dump_file_name = dump_file_name[2:]
                dump_file_name += ".dump"
                file_pth = dump_file_name

        with open(file_pth, 'wb') as f:
            f.write(response)

        self.parse_dump(file_pth, self.parsed_file_path)
        self.main_win_handle.l_coredump_status.setText("{}: {}".format(self.info_prefix_cmnd, "Generated dump file: {}".format(self.parsed_file_path)))
        self.coredump_command_completed_signal.emit()
    
    def parse_dump(self, src_file, dest_file):
        parser = core_dump_parser()
        parsed_file_path = parser.parse_core_dump( src_file, dest_file )

    def exceotion_set_download_file_path(self, path):
        self.file_path = path

    def coredump_command_clean(self):
        self.info_prefix_cmnd = "COREDUMP CLEAN"
        self.comm_agent.issue_command("coredump clean", self.coredump_command_clean_completed_callback)

    def coredump_command_clean_completed_callback(self, response):
        self.main_win_handle.l_coredump_status.setText("{}: {}".format(self.info_prefix_cmnd, "Finish"))
        self.coredump_command_completed_signal.emit()
