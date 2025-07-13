import os
import json
from datetime import datetime
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent / 'storage'
INDEX_PATH = BASE_DIR / 'notes_index.json'


if not BASE_DIR.exists():
    BASE_DIR.mkdir(parents=True, exist_ok=True)


def load_index():
    if not INDEX_PATH.exists() or INDEX_PATH.stat().st_size == 0:
        # Inicializa el index vacío
        save_index({"notes": []})
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_index(data):
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_next_id():
    index = load_index()
    notes = index["notes"]
    if not notes:
        return "nt-001"
    last_id = sorted([n["id"] for n in notes])[-1]
    num = int(last_id.split('-')[1]) + 1
    return f"nt-{num:03d}"


def word_count(text):
    return len(text.strip().split())


def save_note_md(note_id, title, linked_to, content):
    wc = word_count(content)
    filepath = BASE_DIR / f"{note_id}.md"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"ID: {note_id}\n")
        f.write(f"title: {title}\n")
        f.write("type: note\n")
        f.write(f"linked_to: {linked_to}\n")
        f.write(f"wordCount: {wc}\n")
        f.write("->" + content)
    return wc


def load_note_md(note_id):
    filepath = BASE_DIR / f"{note_id}.md"
    if not filepath.exists():
        return None
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        content = ''.join(lines[5:]).lstrip("->")
        return content


def delete_note_md(note_id):
    filepath = BASE_DIR / f"{note_id}.md"
    if filepath.exists():
        filepath.unlink()
        return True
    return False
