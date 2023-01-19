import math
import time
import logging

from PyQt5.QtCore import QObject
from PyQt5 import QtCore, QtWidgets

class PC_App_Handler(QObject):

    def __init__(self, main_window_h) -> None:
        super(PC_App_Handler, self).__init__()
        self.main_window = main_window_h

        """ Connect available signals to the callbacks. """
        self.connect_pyqt_main_window_signals()

    def connect_pyqt_main_window_signals(self):
        self.main_window.pb_connect.clicked.connect(self.pb_connect_device_cb)
        self.main_window.pb_disconnect.clicked.connect(self.pb_connect_device_cb)
        self.main_window.pb_send_cmnd.clicked.connect(self.pb_connect_device_cb)

    def pb_connect_device_cb(self):
        print("Connect")