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

class Exception_Handler(QtCore.QObject):

    exception_command_completed_signal = QtCore.pyqtSignal()

    def __init__(self, comm_agent, main_win_handle) -> None:
        super(Exception_Handler, self).__init__()
        self.comm_agent = comm_agent
        self.main_win_handle = main_win_handle
        self.exception_command_completed_signal.connect(self.exception_command_completed_slot)

    def exception_command_completed_slot(self):
        self.main_win_handle.l_pcap_status.setText("{}: {}".format(self.info_prefix_cmnd, self.pcap_data))
        self.info_prefix_cmnd = ""

    def exception_command_check(self):
        self.info_prefix_cmnd = "EXCEPTION CHECK"
        self.comm_agent.issue_command("exception check", self.exception_command_check_completed_callback)
        print("exception_command_check")

    # This callback runs in the comm agent thread's context and therefore, must
    # not manipulate the UI.
    def exception_command_check_completed_callback(self, response):
        self.main_win_handle.l_exception_status.setText("")

        if response is not None:
            try:
                str_resp = response.decode(encoding = 'ascii')

                if str_resp == "TRUE":
                    self.main_win_handle.l_exception_status.setText("{}: {}".format(self.info_prefix_cmnd, "Dump Available"))
                else:
                    self.main_win_handle.l_exception_status.setText("{}: {}".format(self.info_prefix_cmnd, "Dump Not Available"))
                
                self.exception_command_completed_signal.emit()
            except:
                pass

    def exception_command_assert(self):
        self.info_prefix_cmnd = "EXCEPTION ASSERT"
        self.comm_agent.issue_command("exception assert", self.exception_command_assert_completed_callback)
        print("exception_command_assert")

    # This callback runs in the comm agent thread's context and therefore, must
    # not manipulate the UI.
    def exception_command_assert_completed_callback(self, response):
        if response is not None:
            try:
                str_resp = response.decode(encoding = 'ascii')
                self.main_win_handle.l_exception_status.setText("{}: {}".format(self.info_prefix_cmnd, str_resp))
                self.exception_command_completed_signal.emit()
            except:
                pass

    def exception_command_dump(self):
        self.info_prefix_cmnd = "EXCEPTION DUMP"
        self.comm_agent.issue_command("exception dump", self.exception_command_dump_completed_callback)
        print("exception_command_dump")

    def exception_command_dump_completed_callback(self, response):
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

        self.dump_data = "Generated dump file: {}".format(file_pth)

        self.parse_dump(file_pth)

        self.main_win_handle.l_exception_status.setText("{}: {}".format(self.info_prefix_cmnd, "Finish"))
        self.exception_command_completed_signal.emit()
    
    def parse_dump(self, file):
        parser = core_dump_parser()
        parsed_file_path = parser.parse_core_dump( file )

    def exceotion_set_download_file_path(self, path):
        self.file_path = path

    def exception_command_clean(self):
        self.info_prefix_cmnd = "EXCEPTION CLEAN"
        self.comm_agent.issue_command("exception clean", self.exception_command_clean_completed_callback)
        print("exception_command_dump")

    def exception_command_clean_completed_callback(self, response):
        self.main_win_handle.l_exception_status.setText("{}: {}".format(self.info_prefix_cmnd, "Finish"))
        self.exception_command_completed_signal.emit()
