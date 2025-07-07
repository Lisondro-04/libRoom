# worldbuilding app - structure and operation

Gestiona toda la información de construcción de mundo en un proyecto: lugares, ciudades, objetos importantes, costumbres, razas, historia.

# objectives
- Crear un world.json como índice del worldbuilding.
- Crear automáticamente subcarpetas iniciales cómo:
	- places/
	- objects/
	- cities/
- Permitir la creación de archivos .md personalizados desde el frontend (ej. "Religions.md" o "Creatures.md").
- Asociar un id a cada entrada para que pueda ser usuada en otras secciones como el editor de escenas, filtros o en la búsqueda global.

## file intregation
Esta app depende del archivo project.json generado por la app *project* para:
- Detectar la carpeta world/.
- Validar la estructura del proyecto.
- Sincronizar datros entre backend y frontend.

### world folder structure
	world/ 
		- places/ dentro de cada uno se crean archivos .md que el usuario nombra y edita.
		- objects/
		- cities/
		- other/ created by the user
		- world.json

### world.json structure
Funciona como índice del worldbuilding, permitiendo ubicar y registrar los archivos de mundo, ejemplo
	{
	"places": [
		{
		"id": "plc-001",
		"title": "Gates of the End",
		"path": "world/places/gates_of_the_end.md"
		}
	],
	"objects": [
		{
		"id": "obj-002",
		"title": "Soul Breaker",
		"path": "world/objects/soul_breaker.md"
		}
	],
	"cities": [],
	"custom": [
		{
		"id": "cus-001",
		"title": "Outer Gods",
		"path": "world/other/creatures.md"
		}
	]
	}

### object.md structure

	Title: Soul Breaker
	ID: obj-002
	Type: object
	Path: world/objects/soul_breaker.md
	Tags: [mythic, archaeotechnology, cursed]

	# Description

	# Origin

	# Abilities

	# Historical Relevance

	# Notes

Las secciones pueden variar por tipo (place, city, creature, etc.), pero deben estar organizadas con encabezados Markdown (#) para que puedan ser modificadas por sección desde el editor.

## editing
Desde el frontend:
- Seleccionar una sección específica (ej: # Description) para su edición.
- El backend extrae el contenido debajo de ese encabezado, lo entrega al frontend y puede sobreescribirlo en la misma posición.

# key operations

	POST /world/ 
Crear el archivo world.json e inicializar carpetas por defecto (mostradas como secciones en el editor).

	POST /world/add/
Crear un nuevo archivo .md en una categoría existente o nueva (custom).

	GET /world/{category}/{id}/
Retorna el contenido de un archivo markdown específico.

	PATCH /world/{category}/{id}/section/ 
Editar una sección del archivo .md

	DELETE /world/{category}/{id}/ 
Eliminar una entrada del worldbuilding.

# drf-spectacular
Cada vista puede documentarse con drf-spectacular para generar especificaciones OpenAPI automáticamente:

	from drf_spectacular.utils import extend_schema

	@extend_schema(
		summary="Obtener detalles de un archivo de worldbuilding",
		description="Devuelve el contenido markdown de un archivo específico como string.",
		responses={200: OpenApiTypes.STR}
	)
	def get(self, request, category: str, id: str):
		...


# nav
Volver al inicio:
[Index](index.md)

Anterior:
[Characters](characters.md)

Siguiente:
[Outline](outline.md)