import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QLabel, QWidget, QMessageBox

class AppDialogBox():

    def __init__(self, main_window):
        self.mw = main_window

    def show_dialog(self, title, message):
        # Create a QDialog instance
        dialog = QMessageBox(self.mw)
     
        dialog.setText(message)
        dialog.setWindowTitle(title)
        #dialog.setStyleSheet("QLabel{height: 100px; min-height: 100px; max-height: 100px;min-width: 500px; }")

        # Show the dialog as a modal dialog (blocks the main window)
        dialog.exec_()