# exporter app - structure and operation

Se encarga de transformar y exportar el contenido del proyecto (capítulos, escenas), en múltiples formatos, con configuraciones personalizables relacionadas con contenido, estilo, estructura y formato de salida.

# nav
Volver al inicio:
[Index](index.md)

Anterior:
[Notes](notes.md)

Siguiente:
[Settings](settings.md)

## main functionalities

- Exportación en múltiples formatos:
txt, md, docx, odt, pdf (usando pando u otros)
- Filtros de contenido exportado:
 - Incluir capítulos, escenas u otros niveles.
 - Filtrar por estado de escena o capítulo (ej, solo finalizados)
 - Ignorar escenas o capítulos con status < N.
- Personalización de contenido:
  - Transformación de caracteres (comillas, guiones, etc).
  - Eliminación de espacios múltiples.
  - Reemplazos personalizados, por ejemplo --- → —.
  - Configuración de separación entre bloques (\n, ###, etc).
- Generación de tabla de contenido (índice) según estructura jerárquica.
- Definición del directorio de salida leído desde settings.json > default_export_path.

## sugested endpoints

    POST /api/export/
    {
    "format": "pdf",
    "include_chapters": true,
    "include_scenes": true,
    "status_filter": [2, 3],
    "text_transformations": {
        "double_quotes": ["\"", "«»"],
        "single_quotes": ["'", "‹›"],
        "long_dash": "---",
        "custom_replacements": {
        "[...]": "…"
        },
        "remove_multiple_spaces": true
    },
    "block_separators": {
        "between_chapters": "\n\n",
        "between_chapter_and_scene": "---",
        "between_scenes": "\n\n"
    },
    "include_toc": true
    }

respuesta

    {
    "success": true,
    "message": "Exportación completada.",
    "output_path": "C:/Users/usuario/exports/project_01.pdf"
    }

## drf-spectacular

    from drf_spectacular.utils import extend_schema, OpenApiExample
    from rest_framework.views import APIView
    from rest_framework.response import Response

    class ExportProjectView(APIView):
        @extend_schema(
            summary="Exportar contenido del proyecto",
            description="Exporta el contenido del proyecto en el formato especificado, con filtros de estado y transformaciones personalizadas.",
            request=ExportConfigSerializer,
            responses={200: ExportResponseSerializer}
        )
        def post(self, request):
            # lógica de exportación
            return Response(...)

## technical considerations
- Usar una carpeta temporal (tempfile) antes de mover el archivo final al default_export_path.
