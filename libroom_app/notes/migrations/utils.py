import os
import re
from django.conf import settings

NOTES_DIR = os.path.join(settings.BASE_DIR, 'notes')

def get_next_note_id():
    files = [f for f in os.listdir(NOTES_DIR) if re.match(r'nt-\d{3}\.md', f)]
    if not files:
        return 'nt-001'
    numbers = [int(re.findall(r'\d{3}', f)[0]) for f in files]
    next_number = max(numbers) + 1
    return f"nt-{next_number:03d}"

def save_note_content(note_id, content):
    path = os.path.join(NOTES_DIR, f"{note_id}.md")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def read_note_content(note_id):
    path = os.path.join(NOTES_DIR, f"{note_id}.md")
    if not os.path.exists(path):
        return ''
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def delete_note_file(note_id):
    path = os.path.join(NOTES_DIR, f"{note_id}.md")
    if os.path.exists(path):
        os.remove(path)

def count_words(content):
    return len(content.split())
