
import time
import logging
import threading
from datetime import datetime

import pyqtgraph as pg
from PyQt5 import QtCore

DEFAULT_MAX_STREAM_TIME_PERIOD_SEC = 1

logger = logging.getLogger(__name__)

class NetStatStream(QtCore.QThread):

    gui_stream_handle_cb = QtCore.pyqtSignal(str)

    def __init__(self, instant_resp_cmnd_handle) -> None:
        super(NetStatStream, self).__init__()
        self.instant_resp_cmnd_handle = instant_resp_cmnd_handle
        self.kill_netstat_plot = False
        self.response_received = threading.Event()
        self.netstat_data = None
        logger.info("Init NetStatStream thread")

    def run(self):

        prev_data_stream_time = datetime.now()
        logger.info("NetStatStream thread function")
        while True:
            data_stream = ''
            try:
                self.response_received.clear()
                self.instant_resp_cmnd_handle.issue_command(self.default_netstat_rx_callback)
                # Wait for the response.
                self.response_received.wait()
            except:
                pass

            if self.kill_netstat_plot:
                break

            if data_stream == '':
                continue

            self.gui_stream_handle_cb.emit(self.netstat_data)
            time.sleep(DEFAULT_MAX_STREAM_TIME_PERIOD_SEC)

    def default_netstat_rx_callback(self, response):
        if response is not None:
            try:
                str_resp = response.decode(encoding = 'ascii')
                self.netstat_data = str_resp
                print(f"{str_resp}")
            except:
                print(response)
        else:
            print("Timed out while waiting for response!")
        # Signal the do_send function to return.
        self.response_received.set()


    def stop_stream_qthread(self, stop_fw_stream = False, simple_cmnd_app = None):

        self.kill_netstat_plot = True

    def start_stream_qthread(self, start_fw_stream = True):
        logger.info("Start NetStatStream thread")
        self.start()




NETSTAT_PLOT_COLOR = '#0099ff'
NETSTAT_PLOT_AXIS_LABEL_COLOR = '#000000'
NETSTAT_PLOT_AXIS_LABEL_FONT_SIZE = "12pt"
NETSTAT_PLOT_COLOR_LEFT_Y_AXIS_NAME =  "ms"
DEFAULT_MAX_NETSTAT_PLOT_REAL_TIME_DATA = 40
NETSTAT_PLOT_COLOR_BOTTOM_X_AXIS_NAME =  "TIME"
NETSTAT_PLOT_AXIS_LABEL_STYLE = {"label": "COLUMN 1", "color": (NETSTAT_PLOT_AXIS_LABEL_COLOR), "font-size": NETSTAT_PLOT_AXIS_LABEL_FONT_SIZE}
NETSTAT_PLOT_PERCENT_INDEX = 0

class NetStat_MainWindowPlotter:

    def __init__(self, ui_plot_widget) -> None:

        self.plot_x_axis_data = []
        self.plot_y_axis_data = []
        self.num_current_data_pts = 0
        self.is_plot_paused = False

        self.netstat_plot_plot_widget = ui_plot_widget
        self.netstat_plot_plot_item = self.netstat_plot_plot_widget.plotItem

        """ Set axis labels, and label & axis colors. """
        self.netstat_plot_plot_item.getAxis('left').setPen(pg.mkPen(color=(NETSTAT_PLOT_COLOR), width=2))
        self.netstat_plot_plot_item.getAxis('bottom').setPen(pg.mkPen(color=(NETSTAT_PLOT_COLOR), width=2))
        self.netstat_plot_plot_item.setLabel('left', NETSTAT_PLOT_COLOR_LEFT_Y_AXIS_NAME, **NETSTAT_PLOT_AXIS_LABEL_STYLE)
        self.netstat_plot_plot_item.setLabel('bottom', NETSTAT_PLOT_COLOR_BOTTOM_X_AXIS_NAME, **NETSTAT_PLOT_AXIS_LABEL_STYLE) 

        self.netstat_plot_plot_item.showGrid(x = True, y = True, alpha = 0.1)

        """ Create one curves and add it to the plotWidget """
        self.netstat_plot_curve_item = pg.PlotCurveItem(pen=({'color': NETSTAT_PLOT_COLOR, 'width': 2}), skipFiniteCheck=True)
        self.netstat_plot_plot_widget.addItem(self.netstat_plot_curve_item)

        logger.info("Init plot")


    def append_stream_data_to_list(self, strm_data):

        if strm_data != None:
            self.plot_y_axis_data.append(strm_data.stream_data)
        else:
            self.plot_y_axis_data.append(0)

        self.plot_x_axis_data.append(time.time())


    def parse_curve_data(self, strm_data):
        if self.num_current_data_pts < DEFAULT_MAX_NETSTAT_PLOT_REAL_TIME_DATA:
            self.append_stream_data_to_list(strm_data)
            self.num_current_data_pts += 1
        else:
            self.plot_x_axis_data = self.plot_x_axis_data[1:]
            self.plot_y_axis_data = self.plot_y_axis_data[1:]
            self.append_stream_data_to_list(strm_data)

    def update_plot_data(self, strm_data):

        """ 
        Parse the stream data from the Stream_Data object and plot
        it. 
        """
        try:
            if not self.is_plot_paused:
                self.parse_curve_data(strm_data)
                self.netstat_plot_curve_item.setData(self.plot_x_axis_data[:self.num_current_data_pts], \
                    self.plot_y_axis_data[:self.num_current_data_pts])
        except:
            logger.error("Exception in append_stream_data_to_list: {}".format(strm_data))


    def clear_plot_data(self):

        """ Clear the plot data and clear the graph curve. """

        self.plot_x_axis_data = []
        self.plot_y_axis_data = []
        self.num_current_data_pts = 0
        self.netstat_plot_curve_item.setData([])
        logger.info("")

    def reset_plot(self):

        """ Reset the plot auto range. """

        self.netstat_plot_plot_widget.getPlotItem().enableAutoRange()
        logger.info("")
