from PySide2.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFileDialog,
    QWidget,
    QRadioButton
)
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
import os
from pathlib import Path
import subprocess
from ui.custom_button import CustomButton
from logic.app_finder import AppFinder
from logic.json_funcs import get_value, set_value, json_to_dict


class MainWindow(QMainWindow):
    
    
    VERSION = '1.1.0'
    JSON_FILE_PATH: Path = Path.cwd().joinpath('user_data', 'software_launcher_infos.json')
    apps = []
    paths = []
    current_app: str = None
    current_path: Path = None
    current_pref: Path = None
    current_python_path: Path = None
    current_file: Path = None
    
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.init_ui()
        self.create_widgets()
        self.create_layout()
        self.create_connections()
        
        
    def get_app_infos(self):
        if not self.JSON_FILE_PATH.exists():
            AppFinder(write_json=self.JSON_FILE_PATH)
            
        self.app_dict: dict = json_to_dict(self.JSON_FILE_PATH)
        for app, app_infos in self.app_dict.items():
            path = app_infos['path']
            if not path:
                continue
            self.apps.append(app)
            self.paths.append(path)
        
        
    def create_widgets(self):
        # create radio buttons
        self.get_app_infos()
        self.radio_buttons = []
        for app in self.apps:
            radio_button = QRadioButton(app.capitalize())
            self.radio_buttons.append(radio_button)
            
        # create buttons
        self.select_pref_label = QLabel('Preferences')
        self.select_pref_button = CustomButton()
        
        self.select_python_path_label = QLabel('Python path')
        self.select_python_path_button = CustomButton()
        
        self.select_file_label = QLabel('File path')
        self.select_file_button = CustomButton()
        self.select_file_button.setMinimumWidth(300)
        
        self.launch_button = QPushButton('Launch ')
        self.launch_button.setMinimumHeight(40)
    
    
    def create_layout(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)
        self.central_layout.addStretch(1)
        
        self.main_layout = QHBoxLayout()
        self.central_layout.addLayout(self.main_layout)
        
        self.radio_button_layout = QVBoxLayout()
        self.main_layout.addLayout(self.radio_button_layout)
        self.radio_button_layout.setAlignment(Qt.AlignLeft)
        
        for radio_button in self.radio_buttons:
            self.radio_button_layout.addWidget(radio_button)
            
        self.button_layout = QGridLayout()
        self.main_layout.addLayout(self.button_layout)
        
        self.button_layout.addWidget(self.select_pref_label, 0, 0)
        self.button_layout.addWidget(self.select_pref_button, 0, 1)
        
        self.button_layout.addWidget(self.select_python_path_label, 1, 0)
        self.button_layout.addWidget(self.select_python_path_button, 1, 1)
        
        self.button_layout.addWidget(self.select_file_label, 2, 0)
        self.button_layout.addWidget(self.select_file_button, 2, 1)
        
        self.central_layout.addWidget(self.launch_button)


    def create_connections(self):
        radio_button: QPushButton
        for radio_button in self.radio_buttons:
            radio_button.toggled.connect(self.update_current_app)
            radio_button.toggled.connect(self.update_launch_button)
            
        self.select_pref_button.clicked.connect(self.update_button)
        self.select_python_path_button.clicked.connect(self.update_button)
        self.select_file_button.clicked.connect(self.update_button)
        self.select_pref_button.clear_action.triggered.connect(self.update_current_pref)
        self.select_python_path_button.clear_action.triggered.connect(self.update_current_python_path)
        self.select_file_button.clear_action.triggered.connect(self.update_current_file)
        
        self.launch_button.clicked.connect(self.launch_app)
    
    
    def update_current_app(self):
        self.current_app = self.sender().text().lower()
        self.current_path = self.app_dict[self.current_app]['path']
        print(f'Current app : {self.current_app}')
        print(f'Current path : {self.current_path}')
        self.select_pref_button.setText(get_value(json_file=self.JSON_FILE_PATH, main_key=self.current_app, key='pref'))
        self.select_python_path_button.setText(get_value(json_file=self.JSON_FILE_PATH, main_key=self.current_app, key='python_path'))
        self.select_file_button.setText(get_value(json_file=self.JSON_FILE_PATH, main_key=self.current_app, key='file'))
        
        
    def update_current_pref(self):
        self.current_pref: Path = Path(self.select_pref_button.text())
        set_value(json_file=self.JSON_FILE_PATH, main_key=self.current_app, key='pref', value=self.current_pref)
    
    
    def update_current_python_path(self):
        self.current_python_path: Path = Path(self.select_python_path_button.text())
        set_value(json_file=self.JSON_FILE_PATH, main_key=self.current_app, key='python_path', value=self.current_python_path)


    def update_current_file(self):
        self.current_file: Path = Path(self.select_file_button.text())
        set_value(json_file=self.JSON_FILE_PATH, main_key=self.current_app, key='file', value=self.current_file)
        
        
    def update_launch_button(self):
        self.launch_button.setText(f'Launch {self.current_app.capitalize()}')
        
        
    def update_button(self):
        button_dict: dict = {
            self.select_pref_button: self.current_pref,
            self.select_python_path_button: self.current_python_path,
            self.select_file_button: self.current_file,
        }
        
        button: QPushButton = self.sender()
        button_text = button.text()

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)

        if button_text:
            file_dialog.setDirectory(str(Path(button_text).parent))
                
        options = QFileDialog.Options()
        
        if button in (self.select_pref_button, self.select_python_path_button):
            new_path = file_dialog.getExistingDirectory(self, 'Select directory', options=options)
        else:
            new_path, _ = file_dialog.getOpenFileName(self, 'Select file', options=options)
            
        if not new_path:
            return
        
        new_path = Path(new_path)
        current_value: Path = button_dict.get(button)
        current_value = new_path
        set_value(json_file=self.JSON_FILE_PATH, main_key=self.current_app, key='python_path', value=new_path)
        button.setText(str(current_value))
        
        
    def launch_app(self):
        app_args = [self.current_path]
        if self.current_file:
            app_args.append(self.current_file)
        
        pref_dict = {
            'houdini': 'HOUDINI_USER_PREF_DIR',
            'maya': 'MAYA_APP_DIR',
            'nuke': 'NUKE_PATH'
        }
        if not self.current_app in ('houdini', 'maya', 'nuke'):
            subprocess.Popen(app_args)
            return
            
        pref_name = pref_dict[self.current_app]
        env = os.environ.copy()
        if self.current_pref and os.path.exists(self.current_pref):
            env[pref_name] = self.current_pref
        if self.current_python_path and os.path.exists(self.current_python_path):
            env["PYTHONPATH"] = self.current_python_path
            
        subprocess.Popen(app_args, env=env)

        
    def init_ui(self):
        self.setWindowTitle(f'Software launcher - {self.VERSION}')
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setMinimumSize(450, 250)
        self.setStyleSheet(open(Path.cwd().joinpath('ui', 'style.css')).read())
        self.setWindowIcon(QIcon(str(Path.cwd().joinpath('ui', 'icon.ico'))))
