import json
from pathlib import Path
from typing import Union


def json_to_dict(json_file_path: Union[str, Path]) -> dict:
    '''
    Convert a JSON file to a Python dictionary.

    Parameters:
        json_file_path (str): The path of the JSON file to convert to a dictionary.

    Returns:
        dict: The resulting Python dictionary from the JSON file.
    '''
    
    with open(json_file_path, 'r', encoding='utf-8') as file:
        dico = json.load(file)
        
    return dico


def dict_to_json(dictionary: dict, json_file_path: Union[str, Path]) -> None:
    '''
    Convert a Python dictionary to a JSON file.

    Parameters:
        dictionary (dict): The Python dictionary to convert to JSON.
        json_file_path (str): The destination JSON file path.
    '''
    
    dictionary = {key: str(value) if isinstance(value, Path) else value for key, value in dictionary.items()}
    
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(dictionary, file, indent=4, ensure_ascii=False)
        
        
def get_value(json_file: str, main_key: str, key: str) -> str:
    
    value = json_to_dict(json_file_path=json_file).get(main_key).get(key)
    value = '' if value == '.' else value
    return value


def set_value(json_file: str, main_key: str, key: str, value: str) -> None:
    
    value = '' if value == '.' else value
    
    if isinstance(value, Path):
        value = str(value)
    
    dictionnary: dict = json_to_dict(json_file_path=json_file)
    dictionnary[main_key][key] = value
    dict_to_json(dictionary=dictionnary, json_file_path=json_file)
