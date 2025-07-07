# project-app - structure and operation

Gestiona las obras/libros/novelas. Gestión de metadatos generales de la obra (título, subtítulo, autor). 
Incluye creación a partir de plantillas, carpetas asociadas, archivos base (incluyendo los utilizados por el resto de apps), así como su recuperación cada vez que se inicia la aplicación.

Al crear un nuevo proyecto, se escoge si será una novela o un cuento (este último careciendo de capítulos, teniendo solo escenas), la cantidad de capítulos, de escenas por capítulo y la longitud en palabras de cada escena

# nav
Volver al inicio:
- [Index](index.md)
Anterior:
- [Apps Overview](apps-overview.md)
Siguiente:
- [Characters](characters.md)

## structure of the project.json
Contiene metadatos principales de la obra y referencias a sus archivos internos, necesario para que el sistema almacene y recupere las rutas. Es un archivo núcleo junto a chapter.md y scene_x.md

      {
        "title": "",
        "author": "",
        "created": "dd-mm-yyyy",
        "outline_path": "outline/",
        "characters_path": characters/
        "world_path": "world/",
        "notes_path": "notes/",
        "settings_file": "settings.json",
        "preferences_file": "preferences.json",
        "summary_file": "summary.txt",
        "tags_file": "tags.txt",
        "plots_file": "plots.txt",
        "total_words_goal": "0000000",
        "words_by_scene": "00000",
        "words_by_chapter": "000000",
        "number_of_chapters": "000",
        "scenes_by_chapter": "00",
      }

    ## resource files

desde estos archivos se toman tanto los colores, como los nombres de ciertas características, llamando únicamente al archivo y leyendo su contenido.

### tags.txt
    draft: #FFDD00
    reviewed: #00DDFF
    final: #00FF00

### plots.txt
    main_plot: Trama principal
    subplot1: Conflicto político
    subplot2: Romance entre aliados

### summary.txt
Resumen breve de la historia, visible en Flutter para facilitar navegación y exportación.

## core files

### chapter.md
Archivo de cada capítulo (va dentro de cada carpeta de capítulo):

    title: Capítulo I
    ID: ch-000
    type: folder
    label: 3
    status: draft
    compile: 1
    setGoal: 4500
    wordCount: 2396
    scenes_id: ["scn-001, "scn-002"]

### scene_x.md
Escena individual (están dentro de cada carpeta capítulo):
    title: 
    ID: scn-001
    type: md
    POV: char-004
    label: 4
    status: draft
    compile: 2
    setGoal: 1500
    wordCount: 1350

# libraries
os, shutil, pathlib: Crear carpetas, archivos y manejar rutas locales.
markdown2 o mistune	Leer/parsing de archivos Markdown.
json	Leer y escribir project.json.
PyFilesystem2 (opcional)	Manejar filesystem.
watchdog (opcional)	Para detectar cambios en archivos y sincronizar automáticamente.