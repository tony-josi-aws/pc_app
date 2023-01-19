import math
import time
import logging
import threading

from PyQt5.QtCore import QObject, QTimer
from PyQt5 import QtCore, QtWidgets

from communication_utils.comm_agent import CommAgent
from communication_utils.udp_socket_interface import UDPSocket_CommInterface

from ui import netstat_plot

class PC_App_Handler(QObject):
    command_completed_signal = QtCore.pyqtSignal(object)

    def __init__(self, main_window_h) -> None:
        super(PC_App_Handler, self).__init__()
        self.main_window = main_window_h
        self.comm_interface = None
        self.comm_agent = None

        self.net_stat_plot_h = netstat_plot.NetStat_MainWindowPlotter(self.main_window.plot_netstat)
        self.net_stat_cmnd_h = netstat_plot.NetStatStream(self.comm_agent, self.net_stat_plot_h)
        self.timer = QTimer()
        self.timer.timeout.connect(self.net_stat_cmnd_h.timer_callback)
        self.timer.start(500)
        
        # Connect available signals to the callbacks.
        self.connect_pyqt_main_window_signals()

        # Connect this handler's signals to the slots.
        self.connect_local_signals()

    def connect_pyqt_main_window_signals(self):
        self.main_window.pb_connect.clicked.connect(self.pb_connect_clicked)
        self.main_window.pb_disconnect.clicked.connect(self.pb_disconnect_clicked)
        self.main_window.pb_send_cmnd.clicked.connect(self.pb_send_command_clicked)

    def connect_local_signals(self):
        self.command_completed_signal.connect(self.command_completed_slot)

    def pb_connect_clicked(self):
        device_ip = str(self.main_window.le_ip_addres.text())
        device_port = str(self.main_window.le_port_num.text())
        self.comm_interface = UDPSocket_CommInterface(device_ip, device_port)
        self.comm_agent = CommAgent(self.comm_interface)
        self.comm_agent.start_command_processing()

    def pb_disconnect_clicked(self):
        if self.comm_agent is not None:
            self.comm_agent.stop_command_processing()
            self.comm_interface.close_interface()
            self.comm_interface = None
            self.comm_agent = None

    def pb_send_command_clicked(self):
        command = str(self.main_window.cli_stdin.text())
        command = command.strip()
        if command:
            self.comm_agent.issue_command(command, self.command_completed_callback)

    def command_completed_slot(self, response):
        if response is not None:
            try:
                str_resp = response.decode(encoding = 'ascii')
            except:
                str_resp = "Non-Printable response!"
        else:
            str_resp = "Timed out while waiting for response!"

        self.main_window.cli_stdout.append(str_resp)

    # This callback runs in the comm agent thread's context and therefore, must
    # not manipulate the UI.
    def command_completed_callback(self, response):
        self.command_completed_signal.emit(response)
