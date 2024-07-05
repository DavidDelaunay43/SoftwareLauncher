import sys
from PySide2.QtWidgets import QApplication
from .main_window import MainWindow


def launch_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
    