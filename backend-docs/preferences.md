# preferences app - structure and operation

Permite al usuario personalizar aspectos del comportamiento visual y funcional del entorno de escritura, a través del archivo preferences.json, cuya ruta se obtiene desde project.json.

Estas preferencias afectan directamente el frontend (Flutter), pero son gestionadas, persistidas y enviadas desde el backend Django.

# nav
Volver al inicio:
[Index](index.md)

Anterior:
[Settings](settings.md)

Siguiente:
[DRF-SPECTACULAR](drf-spectacular.md)


## objectives
- Leer y actualizar preferences.json.
- Recibir las preferencias desde el frontend y enviarlas nuevamente para aplicación visual.
- Enviar la configuración actual para permitir la personalización.
- Modificar campos adicionales como total_words_goal en project.json.

## preferencies

- escoger el tema (claro, oscuro, predeterminado del sistema).
- fuente del editor 
- tamaño de fuente del editor
- skin: escoger entre las preconfiguradas por el equipo de desarrollo. Estas son opciones que deben enviar al frontend para que este haga los cambios.
- configurar el objetivo global, al modificar el campo total_words_goal del project.json.
- configurar objetivo por sesión de escritura, consumiendo cuántas palabras se han guardado en el editor durante la sesión.

## preferences.json structure

    {
        "theme": "dark-theme" // opciones: light-theme, dark-theme, system-default
        "editor_font": "Times New Roman"
        "font_size": "12",
        "skin": "coffee-talk" //opciones: among-us, walter-white, coffe-talk, among-us, etc.
        "total_words_goal": "65000", // también debe actualizar project.json
        "session_goal": "3000",
        "focus_button": "on", // permite o no pantalla completa en el frontend.
        "show_lateral_menu": "on", //"on" / "off" - menú lateral en el frontend.
        "auto_spell_check": "on", //"on" / "off"- correción automática en el editor del frontend.
        "global_tips": "on", //"on" / "off"-activa o desactiva los consejos de uso y escritura en el frontend.
    }

## project.json integration
Se debe consumir la ruta del proyecto desde project.json para encontrar el archivo preferences.json.

El campo total_words_goal debe sincronizarse con el mismo campo en project.json.

## API REST - endpoints

    GET /api/preferences/
Devuelve las preferencias actuales del usuario.

    PUT /api/preferences/
Actualiza el archivo preferences.json con los datos proporcionados por el frontend. Si *total_words_goals* cambia, debe actualizarse el *project.json*


## DRF Spectacular 
usar en los views @extend_schema para documentar claramente en Swagger:

    from drf_spectacular.utils import extend_schema
    from rest_framework.views import APIView
    from rest_framework.response import Response
    from .serializers import PreferencesSerializer

    class PreferencesView(APIView):

        @extend_schema(
            summary="Obtener preferencias del usuario",
            description="Devuelve las configuraciones actuales desde preferences.json",
            responses={200: PreferencesSerializer}
        )
        def get(self, request):
            # lógica para leer preferences.json
            ...

        @extend_schema(
            summary="Actualizar preferencias",
            description="Modifica y guarda las preferencias en preferences.json y actualiza project.json si es necesario.",
            request=PreferencesSerializer,
            responses={200: PreferencesSerializer}
        )
        def put(self, request):
            # lógica para actualizar preferences.json y sincronizar
            ...

Documentar para el drf-spectacular (ver documentación pertinente)

