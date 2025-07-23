import json
import os

def get_project_metadata(base_path):
    path = os.path.join(base_path, 'project.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_project_metadata(base_path, data):
    path = os.path.join(base_path, 'project.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def get_preferences_path(base_path):
    return os.path.join(base_path, 'preferences.json')

def read_preferences(base_path):
    with open(get_preferences_path(base_path), 'r', encoding='utf-8') as f:
        return json.load(f)

def write_preferences(base_path, data):
    with open(get_preferences_path(base_path), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def update_total_words_goal_in_project(base_path, goal):
    project_data = get_project_metadata(base_path)
    project_data['total_words_goal'] = goal
    update_project_metadata(base_path, project_data)
