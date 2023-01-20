
import time
import random
import logging
import threading
from random import randrange
from datetime import datetime

import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets

logger = logging.getLogger(__name__)

class Pcap_Handler(QtCore.QObject):

    pcap_command_completed_signal = QtCore.pyqtSignal()

    def __init__(self, comm_agent, main_win_handle) -> None:
        super(Pcap_Handler, self).__init__()
        self.comm_agent = comm_agent
        self.main_win_handle = main_win_handle
        self.pcap_command_completed_signal.connect(self.pcap_command_completed_slot)
        self.pcap_data = ""
        self.file_path = None
        self.info_prefix_cmnd = ""
        logger.info("")

    def pcap_command_completed_slot(self):
        self.main_win_handle.l_pcap_status.setText("{}: {}".format(self.info_prefix_cmnd, self.pcap_data))
        self.info_prefix_cmnd = ""
        self.pcap_data = ""        

    def send_pcap_start(self):
        self.info_prefix_cmnd = "PCAP START"
        self.comm_agent.issue_command("pcap start", self.pcap_start_stop_command_completed_callback)

    def send_pcap_stop(self):
        self.info_prefix_cmnd = "PCAP STOP"
        self.comm_agent.issue_command("pcap stop", self.pcap_start_stop_command_completed_callback)

    def send_pcap_download(self):
        self.info_prefix_cmnd = "PCAP GET"
        self.comm_agent.issue_command("pcap get", self.pcap_download_command_completed_callback)

    # This callback runs in the comm agent thread's context and therefore, must
    # not manipulate the UI.
    def pcap_start_stop_command_completed_callback(self, response):
        if response is not None:
            try:
                str_resp = response.decode(encoding = 'ascii')
                self.pcap_data = str_resp
                self.pcap_command_completed_signal.emit()
            except:
                pass

    def pcap_download_command_completed_callback(self, response):
        if response is not None:
            file_pth = ""
            if self.file_path is not None:
                file_pth = self.file_path
            else:
                pcap_file_name = str(hex(random.getrandbits(64)))
                pcap_file_name = pcap_file_name[2:]
                pcap_file_name += ".pcap"
                file_pth = pcap_file_name

        with open(file_pth, 'wb') as f:
            f.write(response)

        self.pcap_data = "Generated PCAP dump file: {}".format(file_pth)
        self.pcap_command_completed_signal.emit()

    def pcap_set_download_file_path(self, path):
        self.file_path = path