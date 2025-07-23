import json
import os
import threading

lock = threading.Lock()

def get_settings_file(base_path):
    """
    Obtiene la ruta completa al settings.json del proyecto actual.
    """
    project_json_path = os.path.join(base_path, "project.json")
    with open(project_json_path, 'r', encoding='utf-8') as f:
        project_data = json.load(f)
        # Retorna la ruta completa a settings.json
        return os.path.join(base_path, project_data['settings_file'])

def read_settings(base_path):
    """
    Lee el settings.json del proyecto.
    """
    settings_path = get_settings_file(base_path)
    with lock:
        with open(settings_path, 'r', encoding='utf-8') as f:
            return json.load(f)

def write_settings(base_path, data):
    """
    Escribe en el settings.json del proyecto.
    """
    settings_path = get_settings_file(base_path)
    with lock:
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

def validate_and_create_paths(data):
    """
    Valida y crea las rutas de carpetas necesarias.
    """
    paths = ['default_project_path', 'default_export_path', 'cloud_sync_path']
    for path_key in paths:
        path_value = data.get(path_key)
        if path_value and not os.path.exists(path_value):
            os.makedirs(path_value, exist_ok=True)
