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
- Editar metatados asociados a una escena (POV, status, title, setGoal, etc.).
- Obetener información del personaje asignado a la escena (POV).
- Permitir funcionalidades de búsqueda goblal (world, outline, notes...).
- Posibilitar el renombramiento de escenas y capítulos.

## data
- *characters* app: Nombres de personajes + IDs desde characters_list.json.
- *outline* app: capítulos y escenas relacionadas desde chapter.md
- *project* app: metadatos generales del proyecto, objetivos desde project.json, etiquetas, trama desde tags.txt y plots.txt
- Las opcines de status se consumen desde tags.txt

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
    charCount: 7350
    #sobreescribir solo de aquí en adelante, sin duplicar ni romper metadatos.

## key operations

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

