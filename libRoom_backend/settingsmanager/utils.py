import json
import os
import threading

lock = threading.Lock()

SETTINGS_FILE_PATH = 'ruta_absoluta_a_tu_project.json'  # Cambia esto por la real

def get_settings_file():
    with open(SETTINGS_FILE_PATH, 'r', encoding='utf-8') as f:
        project_data = json.load(f)
        return project_data['settings_path']

def read_settings():
    settings_path = get_settings_file()
    with lock:
        with open(settings_path, 'r', encoding='utf-8') as f:
            return json.load(f)

def write_settings(data):
    settings_path = get_settings_file()
    with lock:
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

def validate_and_create_paths(data):
    paths = ['default_project_path', 'default_export_path', 'cloud_sync_path']
    for path_key in paths:
        path_value = data.get(path_key)
        if path_value and not os.path.exists(path_value):
            os.makedirs(path_value, exist_ok=True)
