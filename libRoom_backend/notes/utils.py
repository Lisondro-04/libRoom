import os
import json
from datetime import datetime
from pathlib import Path

def get_notes_paths(base_path):
    notes_dir = Path(base_path) / "notes"
    index_path = notes_dir / "notes.json"
    notes_dir.mkdir(parents=True, exist_ok=True)
    return notes_dir, index_path

def load_index(base_path):
    notes_dir, index_path = get_notes_paths(base_path)
    if not index_path.exists() or index_path.stat().st_size == 0:
        # Inicializa el index vacío
        save_index(base_path, {"notes": []})
    with open(index_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_index(base_path, data):
    notes_dir, index_path = get_notes_paths(base_path)
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_next_id(base_path):
    index = load_index(base_path)
    notes = index["notes"]
    if not notes:
        return "nt-001"
    last_id = sorted([n["id"] for n in notes])[-1]
    num = int(last_id.split('-')[1]) + 1
    return f"nt-{num:03d}"

def word_count(text):
    return len(text.strip().split())

def save_note_md(base_path, note_id, title, linked_to, content):
    notes_dir, _ = get_notes_paths(base_path)
    wc = word_count(content)
    filepath = notes_dir / f"{note_id}.md"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"ID: {note_id}\n")
        f.write(f"title: {title}\n")
        f.write("type: note\n")
        f.write(f"linked_to: {linked_to}\n")
        f.write(f"wordCount: {wc}\n")
        f.write("->" + content)
    return wc

def load_note_md(base_path, note_id):
    notes_dir, _ = get_notes_paths(base_path)
    filepath = notes_dir / f"{note_id}.md"
    if not filepath.exists():
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        content = ''.join(lines[5:]).lstrip("->")
        return content

def delete_note_md(base_path, note_id):
    notes_dir, _ = get_notes_paths(base_path)
    filepath = notes_dir / f"{note_id}.md"
    if filepath.exists():
        filepath.unlink()
        return True
    return False
