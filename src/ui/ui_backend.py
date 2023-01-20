import math
import time
import logging
import threading

from PyQt5.QtCore import QObject, QTimer
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget

from communication_utils.comm_agent import CommAgent
from communication_utils.udp_socket_interface import UDPSocket_CommInterface

from ui import netstat_plot, task_table, pcap_handler

from utils.network_stats_deserializer import deserialize_network_stats
from utils.kernel_stats_deserializer import deserialize_kernel_stats
class PC_App_Handler(QObject):
    command_completed_signal = QtCore.pyqtSignal(object)

    def __init__(self, main_window_h) -> None:
        super(PC_App_Handler, self).__init__()
        self.main_window = main_window_h
        self.comm_interface = None
        self.comm_agent = None

        # Init plots widget
        self.net_stat_plot_h = netstat_plot.NetStat_MainWindowPlotter(self.main_window.plot_netstat)
        self.disable_buttons_before_connect()

        # Connect available signals to the callbacks.
        self.connect_pyqt_main_window_signals()

        # Connect this handler's signals to the slots.
        self.connect_local_signals()

    def connect_pyqt_main_window_signals(self):
        self.main_window.pb_connect.clicked.connect(self.pb_connect_clicked)
        self.main_window.pb_disconnect.clicked.connect(self.pb_disconnect_clicked)
        self.main_window.pb_send_cmnd.clicked.connect(self.pb_send_command_clicked)
        self.main_window.pb_clear_cli.clicked.connect(self.pb_clear_cli_clicked)
        self.main_window.pb_stop_pcap.clicked.connect(self.pb_stop_pcap_callback)
        self.main_window.pb_start_pcap.clicked.connect(self.pb_start_pcap_callback)
        self.main_window.pb_download_pcap.clicked.connect(self.pb_download_pcap_callback)

    def connect_local_signals(self):
        self.command_completed_signal.connect(self.command_completed_slot)

    def pb_connect_clicked(self):
        device_ip = str(self.main_window.le_ip_addres.text())
        device_port = str(self.main_window.le_port_num.text())
        self.comm_interface = UDPSocket_CommInterface(device_ip, device_port)
        self.comm_agent = CommAgent(self.comm_interface)
        self.comm_agent.start_command_processing()

        if self.comm_agent != None:
            self.enable_buttons_after_connect()

            self.net_stat_cmnd_h = netstat_plot.NetStatStream(self.comm_agent, self.net_stat_plot_h)
            self.net_stat_plot_timer = QTimer()
            self.net_stat_plot_timer.timeout.connect(self.net_stat_cmnd_h.timer_callback)
            self.net_stat_plot_timer.start(1000)

            self.task_info_h = task_table.KernelTask_TableHandler(self.comm_agent, self.main_window.tw_task_info)
            self.task_info_table_timer = QTimer()
            self.task_info_table_timer.timeout.connect(self.task_info_h.timer_callback)
            self.task_info_table_timer.start(1000)

            self.pcap_h = pcap_handler.Pcap_Handler(self.comm_agent, self.main_window)

    def pb_disconnect_clicked(self):
        if self.comm_agent is not None:
            self.comm_agent.stop_command_processing()
            self.comm_interface.close_interface()
            self.comm_interface = None
            self.comm_agent = None
            self.disable_buttons_before_connect()

            # Stop timers
            self.net_stat_plot_timer.stop()
            self.task_info_table_timer.stop()

    def pb_send_command_clicked(self):
        command = str(self.main_window.cli_stdin.text())
        command = command.strip()
        if command:
            if command == "top":
                self.comm_agent.issue_command(command, self.top_command_completed_callback)
            elif command == "netstat":
                self.comm_agent.issue_command(command, self.netstat_command_completed_callback)
            else:
                self.comm_agent.issue_command(command, self.command_completed_callback)

    def command_completed_slot(self, str_resp):
        self.main_window.cli_stdout.append(str_resp)
        self.main_window.cli_stdout.append("\n------------------------\n")

    # This callback runs in the comm agent thread's context and therefore, must
    # not manipulate the UI.
    def command_completed_callback(self, response):
        if response is not None:
            try:
                str_resp = response.decode(encoding = 'ascii')
            except:
                str_resp = "Non-Printable response!"
        else:
            str_resp = "Timed out while waiting for response!"
        self.command_completed_signal.emit(str_resp)

    # This callback runs in the comm agent thread's context and therefore, must
    # not manipulate the UI.
    def netstat_command_completed_callback(self, response):
        if response is not None:
            try:
                ascii_resp = response.decode(encoding = 'ascii')
                deserialized_stats = deserialize_network_stats(ascii_resp)
                str_resp = str(deserialized_stats.get_simple_formatted_table())
            except:
                str_resp = "Non-Printable response!"
        else:
            str_resp = "Timed out while waiting for response!"
        self.command_completed_signal.emit(str_resp)

    # This callback runs in the comm agent thread's context and therefore, must
    # not manipulate the UI.
    def top_command_completed_callback(self, response):
        if response is not None:
            try:
                ascii_resp = response.decode(encoding = 'ascii')
                deserialized_stats = deserialize_kernel_stats(ascii_resp)
                str_resp = str(deserialized_stats.get_simple_formatted_table())
            except:
                str_resp = "Non-Printable response!"
        else:
            str_resp = "Timed out while waiting for response!"
        self.command_completed_signal.emit(str_resp)

    def pb_clear_cli_clicked(self):
        self.main_window.cli_stdout.clear()

    def pb_download_pcap_clicked(self):
        file_path = self.get_write_filepath_for_pcap()

    def get_write_filepath_for_pcap(self):
        pcap_file_path_dialog = QtWidgets.QFileDialog()
        pcap_file_path = pcap_file_path_dialog.getSaveFileName(filter="All Files(*.pcap);;Text Files(*.pcap)")
        pcap_file_path = pcap_file_path[0]
        return pcap_file_path

    def disable_buttons_before_connect(self):
        self.main_window.le_ip_addres.setEnabled(True)
        self.main_window.le_port_num.setEnabled(True)
        self.main_window.pb_connect.setEnabled(True)
        self.main_window.pb_disconnect.setEnabled(False)
        self.main_window.pb_send_cmnd.setEnabled(False)
        self.main_window.pb_clear_cli.setEnabled(False)
        self.main_window.pb_stop_pcap.setEnabled(False)
        self.main_window.pb_start_pcap.setEnabled(False)
        self.main_window.pb_download_pcap.setEnabled(False)
        self.main_window.tw_task_info.setEnabled(False)
        self.main_window.plot_netstat.setEnabled(False)
        self.main_window.cli_stdout.setEnabled(False)
        self.main_window.cli_stdin.setEnabled(False)

    def enable_buttons_after_connect(self):
        self.main_window.le_ip_addres.setEnabled(False)
        self.main_window.le_port_num.setEnabled(False)
        self.main_window.pb_connect.setEnabled(False)
        self.main_window.pb_disconnect.setEnabled(True)
        self.main_window.pb_send_cmnd.setEnabled(True)
        self.main_window.pb_clear_cli.setEnabled(True)
        self.main_window.pb_stop_pcap.setEnabled(True)
        self.main_window.pb_start_pcap.setEnabled(True)
        self.main_window.pb_download_pcap.setEnabled(True)
        self.main_window.tw_task_info.setEnabled(True)
        self.main_window.plot_netstat.setEnabled(True)
        self.main_window.cli_stdout.setEnabled(True)
        self.main_window.cli_stdin.setEnabled(True)

    def pb_start_pcap_callback(self):
        self.pcap_h.send_pcap_start()

    def pb_stop_pcap_callback(self):
        self.pcap_h.send_pcap_stop()

    def pb_download_pcap_callback(self):
        f_path = self.get_write_filepath_for_pcap()
        self.pcap_h.pcap_set_download_file_path(f_path)
        self.pcap_h.send_pcap_download()