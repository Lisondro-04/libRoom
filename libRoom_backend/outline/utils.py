import os
import json
import uuid
from pathlib import Path
from typing import List, Dict, Optional
from django.conf import settings

def load_project_json(base_path: str) -> Dict:
    path = Path(base_path) / "project.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)

def save_project_json(base_path: str, data: Dict):
    path = Path(base_path) / "project.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_outline_root(base_path: str) -> Path:
    data = load_project_json(base_path)
    return Path(data["outline_path"]) / "chapters"

def generate_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:4]}"

def get_tags_list(base_path: str) -> List[str]:
    pj = load_project_json(base_path)
    path = Path(pj["tags_file"])
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8").splitlines()
