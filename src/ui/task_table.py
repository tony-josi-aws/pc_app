import time
import logging
import threading
from random import randrange
from datetime import datetime

from PyQt5 import QtCore

logger = logging.getLogger(__name__)


class KernelTask_TableHandler():

    def __init__(self, instant_resp_cmnd_handle, ui_table_widget) -> None:
        self.instant_resp_cmnd_handle = instant_resp_cmnd_handle
        self.ui_table_widget = ui_table_widget
        self.response_received = threading.Event()
        self.task_data = []

    def timer_callback(self):

        try:
            self.response_received.clear()
            self.instant_resp_cmnd_handle.issue_command("top", self.default_task_info_rx_callback)
            # Wait for the response.
            self.response_received.wait()
        except:
            pass

        if self.task_data != []:
            x = 0
            y = 0
            for task in self.task_data:
                for task_info in task:
                    self.ui_table_widget.setItem(x, y, task_info)
                    y += 1
                x += 1

        self.task_data = []

    def clear_table(self):
        for row in range(self.ui_table_widget.rowCount()):
            for col in range(self.ui_table_widget.columnCount()):
                self.ui_table_widget.setItem(row, col, 0)


    def default_task_info_rx_callback(self, response):
        if response is not None:
            try:
                str_resp = response.decode(encoding = 'ascii')
                self.task_data = self.parse_task_info_data(str_resp)
                print(f"{str_resp}")
            except:
                print(response)
        else:
            print("Timed out while waiting for response!")
        # Signal the do_send function to return.
        self.response_received.set()

    def parse_task_info_data(self, str_data):
        # TODO: parse data
        return str_data