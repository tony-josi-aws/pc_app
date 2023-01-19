
import sys
import logging
from ui.main_window import Ui_MainWindow
from ui.ui_backend import PC_App_Handler
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

gui_logger = logging.getLogger(__name__)

class PC_APP(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        super(PC_APP, self).__init__()

        """ Set up the main window user interface. """
        self.mw_ui = Ui_MainWindow()
        self.mw_ui.setupUi(self)

        self.app_handle = PC_App_Handler(self.mw_ui)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = PC_APP()
    w.show()
    app.exec()
