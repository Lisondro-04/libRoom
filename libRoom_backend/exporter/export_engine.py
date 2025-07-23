from pathlib import Path
import os
import json
import tempfile
from .utils import (
    load_project_structure,
    apply_text_transformations,
    export_to_format
)

def export_project(config):
    project_root = Path(config["base_path"]).expanduser().resolve()

    # load project metadata
    with open(os.path.join(project_root, "project.json"), encoding="utf-8") as f:
        metadata = json.load(f)

    title = metadata.get("title", "Untitled")
    autor = metadata.get("author", "Unknow")

    # load structure
    content = load_project_structure(
        root_path=project_root,
        include_chapters=config.get("include_chapters", True),
        include_scenes=config.get("include_scenes", True),
        status_filter=config.get("status_filter", [])
    )

    # apply transformations
    transformed_content = apply_text_transformations(
        content=content,
        transformations= config.get("text_transformations", {}),
        separators=config.get("block_separators", {})
    )

    # generate final content with TOC (table of contents)
    final_text = ""
    if config.get("include_toc"):
        toc = generate_toc(content)
        final_text += toc + "\n\n"
    final_text += transformed_content

    # use tempfile before moving to final path
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{config['format']}") as tmp_file:
        tmp_path = tmp_file.name
        export_to_format(
            text=final_text,
            output_path=tmp_path,
            format=config["format"],
            title=title,
            author=autor,
        )

    # read output path from settings
    with open(os.path.join(project_root, "settings.json"), encoding="utf-8") as f:
        project_settings = json.load(f)
    export_dir = project_settings.get("default_export_path", "/exports")
    os.makedirs(export_dir, exist_ok=True)
    final_output_path = os.path.join(export_dir, os.path.basename(tmp_path))
    os.replace(tmp_path, final_output_path)

    return final_output_path

def generate_toc(content):
    lines = ["# Table of Contents"]
    for chapter in content:
        lines.append(f"- {chapter['title']}")
        for scene in chapter.get("scenes", []):
            lines.append(f"  - {scene['title']}")
    return "\n".join(lines)
