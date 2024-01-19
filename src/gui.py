import os
import sys
import ctypes
import logging
import ui.resources.icons
from ui.main_window import Ui_MainWindow
from ui.ui_backend import PC_App_Handler

import qdarktheme

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

gui_logger = logging.getLogger(__name__)

class PC_APP(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        super(PC_APP, self).__init__()

        if os.name == 'nt':
            '''
            Fix main window icon display issue on windows due to peculiarities 
            in how taskbar icons are handled on the Windows platform.

            Refer: https://stackoverflow.com/q/1551605/6792356
            '''
            myappid = 'FreeRTOS.X-RayForFreeRTOS.2.3' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        """ Set up the main window user interface. """
        self.mw_ui = Ui_MainWindow()
        self.mw_ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(':/icons/window_icon.jpg'))

        self.app_handle = PC_App_Handler(self)

if __name__ == "__main__":
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    app.setStyle('QtCurve')
    w = PC_APP()
    w.show()
    app.exec()
