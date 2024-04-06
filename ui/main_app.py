import sys
from PySide2.QtWidgets import QApplication
from .main_dialog import MainDialog

def launch_app():
    app = QApplication(sys.argv)
    dialog = MainDialog()
    if dialog.exec_() == MainDialog.Accepted:
        sys.exit(app.exec_())
