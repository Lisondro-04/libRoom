import os
import json
import threading
from django.conf import settings as django_settings

lock = threading.Lock()

def get_project_settings_path():
    # Asume que el archivo project.json tiene la ruta a settings.json
    project_json_path = os.path.join(django_settings.BASE_DIR, 'project.json')
    with open(project_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['settings_path']

def read_settings():
    settings_path = get_project_settings_path()
    with lock, open(settings_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_settings(data):
    settings_path = get_project_settings_path()
    with lock, open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def validate_and_prepare(data):
    valid_languages = ['es', 'en-US']
    valid_autosave = ['off', '1min', '5min', '10min', 'on_change']

    if data.get('language') not in valid_languages:
        raise ValueError(f"Invalid language: {data.get('language')}")

    if data.get('autosave_frequency') not in valid_autosave:
        raise ValueError(f"Invalid autosave_frequency: {data.get('autosave_frequency')}")

    if data.get('cloud_autosave_frequency') not in valid_autosave:
        raise ValueError(f"Invalid cloud_autosave_frequency: {data.get('cloud_autosave_frequency')}")

    # Validar rutas y crear carpetas si no existen
    for path_key in ['default_project_path', 'default_export_path']:
        path_value = data.get(path_key)
        if path_value and not os.path.exists(path_value):
            os.makedirs(path_value)

    return data
