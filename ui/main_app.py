import sys
from PySide2.QtWidgets import QApplication
#from .main_dialog_old import MainDialog
from .main_dialog import MainWindow

def launch_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
    
