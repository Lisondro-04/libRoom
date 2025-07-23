import json
from pathlib import Path
from libRoom_backend.settings import BASE_DIR

PROJECT_DIR = Path(BASE_DIR) / ""

def get_project_json():
    with open(PROJECT_DIR / "project.json") as f:
        return json.load(f)

def save_project_json(data):
    with open(PROJECT_DIR / "project.json", "w") as f:
        json.dump(data, f, indent=2)
