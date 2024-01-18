import sys
import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QLabel, QWidget

class AppDialogBox():

    def __init__(self, main_window):
        self.mw = main_window

    def show_dialog(self, title, message):
        # Create a QDialog instance
        dialog = QDialog(self.mw)

        dialog.setWindowTitle(title)
        dialog.setFixedWidth(400)
        dialog.setFixedHeight(200)

        # Create a label with a message
        label = QLabel(message)

        # Create a layout for the dialog
        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(label)

        # Set the layout for the dialog
        dialog.setLayout(dialog_layout)

        # Show the dialog as a modal dialog (blocks the main window)
        dialog.exec_()