
import time
import random
import logging
import threading
from random import randrange
from datetime import datetime

from ui.dialog_box import AppDialogBox

import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets

logger = logging.getLogger(__name__)

class Trace_Handler(QtCore.QObject):

    trace_command_completed_signal = QtCore.pyqtSignal()
    trace_command_start_stop_completed_signal = QtCore.pyqtSignal()

    def __init__(self, comm_agent, main_win_handle) -> None:
        super(Trace_Handler, self).__init__()
        self.comm_agent = comm_agent
        self.main_win_handle = main_win_handle
        self.trace_command_completed_signal.connect(self.trace_command_completed_slot)
        self.trace_command_start_stop_completed_signal.connect(self.trace_command_start_stop_completed_slot)
        self.trace_data = ""
        self.file_path = None
        self.info_prefix_cmnd = ""
        logger.info("")

    def trace_command_start_stop_completed_slot(self):
        self.main_win_handle.main_window.l_trace.setText("{}: {}".format(self.info_prefix_cmnd, self.trace_data))

    def trace_command_completed_slot(self):
        #self.main_win_handle.l_trace.setText("{}: {}".format(self.info_prefix_cmnd, self.trace_data))

        dialog_bx_obj = AppDialogBox(self.main_win_handle.pyqt_main_window)
        dialog_bx_obj.show_dialog(self.info_prefix_cmnd, self.trace_data)

        self.info_prefix_cmnd = ""
        self.trace_data = ""        

    def send_trace_start(self):
        self.info_prefix_cmnd = "TRACE START"
        self.comm_agent.issue_command("trace start", self.trace_start_stop_command_completed_callback)

    def send_trace_stop(self):
        self.info_prefix_cmnd = "TRACE STOP"
        self.comm_agent.issue_command("trace stop", self.trace_start_stop_command_completed_callback)

    def send_trace_download(self):
        self.info_prefix_cmnd = "TRACE GET"
        self.comm_agent.issue_command("trace get", self.trace_download_command_completed_callback)

    # This callback runs in the comm agent thread's context and therefore, must
    # not manipulate the UI.
    def trace_start_stop_command_completed_callback(self, response):
        if response is not None:
            try:
                str_resp = response.decode(encoding = 'ascii')
                self.trace_data = str_resp
                self.trace_command_start_stop_completed_signal.emit()
            except:
                pass

    def trace_download_command_completed_callback(self, response):
        if response is not None:
            file_pth = ""
            if self.file_path is not None:
                file_pth = self.file_path
            else:
                trace_file_name = str(hex(random.getrandbits(64)))
                trace_file_name = trace_file_name[2:]
                trace_file_name += ".trace"
                file_pth = trace_file_name

        with open(file_pth, 'wb') as f:
            f.write(response)

        self.trace_data = "Generated TRACE dump file: {}".format(file_pth)
        self.trace_command_completed_signal.emit()

    def trace_set_download_file_path(self, path):
        self.file_path = path