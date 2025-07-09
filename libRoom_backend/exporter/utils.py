import os, re, subprocess
import json

def load_project_structure(root_path, include_chapters=True, include_scenes=True, status_filter=None):
    chapters_dir = os.path.join(root_path, "outline")
    chapters = []

    for folder in sorted(os.listdir(chapters_dir)):
        chapter_path = os.path.join(chapters_dir, folder, "chapter.md")
        if not os.path.exists(chapter_path):
            continue

        chapter_data = parse_chapter_file(chapter_path)

        if status_filter and chapter_data["status"] not in status_filter:
            continue

        if include_scenes:
            chapter_data["scenes"] = load_scenes_for_chapter(chapters_dir, folder, chapter_data.get("scenes_ids", []))

        chapters.append(chapter_data)

    return chapters

def parse_chapter_file(chapter_path):
    with open(chapter_path, encoding="utf-8") as f:
        lines = f.read().splitlines()

    data = {"id": None, "title": None, "status": None, "scenes_ids": []}

    for line in lines:
        if line.startswith("id: "):
            data["id"] = line[4:]
        elif line.startswith("title: "):
            data["title"] = line[7:]
        elif line.startswith("status: "):
            data["status"] = int(line[8:])
        elif line.startswith("scenes_ids: "):
            ids = line[len("scenes_ids: "):].split(", ")
            data["scenes_ids"] = ids

    return data

def load_scenes_for_chapter(chapters_dir, folder, scene_ids):
    scenes = []
    for sid in scene_ids:
        scene_file = os.path.join(chapters_dir, folder, f"{sid}.md")
        if not os.path.exists(scene_file):
            continue
        with open(scene_file, encoding="utf-8") as f:
            scene_text = f.read()
        scenes.append({
            "id": sid,
            "title": f"Scene {sid}",
            "text": scene_text
        })
    return scenes


def apply_text_transformations(content, transformations, separators):
    sep_ch = separators.get("between_chapters", "\n\n")
    sep_cs = separators.get("between_chapter_and_scene", "---")
    sep_s = separators.get("between_scenes", "\n\n")

    full_text = []
    for chapter in content:
        parts = [f"{chapter['title']}"]
        if chapter.get("scenes"):
            for scene in chapter["scenes"]:
                text = scene["text"]
                text = apply_replacements(text, transformations)
                parts.append(sep_cs)
                parts.append(text)
        full_text.append(sep_s.join(parts))
    return sep_ch.join(full_text)

def apply_replacements(text, t):
    if t.get("remove_multiple_spaces"):
        text = re.sub(r'[ \t]{2,}', ' ', text)
    if "double_quotes" in t:
        text = text.replace('"', t["double_quotes"][1])
    if "single_quotes" in t:
        text = text.replace("'", t["single_quotes"][1])
    if "long_dash" in t:
        text = text.replace("---","—")
    for k, v in t.get("custom_replacements", {}).items():
        text = text.replace(k, v)
    return text

def export_to_format(text, output_path, format, title, author):
    input_md = output_path + ".md"
    with open(input_md, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n**{author}**\n\n{text}")
    subprocess.run([
        "pandoc", input_md, "-o", output_path
    ], check=True)
    os.remove(input_md)
