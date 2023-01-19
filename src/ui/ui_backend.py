import math
import time
import logging
import threading

from PyQt5.QtCore import QObject, QTimer
from PyQt5 import QtCore, QtWidgets

from communication_utils.comm_agent import CommAgent
from communication_utils.udp_socket_interface import UDPSocket_CommInterface

from ui import netstat_plot, task_table

class PC_App_Handler(QObject):
    command_completed_signal = QtCore.pyqtSignal(object)

    def __init__(self, main_window_h) -> None:
        super(PC_App_Handler, self).__init__()
        self.main_window = main_window_h
        self.comm_interface = None
        self.comm_agent = None

        # Init plots widget
        self.net_stat_plot_h = netstat_plot.NetStat_MainWindowPlotter(self.main_window.plot_netstat)

        # Connect available signals to the callbacks.
        self.connect_pyqt_main_window_signals()

        # Connect this handler's signals to the slots.
        self.connect_local_signals()

    def connect_pyqt_main_window_signals(self):
        self.main_window.pb_connect.clicked.connect(self.pb_connect_clicked)
        self.main_window.pb_disconnect.clicked.connect(self.pb_disconnect_clicked)
        self.main_window.pb_send_cmnd.clicked.connect(self.pb_send_command_clicked)
        self.main_window.pb_clear.clicked.connect(self.pb_plot_clear_clicked)
        self.main_window.pb_reset.clicked.connect(self.pb_plot_reset_clicked)
        self.main_window.pb_clear_cli.clicked.connect(self.pb_clear_cli_clicked)

    def connect_local_signals(self):
        self.command_completed_signal.connect(self.command_completed_slot)

    def pb_connect_clicked(self):
        device_ip = str(self.main_window.le_ip_addres.text())
        device_port = str(self.main_window.le_port_num.text())
        self.comm_interface = UDPSocket_CommInterface(device_ip, device_port)
        self.comm_agent = CommAgent(self.comm_interface)
        self.comm_agent.start_command_processing()

        
        self.net_stat_cmnd_h = netstat_plot.NetStatStream(self.comm_agent, self.net_stat_plot_h)
        self.net_stat_plot_timer = QTimer()
        self.net_stat_plot_timer.timeout.connect(self.net_stat_cmnd_h.timer_callback)
        self.net_stat_plot_timer.start(500)

        self.task_info_h = task_table.KernelTask_TableHandler(self.comm_agent, self.net_stat_plot_h)
        self.task_info_table_timer = QTimer()
        self.task_info_table_timer.timeout.connect(self.task_info_h.timer_callback)
        self.task_info_table_timer.start(500)

    def pb_disconnect_clicked(self):
        if self.comm_agent is not None:
            self.comm_agent.stop_command_processing()
            self.comm_interface.close_interface()
            self.comm_interface = None
            self.comm_agent = None

            # Stop timers
            self.net_stat_plot_timer.stop()
            self.task_info_table_timer.stop()


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

    def pb_plot_clear_clicked(self):
        self.net_stat_plot_h.clear_plot_data()

    def pb_plot_reset_clicked(self):
        self.net_stat_plot_h.reset_plot()

    def pb_clear_cli_clicked(self):
        self.main_window.cli_stdout.clear()
