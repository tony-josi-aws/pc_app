import time
import random
import logging
import threading
from random import randrange
from datetime import datetime

from ui.dialog_box import AppDialogBox

import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets
from utils.core_dump_parser import core_dump_parser

logger = logging.getLogger(__name__)

class Coredump_Handler(QtCore.QObject):

    coredump_command_completed_signal = QtCore.pyqtSignal()
    coredump_command_check_clear_completed_signal = QtCore.pyqtSignal()

    def __init__(self, comm_agent, main_win_handle) -> None:
        super(Coredump_Handler, self).__init__()
        self.comm_agent = comm_agent
        self.main_win_handle = main_win_handle
        self.coredump_command_completed_signal.connect(self.coredump_command_completed_slot)
        self.coredump_command_check_clear_completed_signal.connect(self.coredump_command_check_clear_completed_slot)
        self.core_dump_data = ""
        self.parsed_file_path = ""
        self.info_prefix_cmnd = ""
        self.file_path = None

    def coredump_command_completed_slot(self):

        dialog_bx_obj = AppDialogBox(self.main_win_handle.pyqt_main_window)
        dialog_bx_obj.show_dialog(self.info_prefix_cmnd, self.core_dump_data)

        self.info_prefix_cmnd = ""
        self.core_dump_data = ""

    def coredump_command_check_clear_completed_slot(self):

        self.main_win_handle.main_window.l_coredump_status.setText("{}".format(self.core_dump_data))
        self.info_prefix_cmnd = ""
        self.core_dump_data = ""

    def coredump_command_check(self):
        self.info_prefix_cmnd = "COREDUMP CHECK"
        self.comm_agent.issue_command("coredump check", self.coredump_command_check_completed_callback)

    # This callback runs in the comm agent thread's context and therefore, must
    # not manipulate the UI.
    def coredump_command_check_completed_callback(self, response):
        #self.main_win_handle.l_coredump_status.setText("")

        if response is not None:
            try:
                str_resp = response.decode(encoding = 'ascii')

                if str_resp == "Coredump exists.":
                    self.core_dump_data = "{}: {}".format(self.info_prefix_cmnd, "Coredump exists")
                    self.main_win_handle.main_window.pb_coredump_clean.setEnabled(True)
                    self.main_win_handle.main_window.pb_coredump_download.setEnabled(True)
                    #self.main_win_handle.l_coredump_status.setText("{}: {}".format(self.info_prefix_cmnd, "Dump Available"))
                else:
                    self.core_dump_data = "{}: {}".format(self.info_prefix_cmnd, "No coredump exist")
                    self.main_win_handle.main_window.pb_coredump_clean.setEnabled(False)
                    self.main_win_handle.main_window.pb_coredump_download.setEnabled(False)
                    #self.main_win_handle.l_coredump_status.setText("{}: {}".format(self.info_prefix_cmnd, "Dump Not Available"))

                self.coredump_command_check_clear_completed_signal.emit()
            except:
                pass

    def coredump_set_download_file_path(self, path):
        self.parsed_file_path = path
        self.file_path = self.parsed_file_path + ".tmp"

    def coredump_command_get(self):
        self.info_prefix_cmnd = "COREDUMP GET"
        self.comm_agent.issue_command("coredump get", self.coredump_command_get_completed_callback)

    def coredump_command_get_completed_callback(self, response):
        if response is not None:
            file_pth = ""
            if self.file_path is not None:
                file_pth = self.file_path
            else:
                tmp_file_name = str(hex(random.getrandbits(64)))
                tmp_file_name = tmp_file_name[2:]
                tmp_file_name += ".tmp"
                file_pth = tmp_file_name

        with open(file_pth, 'wb') as f:
            f.write(response)

        self.parse_dump(file_pth, self.parsed_file_path)
        # self.main_win_handle.l_coredump_status.setText("{}: {}".format(self.info_prefix_cmnd, "Generated dump file: {}".format(self.parsed_file_path)))
        self.core_dump_data = "Generated dump file: {}".format(self.parsed_file_path)
        self.coredump_command_completed_signal.emit()

    def parse_dump(self, src_file, dest_file):
        parser = core_dump_parser()
        parsed_file_path = parser.parse_core_dump( src_file, dest_file )

    def coredump_command_clean(self):
        self.info_prefix_cmnd = "COREDUMP REMOVE"
        self.comm_agent.issue_command("coredump remove", self.coredump_command_remove_completed_callback)

    def coredump_command_remove_completed_callback(self, response):
        # self.main_win_handle.l_coredump_status.setText("{}: {}".format(self.info_prefix_cmnd, "Finish"))
        self.core_dump_data = "{}: {}".format(self.info_prefix_cmnd, "remove")
        self.coredump_command_check_clear_completed_signal.emit()
