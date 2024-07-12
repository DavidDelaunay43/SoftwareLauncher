from pathlib import Path
from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QPushButton,
    QAction,
    QMenu
)


class CustomButton(QPushButton):
    
    JSON_FILE_PATH: Path = Path.cwd().joinpath('user_data', 'software_launcher_infos.json')
    
    def __init__(self):
        super(CustomButton, self).__init__()
        self.create_context_menu()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        
    def create_context_menu(self):
        self.context_menu = QMenu(self)
        self.clear_action = QAction('Clear', self)
        self.context_menu.addAction(self.clear_action)
        self.clear_action.triggered.connect(self.clear_text)
        

    def show_context_menu(self, pos):
        self.context_menu.exec_(self.mapToGlobal(pos))


    def clear_text(self):
        self.setText('')
