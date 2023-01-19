
import sys
import logging
from ui.main_window import Ui_MainWindow
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

if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = PC_APP()
    w.show()
    app.exec()
