# libRoom
A writing software.
More than a rich text processor, libRoom seeks to meet the needs of writing and managing narrative projects by using a local database customized for each user. Therefore, it is aimed at writers and poets.

## Commands to work with the backend
Abrir la consola, ejecutar los siguientes comandos: 

cd libRoom (para abrir el proyecto global, que incluye tanto el frontend como el backend).

cd libRoom_backend

pip install -r requirements.txt <!--en este documento se listan todas las liberías que se utilizarán en este proyecto, en el mismo se deben incluir las librerías que se vayan instalando en el futuro -->

pip freeze > requirements.txt <!--requirements.txt para actualizarlo cada vez que se instala una nueva librería -->

<!-- traducir antes de entregar el repositorio -->


### Apps
Lo que debe hacer cada app de django. Las apps no tendrán vista o template, debido a que se encargarán únicamente de gestionar los datos. Para saber qué funciones debe llevar a cabo un app, continuar leyendo y revisar el prototipo en Figma.

#### projects app
Responsabilidad: Gestiona las obras/libros/novelas. Gestión de metadatos generales de la obra (título, subtítulo, autor). 
Incluye creación a partir de plantillas, carpetas asociadas, archivos base (incluyendo los utilizados por el resto de apps)
Modelos sugeridos: Work, WorkTemplate, WorkSettings, WorkFolderStructure

#### characters app
Creación y gestión de las fichas de personaje.
Modelos sugeridos: Character, CharacterTrait, Relationship.

#### worldbuilding app 
Creación y gestión de las fichas sobre el mundo (historia, cultura, clima, objetos).
Modelos: Place, Culture, Object, Event...

#### outline app
Árbol de capítulos y escenas.
Esta app debe trabajar en conjunto con *projects*, gestionando y administrando los archivos y carpetas creados por esta, enviándolos al frontend para que el usuario pueda verlos.
Responsabilidad: Esquema estructural: capítulos, escenas, árbol de la historia. 
Modelos: Chapter, Scene, PlotPoint, OutlineNode...

#### editor app
Responsabilidad: Editor de texto enriquecido, navegación por escenas, selección de POV, anotaciones.
Altera y actualiza los archivos creados por *projects* a partir de las acciones indicadas por los archivos. Para que esta app sepa dónde están los archivos, *outline* debe enviarle dichos datos.

#### notes app
Para crear y gestionar notas sueltas o asociadas a capítulos, escenas, personajes, mundo.
Modelos: Note, NoteLink, NoteTag.

#### preferences app
Responsabilidad: Configuración de la app a nivel usuario.
Modelo: UserPreferences, incluir otros de ser necesario

#### exporter
Responsabilidad: Exportación a .docx, .epub, .md, .pdf, etc.
De ser posible, añadirle pandoc.

#### settingsmanager app
Responsabilidad: Configuración de rutas, carpetas de trabajo, configuración interna del programa (no estética).

## File system
- outline #lo incluido dentro de esta carpeta dependerá de la plantilla#
	- Libros #cotiene las subcarpetas secciones"
		- Secciones #contendrá las subcarpetas capítulos, esta carpeta existe de manera opcional#
			- Capítulos #contendrá los markdown de las escenas#
- world #contiene información esencial para el usuario#
	- lugares
	- objetos
	- ciudades
	- regiones
	- planetas
	- facciones
		- equipo militar
		- equipo civil
- chracters
- tags.txt #almacena los colores de las etiquetas de estado#
- plots.txt #almacena las etiquetas de las tramas#
- summary.txt #almacena el resumen de la historia
- notas # carpeta de notas
- lib_room.json #almacena el título y datos de la obra y el autor, además de permitirle al programa encontrar los archivos relacionados a est
