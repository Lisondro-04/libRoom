# outline app - structure and operation

Es el árbol de capítulos y escenas. Se encarga de presentar representar y gestionar el árbol estructural del proyecto: capítulos, escenas y jerarquía.

# nav
Volver al inicio:
[Index](index.md)

Anterior:
[Worldbuilding](worldbuilding.md)

Siguiente:
[Editor](editor.md)

## objective

Gestionar y mantener sincronizada la estructura narrativa del proyecto:
- Listado de capítulos y escenas.
- Operaciones de creación, edición, renombramiento, reubicación y eliminación.
- Funciona como intermediario entre:
    - project: manipulación de archivos/folders y actualización del project.json.
    - editor: edición del contenido de escenas.
    - entrega de estructura para renderizado del árbol.
    - editar el objetivo en palabras del capítulo
    - contar la cantidad de palabras actuales.

## integration and dependencies

- Depende del archivo project.json.
- Trabaja directamente sobre la carpeta outline/:
    - chapters/
        - chapter_x/
            - chapter.md
            - scene_x.md
- Envía rutas y metadatos a la app *editor*.

## folder structure

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
    status: draft # status se consume desde el archivo tags.txt en la raíz, (se encuentra en el campo "tags_file" del project.json)
    compile: 2
    setGoal: 4500
    wordCount: 2396
    scenes_ids: ["scn-001", "scn-002"...]

## key operations

    GET /outline/ 
Retorna el árbol estructural.

    POST /outline/chapters/
Crear una nueva escena dentro de un capítulo.

    PATCH /outline/rename/ 
Renombrar un capítulo o escena.

    PATCH /outline/move/
Mover escena entre capítulos.

    DELETE /outline/chapters/{id}/
Eliminar un capítulo (con confirmación)

    DELETE /outline/scenes/{id}/
Eliminar escena específica

    PATCH /outline/scene-meta/ 
Editar metadatos (POV, título, objetivo, etc)

    PATCH /outline/scenes_ids/ 
actualizar el campo scenes_ids en el chapter.md al reordenar escenas.

    PATCH /outline/chapters/chapter/{id}/goal/
Cambiar el objetivo de palabras (setGoal) [comprobar si la escritura de la operación es la correcta].


## drf-spectacular example
    from drf_spectacular.utils import extend_schema
    from rest_framework.views import APIView

    @extend_schema(
        summary="Crear nuevo capítulo",
        request=ChapterCreateSerializer,
        responses={201: ChapterResponseSerializer},
        tags=["Outline"]
    )
    class CreateChapterView(APIView):
        def post(self, request):
            ...

Usa los decoradores de drf-spectacular para cada endpoint con:

summary: descripción corta.

description: más detalles si es necesario.

request: serializer de entrada.

responses: posibles respuestas (serializers o tipos).

## considerations that must be included
Reutiliza la lógica de manejo de archivos de la app project (su creación, etc.)

La creación o movimiento de archivos debe actualizar automáticamente el project.json.

Al mover una escena, se debe:
- Eliminar su ID del capítulo anterior.

- Añadir su ID al campo scenes_ids del capítulo nuevo.

Es importante que los IDs sean únicos y rastreables por otras apps como editor, tags, notes, etc (tienen el siguiente formato: ch-000 para capítulos, scn-000 para escenas)
