# apps overview

Lo que debe hacer cada app de django. Las apps no tendrán vista o template, debido a que se encargarán únicamente de gestionar los datos. Para saber qué funciones debe llevar a cabo un app, continuar leyendo y revisar el prototipo en Figma.

# nav
Volver al inicio:
- [Index](index.md)

Siguiente:
- [Projects](project.md)

## projects app
Responsabilidad: Gestiona las obras/libros/novelas. Gestión de metadatos generales de la obra (título, subtítulo, autor). 
Incluye creación a partir de plantillas, carpetas asociadas, archivos base (incluyendo los utilizados por el resto de apps)
Modelos sugeridos: Work, WorkTemplate, WorkSettings, WorkFolderStructure

## characters app
Creación y gestión de las fichas de personaje.
Modelos sugeridos: Character, CharacterTrait, Relationship.

## worldbuilding app 
Creación y gestión de las fichas sobre el mundo (historia, cultura, clima, objetos).
Modelos: Place, Culture, Object, Event...

## outline app
Árbol de capítulos y escenas.
Esta app debe trabajar en conjunto con *projects*, gestionando y administrando los archivos y carpetas creados por esta, enviándolos al frontend para que el usuario pueda verlos.
Responsabilidad: Esquema estructural: capítulos, escenas, árbol de la historia. 
Modelos: Chapter, Scene, PlotPoint, OutlineNode...

## editor app
Responsabilidad: Editor de texto enriquecido, navegación por escenas, selección de POV, anotaciones.
Altera y actualiza los archivos creados por *projects* a partir de las acciones indicadas por los archivos. Para que esta app sepa dónde están los archivos, *outline* debe enviarle dichos datos.

## notes app
Para crear y gestionar notas sueltas o asociadas a capítulos, escenas, personajes, mundo.
Modelos: Note, NoteLink, NoteTag.

## preferences app
Responsabilidad: Configuración de la app a nivel usuario.
Modelo: UserPreferences, incluir otros de ser necesario

## exporter
Responsabilidad: Exportación a .docx, .epub, .md, .pdf, etc.
De ser posible, añadirle pandoc.

## settingsmanager app
Responsabilidad: Configuración de rutas, carpetas de trabajo, configuración interna del programa (no estética).

## File system
-project
    - outline/ #lo incluido dentro de esta carpeta dependerá de la plantilla#
        - capítulos/  #contendrá los markdown de las escenas
                -chapter.md #índice de escenas, datos del capítulo 
                -scene.md #markdown de cada escena#
    - world/ #contiene información esencial para el usuario#
        - world.json # índice de archivos de world, contiene información para ubicar cada archivo, incluyendo su id (plc-000 para places, obj-000 para objetos, cit-000 para ciudades, cus-000 para archivos custom)
        - places
        - objects
        - cities
        - other/ #otros, aquí se guardan los archivos cus-000
    - characters/
        -characters_list.json
        -character_name.md
    - tags.txt #almacena las etiquetas de estado y sus colores#
    - plots.txt #almacena las etiquetas de las tramas#
    - summary.txt #almacena el resumen de la historia
    - notes/ # carpeta de notas
        - notes.json # índice de notas (los id de las notas tienen este formato : nt-000)
        -notexxx.md
    - project.json #almacena el título y datos de la obra y el autor, además de permitirle al programa encontrar los archivos relacionados a esta (todos los archivos listados arriba de este archivo).
