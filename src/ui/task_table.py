import logging
from PyQt5.QtCore import QObject
from PyQt5 import QtCore, QtWidgets
from utils.kernel_stats_deserializer import deserialize_kernel_stats

logger = logging.getLogger(__name__)


class KernelTask_TableHandler(QObject):

    top_command_completed_signal = QtCore.pyqtSignal()

    def __init__(self, comm_agent, ui_table_widget) -> None:
        super(KernelTask_TableHandler, self).__init__()
        self.comm_agent = comm_agent
        self.ui_table_widget = ui_table_widget
        self.top_command_completed_signal.connect(self.top_command_completed_slot)
        self.task_data = []

    def timer_callback(self):
        self.comm_agent.issue_command("top", self.top_command_completed_callback)

    def top_command_completed_slot(self):
        if self.task_data:
            self.ui_table_widget.setRowCount(len(self.task_data))
            x = 0
            for task in self.task_data:
                y = 0
                for task_info in task:
                    self.ui_table_widget.setItem(x, y, QtWidgets.QTableWidgetItem(task_info))
                    y += 1
                x += 1

        self.task_data = []

    # This callback runs in the comm agent thread's context and therefore, must
    # not manipulate the UI.
    def top_command_completed_callback(self, response):
        if response is not None:
            try:
                str_resp = response.decode(encoding = 'ascii')
                deserialized_kernel_stats = deserialize_kernel_stats(str_resp)
                self.task_data = deserialized_kernel_stats.get_all_task_stats()
                print(self.task_data)
                self.top_command_completed_signal.emit()
            except:
                pass
