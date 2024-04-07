import os
from .convert_funcs import json_to_dict, dict_to_json


JSON_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'user_data', 'software.json')


def get_app_list():
    dico = json_to_dict(JSON_FILE)
    return dico['apps']


def get_app_path(app_name: str):
    dico = json_to_dict(JSON_FILE)
    return dico[app_name]['app_path']


def get_preferences(app_name: str):
    dico = json_to_dict(JSON_FILE)
    return dico[app_name]['preferences']


def get_python_path(app_name: str):
    dico = json_to_dict(JSON_FILE)
    return dico[app_name]['python_path']


def get_icon(app_name: str):
    dico = json_to_dict(JSON_FILE)
    return dico[app_name]['icon']


def get_file(app_name: str):
    dico = json_to_dict(JSON_FILE)
    return dico[app_name]['file']


def set_app_path(app_name: str, path: str):
    dico = json_to_dict(JSON_FILE)
    dico[app_name]['app_path'] = path
    dict_to_json(dico, JSON_FILE)


def set_preferences(app_name: str, path: str):
    dico = json_to_dict(JSON_FILE)
    dico[app_name]['preferences'] = path
    dict_to_json(dico, JSON_FILE)


def set_python_path(app_name: str, path: str):
    dico = json_to_dict(JSON_FILE)
    dico[app_name]['python_path'] = path
    dict_to_json(dico, JSON_FILE)


def set_icon(app_name: str, path: str):
    dico = json_to_dict(JSON_FILE)
    dico[app_name]['icon'] = path
    dict_to_json(dico, JSON_FILE)


def set_file(app_name: str, path: str):
    dico = json_to_dict(JSON_FILE)
    dico[app_name]['file'] = path
    dict_to_json(dico, JSON_FILE)


def set_last_app(app_name: str):
    dico = json_to_dict(JSON_FILE)
    app_list: list = dico['apps']
    app_list.remove(app_name)
    app_list.insert(0, app_name)
    dico['apps'] = app_list
    dict_to_json(dico, JSON_FILE)
