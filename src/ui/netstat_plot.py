
import time
import logging
import threading
from random import randrange
from datetime import datetime

import pyqtgraph as pg
from PyQt5 import QtCore, QtWidgets

from utils import network_stats_deserializer

DEFAULT_MAX_STREAM_TIME_PERIOD_SEC = 1

logger = logging.getLogger(__name__)

class NetStatStream(QtCore.QObject):

    netstat_command_completed_signal = QtCore.pyqtSignal()

    def __init__(self, instant_resp_cmnd_handle, plot_handle) -> None:
        self.instant_resp_cmnd_handle = instant_resp_cmnd_handle
        self.response_received = threading.Event()
        self.plot_handle = plot_handle
        self.netstat_command_completed_signal.connect(self.netstat_command_completed_slot)
        self.netstat_data = None
        logger.info("Init NetStatStream thread")

    def timer_callback(self):
        self.comm_agent.issue_command("netstat", self.netstat_command_completed_callback)

    def netstat_command_completed_slot(self):
        if self.netstat_data != None:
            self.plot_handle.update_plot_data(self.netstat_data.rx_latency, self.netstat_data.tx_latency)
            self.netstat_data = None

    # This callback runs in the comm agent thread's context and therefore, must
    # not manipulate the UI.
    def netstat_command_completed_callback(self, response):
        if response is not None:
            try:
                str_resp = response.decode(encoding = 'ascii')
                deserialized_kernel_stats = network_stats_deserializer.deserialize_network_stats(response)
                self.netstat_data = deserialized_kernel_stats.get_all_task_stats()
                self.netstat_command_completed_signal.emit()
            except:
                pass


NETSTAT_PLOT_COLOR = '#0099ff'
NETSTAT_PLOT_COLOR_RX_LATENCY_CURVE = '#0094d1'
NETSTAT_PLOT_COLOR_TX_LATENCY_CURVE = '#8b1ec9'
NETSTAT_PLOT_AXIS_LABEL_COLOR = '#000000'
NETSTAT_PLOT_AXIS_LABEL_FONT_SIZE = "10pt"
NETSTAT_PLOT_COLOR_LEFT_Y_AXIS_NAME =  "Latency (ms)"
DEFAULT_MAX_NETSTAT_PLOT_REAL_TIME_DATA = 40
NETSTAT_PLOT_COLOR_BOTTOM_X_AXIS_NAME =  "Time"
NETSTAT_PLOT_AXIS_LABEL_STYLE = {"label": "COLUMN 1", "color": (NETSTAT_PLOT_AXIS_LABEL_COLOR), "font-size": NETSTAT_PLOT_AXIS_LABEL_FONT_SIZE}
NETSTAT_PLOT_PERCENT_INDEX = 0

class NetStat_MainWindowPlotter:

    def __init__(self, ui_plot_widget) -> None:

        self.plot_x_axis_data = []
        self.plot_y_axis_data = []
        self.plot_y2_axis_data = []
        self.num_current_data_pts = 0
        self.is_plot_paused = False

        self.netstat_plot_plot_widget = ui_plot_widget
        self.netstat_plot_plot_item = self.netstat_plot_plot_widget.plotItem

        """ Set axis labels, and label & axis colors. """
        self.netstat_plot_plot_item.getAxis('left').setPen(pg.mkPen(color=(NETSTAT_PLOT_COLOR_RX_LATENCY_CURVE), width=2))
        self.netstat_plot_plot_item.getAxis('right').setPen(pg.mkPen(color=(NETSTAT_PLOT_COLOR_TX_LATENCY_CURVE), width=2))
        self.netstat_plot_plot_item.getAxis('bottom').setPen(pg.mkPen(color=(NETSTAT_PLOT_COLOR), width=2))
        self.netstat_plot_plot_item.setLabel('left', NETSTAT_PLOT_COLOR_LEFT_Y_AXIS_NAME, **NETSTAT_PLOT_AXIS_LABEL_STYLE)
        self.netstat_plot_plot_item.setLabel('bottom', NETSTAT_PLOT_COLOR_BOTTOM_X_AXIS_NAME, **NETSTAT_PLOT_AXIS_LABEL_STYLE) 

        self.netstat_plot_plot_item.showGrid(x = True, y = True, alpha = 0.1)

        """ Create two curves and add it to the plotWidget """
        self.netstat_plot_curve_item_rx_latency = pg.PlotCurveItem(pen=({'color': NETSTAT_PLOT_COLOR_RX_LATENCY_CURVE, 'width': 2}), skipFiniteCheck=True)
        self.netstat_plot_plot_widget.addItem(self.netstat_plot_curve_item_rx_latency)

        self.netstat_plot_view_box = pg.ViewBox()
        self.netstat_plot_plot_item.showAxis('right')
        self.netstat_plot_plot_item.scene().addItem(self.netstat_plot_view_box)
        self.netstat_plot_plot_item.getAxis('right').linkToView(self.netstat_plot_view_box)
        self.netstat_plot_view_box.setXLink(self.netstat_plot_plot_item)

        self.netstat_plot_curve_item_tx_latency = pg.PlotCurveItem(pen=({'color': NETSTAT_PLOT_COLOR_TX_LATENCY_CURVE, 'width': 2}), skipFiniteCheck=True)
        self.netstat_plot_view_box.addItem(self.netstat_plot_curve_item_tx_latency)

        self.updateViews_Graph1()
        self.netstat_plot_plot_item.vb.sigResized.connect(self.updateViews_Graph1)

        logger.info("Init plot")

    def updateViews_Graph1(self):
        self.netstat_plot_view_box.setGeometry(self.netstat_plot_plot_item.vb.sceneBoundingRect())
        self.netstat_plot_view_box.linkedViewChanged(self.netstat_plot_plot_item.vb, self.netstat_plot_view_box.XAxis)

    def append_stream_data_to_list(self, strm_data, strm_data2):

        self.plot_y_axis_data.append(strm_data if strm_data != None else 0)
        self.plot_y2_axis_data.append(strm_data2 if strm_data2 != None else 0)

        self.plot_x_axis_data.append(time.time())


    def parse_curve_data(self, strm_data, strm_data2):
        if self.num_current_data_pts < DEFAULT_MAX_NETSTAT_PLOT_REAL_TIME_DATA:
            self.append_stream_data_to_list(strm_data, strm_data2)
            self.num_current_data_pts += 1
        else:
            self.plot_x_axis_data = self.plot_x_axis_data[1:]
            self.plot_y_axis_data = self.plot_y_axis_data[1:]
            self.plot_y2_axis_data = self.plot_y2_axis_data[1:]
            self.append_stream_data_to_list(strm_data, strm_data2)

    def update_plot_data(self, tx, rx):

        """ 
        Parse the stream data from the Stream_Data object and plot
        it. 
        """
        try:
            if not self.is_plot_paused:
                self.parse_curve_data(tx, rx)
                self.netstat_plot_curve_item_rx_latency.setData(self.plot_x_axis_data[:self.num_current_data_pts], \
                    self.plot_y_axis_data[:self.num_current_data_pts])
                self.netstat_plot_curve_item_tx_latency.setData(self.plot_x_axis_data[:self.num_current_data_pts], \
                    self.plot_y2_axis_data[:self.num_current_data_pts])
        except:
            logger.error("Exception in append_stream_data_to_list: {}, {}".format(tx, rx))


    def clear_plot_data(self):

        """ Clear the plot data and clear the graph curve. """

        self.plot_x_axis_data = []
        self.plot_y_axis_data = []
        self.num_current_data_pts = 0
        self.netstat_plot_curve_item_rx_latency.setData([])
        self.netstat_plot_curve_item_tx_latency.setData([])
        logger.info("")

    def reset_plot(self):

        """ Reset the plot auto range. """

        self.netstat_plot_plot_widget.getPlotItem().enableAutoRange()
        logger.info("")
