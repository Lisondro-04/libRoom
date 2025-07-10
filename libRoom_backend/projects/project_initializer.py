import os
import json
from datetime import datetime
from pathlib import Path

def create_base_files(base_path: Path):
    base_path.mkdir(parents=True, exist_ok=True)

    (base_path / "outline").mkdir(exist_ok=True)
    (base_path / "characters").mkdir(exist_ok=True)
    (base_path / "world").mkdir(exist_ok=True)
    (base_path / "notes").mkdir(exist_ok=True)

    # archivos vacíos base
    (base_path / "settings.json").write_text('{}')
    (base_path / "preferences.json").write_text('{}')
    (base_path / "summary.txt").write_text('Project summary.')
    (base_path / "tags.txt").write_text('draft: #FFDD00\nreviewed: #00DDFF\nfinal: #00FF00\n')
    (base_path / "plots.txt").write_text('main_plot: \nsubplot1: \nsubplot2: \n')

def create_chapter_scene_structure(base_path: Path, chapters: int, scenes_per_chapter: int, words_per_scene: int):
    for ch_index in range(chapters):
        chapter_id = f"ch-{str(ch_index).zfill(3)}"
        chapter_folder = base_path /f"chapters/chapter_{ch_index + 1}"
        chapter_folder.mkdir(parents=True, exist_ok=True)

        scenes_ids = []

        for scn_index in range(scenes_per_chapter):
            scene_id = f"scn-{str((ch_index * scenes_per_chapter) + scn_index + 1).zfill(3)}"
            scenes_ids.append(scene_id)

            scene_data = {
                "title": f"Scene {scn_index + 1}",
                "ID": scene_id,
                "type": "md",
                "POV": "",
                "label": str(scn_index + 1),
                "status": "draft",
                "compile": 2,
                "setGoal": str(words_per_scene),
                "wordCount": 0,
            }

            (chapter_folder / f"{scene_id}.md").write_text(json.dumps(scene_data, indent=2))

        chapter_data = {
            "title": f"Chapter{ch_index + 1}",
            "ID": chapter_id,
            "type": "folder",
            "label": str(ch_index + 1),
            "status": "draft",
            "compile": 1,
            "setGoal": str(scenes_per_chapter * words_per_scene),
            "wordCount": "0",
            "scenes_id": scenes_ids,
        }

        (chapter_folder / "chapter.md").write_text(json.dumps(chapter_data, indent=2))
        
def generate_project_json(base_path: Path, data: dict):
    now = datetime.now().strftime("%d-%m-%Y")
    chapters = data["number_of_chapters"]
    scenes = data["scenes_by_chapter"]
    words_scene = data["words_by_scene"]

    content = {
        "title": data["title"],
        "author": data["author"],
        "created": now,
        "outline_path": "outline/",
        "characters_path": "characters/",
        "world_path": "notes/",
        "settings_file": "settings.json",
        "preferences_file": "preferences.json",
        "tags_file": "tags.txt",
        "plots_file": "plots.txt",
        "total_words_goal": str(chapters * scenes * words_scene),
        "words_by_scene": str(words_scene),
        "words_by_chapter": str(words_scene),
        "number_of_chapters": str(chapters),
        "scenes_by_chapters": str(scenes)
        }
    
    with open(base_path / "project.json", "w") as f:
        json.dump(content, f, indent=2)