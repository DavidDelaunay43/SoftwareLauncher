from PySide2.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QComboBox,
    QPushButton
)
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon

from json_funcs.get_set_funcs import (
    get_app_list,
    get_app_path,
    get_preferences,
    get_python_path,
    get_file,
    set_last_app
)


class MainDialog(QDialog):
    
    
    def __init__(self):
        super(MainDialog, self).__init__()
        
        self.VERSION = '0.0.0'
        self.init_ui()
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        
        self.init_widgets()
        
        
    def init_ui(self):
        self.setWindowTitle(f'Software launcher - {self.VERSION}')
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumSize(450, 250)
        
        
    def create_widgets(self):
        self.select_app_label = QLabel('Select app')
        self.select_app_combobox = QComboBox()
        
        self.select_app_path_label = QLabel('App path')
        self.select_app_path_button = QPushButton()
        
        self.select_pref_label = QLabel('Select pref folder')
        self.select_pref_button = QPushButton()
        
        self.select_python_path_label = QLabel('Select python path folder')
        self.select_python_path_button = QPushButton()
        
        self.select_file_label = QLabel('Select file folder')
        self.select_file_button = QPushButton()
        
        self.launch_button = QPushButton('Launch app')
    
    
    def create_layout(self):
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)
        
        self.grid_layout.addWidget(self.select_app_label, 0, 0)
        self.grid_layout.addWidget(self.select_app_combobox, 0, 1)
        
        self.grid_layout.addWidget(self.select_app_path_label, 1, 0)
        self.grid_layout.addWidget(self.select_app_path_button, 1, 1)
        
        self.grid_layout.addWidget(self.select_pref_label, 2, 0)
        self.grid_layout.addWidget(self.select_pref_button, 2, 1)
        
        self.grid_layout.addWidget(self.select_python_path_label, 3, 0)
        self.grid_layout.addWidget(self.select_python_path_button, 3, 1)
        
        self.grid_layout.addWidget(self.select_file_label, 4, 0)
        self.grid_layout.addWidget(self.select_file_button, 4, 1)
        
        self.main_layout.addWidget(self.launch_button)
    
    
    def create_connections(self):
        self.select_app_combobox.currentIndexChanged.connect(self.update_widgets)
        self.launch_button.clicked.connect(self.launch_app)

    def init_widgets(self):
        app_list = get_app_list()
        
        self.select_app_combobox.addItems(app_list)
        

    def update_widgets(self):
        app = self.select_app_combobox.currentText()
        set_last_app(app)
        
        self.select_app_path_button.setText(get_app_path(app))
        self.select_pref_button.setText(get_preferences(app))
        self.select_python_path_button.setText(get_python_path(app))
        self.select_file_button.setText(get_file(app))


    def launch_app(self):
        
        import os
        import subprocess
        
        path = self.select_app_path_button.text()
        prefs = self.select_pref_button.text()
        python_path = self.select_python_path_button.text()
        file = self.select_file_button.text()
        
        env = os.environ.copy()
        
        if prefs and os.path.exists(prefs):
            env["MAYA_APP_DIR"] = prefs
            
        if python_path and os.path.exists(python_path):
            env["PYTHONPATH"] = python_path

        app_args = [path]
        
        if file and os.path.exists(file):
            app_args.append(file)
        
        print(f'subprocess.Popen({app_args}, env={env})')
        subprocess.Popen(app_args, env=env)
