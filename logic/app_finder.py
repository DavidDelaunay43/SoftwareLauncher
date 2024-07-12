from pathlib import Path
from .json_funcs import dict_to_json


class AppFinder:
    
    
    PROGRAM_FILES: Path = Path('C:/Program Files')
    APPS: tuple = 'blender', 'it', 'krita', 'houdini', 'maya', 'mari', 'nuke', 'photoshop', 'substance_designer', 'substance_painter', 'zbrush'
    app_dict = {app: {'path': None, 'pref': None, 'python_path': None, 'file': None} for app in APPS}
    
    
    def __init__(self, write_json: str = None) -> dict:
            
        self.app_dict['blender']['path'] = str(self.find_blender())
        self.app_dict['krita']['path'] = str(self.find_krita())
        self.app_dict['houdini']['path'] = str(self.find_houdini())
        self.app_dict['mari']['path'] = str(self.find_mari())
        self.app_dict['maya']['path'] = str(self.find_maya())
        self.app_dict['nuke']['path'] = str(self.find_nuke())
        self.app_dict['photoshop']['path'] = str(self.find_photoshop())
        self.app_dict['zbrush']['path'] = str(self.find_zbrush())
        
        self.app_dict['houdini']['pref'] = str(self.find_houdini_pref())
        self.app_dict['mari']['pref'] = str(self.find_mari_pref())
        self.app_dict['maya']['pref'] = str(self.find_maya_pref())
        self.app_dict['nuke']['pref'] = str(self.find_nuke_pref())
        
        if write_json:
            self.write_json_file(json_file=write_json)
        
        
    def write_json_file(self, json_file: str):
        dict_to_json(dictionary=self.app_dict, json_file_path=json_file)
        
            
    def find_directory(self, parent_directory: Path, directory_string: str, exclude_strings = [], exe=False) -> Path:
        for dir in parent_directory.iterdir():
            dir_name: str = dir.name
            if dir_name.startswith(directory_string):
                if dir_name in exclude_strings:
                        continue
                if exe:
                    if dir_name.endswith('.exe'):
                        return dir
                else:
                    return dir
            
            
    def find_blender(self) -> Path:
        exe: str = 'blender.exe'
        parent_dir: Path = self.PROGRAM_FILES.joinpath('Blender Foundation')
        dir_string: str = 'Blender '
        return self.find_directory(parent_directory=parent_dir, directory_string=dir_string).joinpath(exe)
        
    
    def find_krita(self) -> Path:
        exe: str = 'krita.exe'
        return self.PROGRAM_FILES.joinpath('Krita (x64)', 'bin', exe)
    
    
    def find_houdini(self) -> Path:
        exe: str = 'houdini.exe'
        parent_dir: Path = self.PROGRAM_FILES.joinpath('Side Effects Software')
        dir_string: str = 'Houdini'
        return self.find_directory(parent_directory=parent_dir, directory_string=dir_string, exclude_strings=['Houdini Engine', 'Houdini Server']).joinpath('bin', exe)
    
    
    def find_mari(self) -> Path:
        mari: str = 'Mari'
        parent_dir: Path = self.PROGRAM_FILES.joinpath(self.find_directory(parent_directory=self.PROGRAM_FILES, directory_string=mari), 'Bundle', 'bin')
        return self.find_directory(parent_directory=parent_dir, directory_string=mari)
    
    def find_maya(self) -> Path:
        exe: str = 'maya.exe'
        parent_dir: Path = self.PROGRAM_FILES.joinpath('Autodesk')
        dir_string: str = 'Maya'
        return self.find_directory(parent_directory=parent_dir, directory_string=dir_string).joinpath('bin', exe)
    
    
    def find_nuke(self) -> Path:
        nuke: str = 'Nuke'
        parent_dir: Path = self.PROGRAM_FILES.joinpath(self.find_directory(parent_directory=self.PROGRAM_FILES, directory_string=nuke))
        return self.find_directory(parent_directory=parent_dir, directory_string=nuke, exe=True)
    
    
    def find_photoshop(self) -> Path:
        exe: str = 'Photoshop.exe'
        parent_dir: Path = self.PROGRAM_FILES.joinpath('Adobe')
        dir_string: str = 'Adobe Photoshop '
        return self.find_directory(parent_directory=parent_dir, directory_string=dir_string).joinpath(exe)
    
    
    def find_zbrush(self) -> Path:
        exe: str = 'ZBrush.exe'
        return self.PROGRAM_FILES.joinpath(self.find_directory(parent_directory=self.PROGRAM_FILES, directory_string='Maxon ZBrush ')).joinpath(exe)


    def find_houdini_pref(self) -> str:
        documents_folder: Path = Path.home().joinpath('Documents')
        return documents_folder.joinpath(self.find_directory(parent_directory=documents_folder, directory_string='houdini'))
    
    
    def find_maya_pref(self) -> Path:
        documents_folder: Path = Path.home().joinpath('Documents')
        return documents_folder.joinpath(self.find_directory(parent_directory=documents_folder, directory_string='maya'))
    
    
    def find_mari_pref(self) -> Path:
        return Path.home().joinpath('.mari')
    
    
    def find_nuke_pref(self) -> Path:
        return Path.home().joinpath('.nuke')
