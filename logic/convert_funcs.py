import json


def json_to_dict(json_file_path: str) -> dict:
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


def dict_to_json(dictionary: dict, json_file_path: str) -> None:
    '''
    Convert a Python dictionary to a JSON file.

    Parameters:
        dictionary (dict): The Python dictionary to convert to JSON.
        json_file_path (str): The destination JSON file path.
    '''
    
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(dictionary, file, indent=4, ensure_ascii=False)
