import json
import os
from django.conf import settings

def get_project_path():
    with open(os.path.join(settings.BASE_DIR, 'project.json')) as f:
        project = json.load(f)
    return project.get('path')

def get_preferences_path():
    project_path = get_project_path()
    return os.path.join(project_path, 'preferences.json')

def read_preferences():
    with open(get_preferences_path(), 'r') as f:
        return json.load(f)

def write_preferences(data):
    with open(get_preferences_path(), 'w') as f:
        json.dump(data, f, indent=4)

def update_total_words_goal_in_project(goal):
    project_path = get_project_path()
    project_file = os.path.join(project_path, 'project.json')
    with open(project_file, 'r') as f:
        project_data = json.load(f)
    project_data['total_words_goal'] = goal
    with open(project_file, 'w') as f:
        json.dump(project_data, f, indent=4)
