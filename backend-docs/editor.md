# editor app - structure and operation

Es el editor de escenas propiamente dicho, se encarga de editar y administrar el contenido narrativo de las escenas de un proyecto. Opera directamente sobre los archivos .md de escena y expone endpoints que permiten modificar tanto el texto como actualizar los metadatos relacionados.

# nav
Volver al inicio:
[Index](index.md)

Anterior:
[Outline](outline.md)

Siguiente:
[Notes](notes.md)


## objectives
- Leer, editar y guardar el contenido de una escena específica.
- Editar metatados asociados a una escena (POV, status, title, setGoal, etc.). Asociando el POV de un personaje (el id del personaje) al campo POV de la escena.
- Obtener información del personaje asignado a la escena (POV).
- Permitir funcionalidades de búsqueda goblal (world, outline, notes...) a partir de los tags asociados en cada archivo .json dentro de las carpetas world, notes.
- Posibilitar el renombramiento de escenas y capítulos.

## paths almacenados en settings.py
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECTS_BASE_DIR = BASE_DIR / "user" / "projects"
CURRENT_PROJECT_PATH = PROJECTS_BASE_DIR / "current"
PROJECT_JSON_PATH = CURRENT_PROJECT_PATH / "project.json"

CURRENT_PROJECT_PATH = str (CURRENT_PROJECT_PATH) # para importar "from libRoom_backend.settings import PROJECT_JSON_PATH"

## File system
-project
    - outline/ #lo incluido dentro de esta carpeta dependerá de la plantilla#
        - capítulos/  #contendrá los markdown de las escenas
                - scene.md #markdown de cada escena#
    - world/ #contiene información esencial para el usuario#
        - world.json # índice de archivos de world, contiene información para ubicar cada archivo, incluyendo su id (plc-000 para places, obj-000 para objetos, cit-000 para ciudades, cus-000 para archivos custom)
        - places
        - objects
        - cities
        - other/ otros, aquí se guardan los archivos cus-000
    - characters/
        -characters_list.json
        - character_name.md
    - tags.txt #almacena las etiquetas de estado y sus colores#
    - plots.txt #almacena las etiquetas de las tramas#
    - summary.txt #almacena el resumen de la historia
    - notas/ # carpeta de notas
        - notes.json # índice de notas (los id de las notas tienen este formato : nt-000)
    - project.json #almacena el título y datos de la obra y el autor, además de permitirle al programa encontrar los archivos relacionados a esta (todos los archivos listados arriba de este archivo)

### project.json

      {
        "title": "",
        "author": "",
        "created": "dd-mm-yyyy",
        "outline_path": "outline/", (aquí dentro se encuentras las carpetas de los capítulos(chapter_X/), cada carpeta tiene un chapter.md, con la lista de id de scenas en un campo scenes_ids)
        "characters_path": characters/ (aquí se encuentra el characters_list.json)
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

### charactes_list.json
    [
            {
            "id": "char-001",
            "name": "Mark",
            type "main",
            "path": "characters/Mark.md"
        },
        {
            "id": "char-002",
            "name": "Loise",
            "type": "secondary",
            "path": "characters/Loise.md"
        }
    ]

## data
- *characters* app: Nombres de personajes + IDs desde characters_list.json.
- *outline* app: capítulos y escenas relacionadas desde chapter.md
- *project* app: metadatos generales del proyecto, objetivos desde project.json, etiquetas, trama desde tags.txt y plots.txt
- Las opcines de status se consumen desde tags.txt

## integration and dependencies

- Depende del archivo project.json.
- Trabaja directamente sobre la carpeta outline/:
    - chapters/
        - chapter_x/
            - chapter.md
            - scene_x.md
- Envía rutas y metadatos a la app *editor*.

## folder structure
estructura del folder outline, desde dónde el editor debe consumir para editar el contenido.
    outline/
    ├── chapters/
    │   ├── chapter_1/
    │   │   ├── chapter.md
    │   │   ├── scene_1.md
    │   │   └── scene_2.md
    │   └── chapter_2/
    │       ├── chapter.md
    │       └── scene_3.md

## chapter.md

    title: Capítulo I
    ID: ch-001
    type: folder
    label: 3
    status: draft
    compile: 2
    setGoal: 4500
    wordCount: 2396
    scenes_ids: ["scn-001", "scn-002"...]


## scene_x.md structure
ver [Project](project.md)

    title: 
    ID: scn-001
    type: md
    POV: char-004
    label: 4
    status: draft
    compile: 2
    setGoal: 1500
    wordCOunt: 7350
    # sobreescribir solo de aquí en adelante, sin duplicar ni romper metadatos.

## key operations

Añadir más operaciones de ser necesarias

    GET /editor/scenes/{id}/
Retorna contenido completo de una escena (metadatos + narrativa).

    PATCH /editor/scenes/{id}/
Actualiza el contenido narrativo o los metadatados de una escena

    PATCH /editor/scenes/{id}/goal/ 
Cambia el objetivo de palabras (setGoal)

    GET /editor/search/ 
Búsqueda global de contenido.

    PATCH /editor/rename/scene/ 
renombre una escena (archivo y título).

    PATCH /editor/rename/chapter/ 
Renombra un artículo completo


## drf-spectacular example
    from drf_spectacular.utils import extend_schema
    from rest_framework.views import APIView
    from rest_framework.response import Response

    @extend_schema(
        summary="Obtener una escena por ID",
        responses={200: SceneDetailSerializer},
        tags=["Editor"]
    )
    class SceneRetrieveView(APIView):
        def get(self, request, scene_id):
            ...

    @extend_schema(
        summary="Actualizar contenido y metadatos de una escena",
        request=SceneUpdateSerializer,
        responses={200: SceneDetailSerializer},
        tags=["Editor"]
    )
    class SceneUpdateView(APIView):
        def patch(self, request, scene_id):
            ...

## technical considerations (must include)
El archivo de escena se divide en dos partes a editar: cabecera de metadatos y contenido (content)
- El sistema debe ser capaz de:
    - identificar la línea de separación.
    - sobreescribir solo contenido, preservando la cabecera
- El wordCount debe actualizarse automáticamente al realizar cambios.
- Al cambiar el título o renombrar una escena, también se debe renombrar el archivo en disco.
- Al cambiar el capítulo, debe mover la escena y actualizar el scenes_ids en el chapter.md
- Enviar la cantidad de palabras que se han ido guardando para que el settings y el editor puedan visualizar y para saber cuánto se ha cumplido del objetivo

