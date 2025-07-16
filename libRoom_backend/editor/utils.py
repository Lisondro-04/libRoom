import re
from pathlib import Path

def read_scene_file(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    metadata = {}
    content_lines = []
    in_metadata =  True

    for line in lines:
        if in_metadata and ": " in line:
            key, value = line.strip().split(": ", 1)
            metadata[key] = value
        else:
            in_metadata = False
            content_lines.append(line)

    content = ''.join(content_lines).lstrip()
    metadata['content'] =  content
    metadata['wordCount'] = len(content.split())

    # type conversion
    for int_field in ['label', 'compile', 'setGoal', 'wordCount']:
        if int_field in metadata:
            try:
                metadata[int_field] = int(metadata[int_field])
            except ValueError:
                pass # deja el string si no se puede convertir

    return metadata

def write_scene_file(path: Path, data: dict):
    lines = []
    for key in ['title', 'ID', 'type', 'POV', 'label', 'status', 'compile', 'setGoal', 'wordCount']:
        if key in data: 
            lines.append(f"{key}: {data[key]}\n")
    lines.append("\n") #separación entre metadatos y contenido
    lines.append(data.get("content", ""))

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def get_scene_path_by_id(scene_id, base_dir):
    chapters_path = Path(base_dir) / "outline"/ "chapters"
    for chapter in chapters_path.iterdir():
        if chapter.is_dir():
            for file in chapter.glob("*.md"):
                if file.stem.startswith(scene_id):
                    return file
    return None