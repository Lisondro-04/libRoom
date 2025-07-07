# notes app - structure and operation

Gestiona las notas auxiliares de escritura creadas por el usuario. Permite crear, editar, asociar y clasificar notas relacionadas con escenas, capítulos, entidades de worldbuilding o como notas globales.

# nav
Volver al inicio:
[Index](index.md)

Anterior:
[Editor](editor.md)

Siguiente:
[Exporter](exporter.md)

## objectives
- Crear notas con un id único.
- Asociar notas con escenas, capítulos, entidades del mundo u otras entidades definidas.
- Editar el contenido y metadatos de la nota.
- Eliminar notas.
- Filtrar/ordenar por tipo de asociación.
- Mostrar longitud en palabras de cada nota.
- Buscar y recuperar notas por tag de asociación.

## folder structure

    notes/
    │
    ├── notes_index.json   # índice global de todas las notas con sus metadatos
    ├── nt-001.md          # nota individual
    ├── nt-002.md
    ├── ...

## notes_index structure

|**campo**    |  **tipo**     | **descripción**|
|---           |  ----          |-----
|id            |   str          |   identificador único de la nota (nt-000)|
|title         |  str          |   título de la nota|
|linked_to:    |  object        |  información de asociación: *type*: tipo de entidad (blg-scn, blg-wrld, blg-ch, glob). target_id:   ID exacto de la entidad asociada |(o *null* si es global) |
|word_count    | int           |  número de palabras de la nota |
|created_at    | datetime      |  Fecha de creación (ISO 8601) |
|updated_at    | datetime      |  Fecha de última edición|

    {
    "notes": [
        {
        "id": "nt-001",
        "title": "Introducción de antagonista",
        "linked_to": {
            "type": "blg-scn",
            "target_id": "scn-003"
        },
        "word_count": 264,
        "created_at": "2025-07-06T14:32:00",
        "updated_at": "2025-07-06T15:10:20"
        },
        {
        "id": "nt-002",
        "title": "Religión en el Mundo Roto",
        "linked_to": {
            "type": "blg-wrld",
            "target_id": "wrld-005"
        },
        "word_count": 578,
        "created_at": "2025-07-06T15:25:30",
        "updated_at": "2025-07-06T16:00:01"
        },
        {
        "id": "nt-003",
        "title": "Ideas sueltas para final alternativo",
        "linked_to": {
            "type": "glob",
            "target_id": null
        },
        "word_count": 127,
        "created_at": "2025-07-06T17:15:45",
        "updated_at": "2025-07-06T17:15:45"
        }
    ]
    }

## nt-000.md file 
(nt = note)

    ID: nt-001
    title: Detalles de la Ciudad Roja
    type: note
    linked_to: blg-wrld|wrld-004
    wordCount: 143
    ->contenido de la nota aquí...

## asociations
- blg = belongs, ch = chapters, scn = scene, wrld = world, glob = global.
- Capítulo: blg-ch -> asociación con un capítulo específico.
- Escena: blg-scn -> asociación con una escena específica.
- Worldbuilding: blg-wrld -> asociación con un objeto de worldbuilding.
- Global: glob -> nota general, sin asociación directa.

## key functions

    GET /notes/ 
Listar todas las notas o filtradas por tipo

    POST /notes/ 
Crear nueva nota

    PATCH /notes/{note_id}/
Obtener el contenido completo de una nota.

    DELETE /notes/{note_id}
Eliminar nota

    GET /notes/by-tag/{tag}/ 
Obtener notas por tipo de asociación (blg-ch)

Documentar para el drf-spectacular (ver documentación pertinente)

## drf-spectacular examples

### serializer
    class NoteSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    linked_to = serializers.CharField()
    content = serializers.CharField()

### view
    from drf_spectacular.utils import extend_schema

    @extend_schema(
        summary="Crear nueva nota",
        request=NoteSerializer,
        responses={201: NoteSerializer},
        tags=["Notes"]
    )
    class NoteCreateView(APIView):
        def post(self, request):
            ...

## technical considerations
- El id de cada nota se genera automáticamente con el formato nt-000 de forma incremental
- Las asociasiones son tags que indican el tipo de vínculo + id del elemento relacionado, ej: blg-scn|scn-003.
- El contenido se guarda en .md y los metadatos se registran también en notes_index.json
- Al editar una nota, se debe actualizar tanto el .md como el index.
- El recuento de palabras se calcula al guardar o consultar la nota.
- Los filtros por asociación permiten organizar el flujo en el frontend (ej: ver solo las notas de una escena).

