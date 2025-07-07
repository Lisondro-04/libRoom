# characters app - structure and operation
Esta app se encarga de la creación, gestión y edición de las fichas de personaje.

# nav
Volver al inicio:
[Index](index.md)
Anterior:
[Characters](characters.md)
Siguiente:
[Worldbuilding](worldbuilding.md)

# how-it-should-be

## objectives

- crear personaje (principal o secundario).
- Almacenar su información en archivos markdown.
- Editar secciones específicas de dichos archivos desde el frontend.
- Enviar y recibir datos estructurados desde y hacia el backend para actualizar y mostrar las fichas.

## file intregation

Esta app depende del archivo project.json generado por la app *project* para conocer las rutas y estructuras del proyecto actual.

Los archivos de personaje se almacenan en project/characters/character_name.md

Además, se mantiene un índice de personajes por id en project/characters/character_list.json

### character_list.json estructure
Almacena un listado con los ID y rutas de todos los personajes creados.
Se utilizara para:
- Mostrar una lista de personajes en el editor de personajes.
- Seleccionar un personaje como POV en *editor*.

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

## editing by section
En el editor del frontend (gestionado por la app *editor*), se puede seleccionar una sección específica del archivo (por ejemplo: "Bacground"), y:
- Sobreescribir el contenido de esa sección (sin duplicar).
- Leer y mostrar el contenido actual para edición.

Este comportamiento debe ser sincronizado con el backend usando endpoints apropiados, como:
    PATCH /characters/{id}/section/

# key operations

    POST /characters/
Crear un nuevo personaje, genera el archivo .md y lo registra en characters_list.json

    GET /characters/ 
Listar todos los personajes registrados en character_list.json

    GET /characters/{id}/ 
Obtener el contenido completo del archivo .md de un personaje.

    PATCH /characters/{id}/section/
Editar solo una sección específica del archivo (por título).

    DELETE /characters/{id}/
Eliminar un personaje (archivo .md y su entrada en el characters_list.json).

### character_name.md structure

    Name:                
    ID: un número aleatorio de cuatro caracteres
    path:  characters/character_name       
    type: main, secondary      
    POV: bool                 
    Color:  
    # Genereal Info
    # Physical Appareance
    # Personality
    # Background
    # Motivations-Conflicts
    # Skills and Talents
    # Relationships
    #Other

# Documentar para el drf-spectacular
Cada vista debe incluir docstrings y/o usar @extend_schema para que la documentación sea clara, ejemplo

    from drf_spectacular.utils import extend_schema
    from rest_framework.views import APIView

    class CharacterDetailView(APIView):
        """
        Recupera o actualiza una ficha de personaje por ID.
        """

        @extend_schema(
            description="Devuelve los datos de un personaje específico en formato markdown estructurado.",
            responses={200: OpenApiTypes.STR}
        )
        def get(self, request, id):
            ...


