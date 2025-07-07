# settings app - structure and operation

Permite al usuario leer, modificar y guardar configuraciones generales del entorno de escritura, centralizadas en settings.json.

Consume la ruta del archivo settings.json desde project.json, y se encarga de mantenerlo actualizado ante cualquier cambio solicitado desde el frontend.

# nav

Volver al inicio:
[Index](index.md)

Anterior:
[Exporter](exporter.md)

Siguiente:
[Preferences](preferences.md)

## objective

- acceder al archivo settings.json para leer, modificar y persistir configuraciones.
- comunicar estos datos al frontend (flutter) y aceptar actualizaciones desde allí.
- Validar los valores de configuración antes de guardar

Documentar para el drf-spectacular (ver documentación pertinente)

## settings.json structure

    {
    "language": "es",  // Opciones: "es", "en-US"
    "ui_font": "Roboto",
    "ui_font_size": 14,
    "default_project_path": "C:/Users/user/Documents/libRoomProjects",
    "autosave_frequency": "5min",  // Opciones: "off", "1min", "5min", "10min", "on_change"
    "default_export_path": "C:/Users/user/Documents/exports",
    "cloud_sync_path": "OneDrive",
    "cloud_autosave_frequency": "10min"  // Opciones similares
    }

## endopoints

    GET /api/settings/
Retorna las configuraciones actuales del usuario

    PUT /api/settings/
Actualiza configuraciones del entorno

### request example

    {
    "language": "en-US",
    "ui_font": "Open Sans",
    "ui_font_size": 16,
    "autosave_frequency": "on_change",
    "cloud_autosave_frequency": "5min"
    }

#### answer
    {
    "success": true,
    "message": "Configuraciones actualizadas correctamente."
    }

## drf-spectacular
    from drf_spectacular.utils import extend_schema
    from rest_framework.views import APIView
    from rest_framework.response import Response
    from .serializers import SettingsSerializer

    class SettingsView(APIView):
        
        @extend_schema(
            summary="Obtener configuraciones",
            description="Devuelve las configuraciones actuales desde el archivo settings.json",
            responses={200: SettingsSerializer}
        )
        def get(self, request):
            # Lógica para leer settings.json
            ...

        @extend_schema(
            summary="Actualizar configuraciones",
            description="Modifica y guarda las configuraciones en settings.json",
            request=SettingsSerializer,
            responses={200: SettingsSerializer}
        )
        def put(self, request):
            # Lógica para actualizar settings.json
            ...


## final considerations
- Validar que las rutas recibidas existan  o crea las carpetas necesarias.
- Proteger la lectura/escritura concurrente con locks o atomic operations.



