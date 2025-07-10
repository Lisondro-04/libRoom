from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import SettingsSerializer
from .utils import read_settings, save_settings, validate_and_prepare

class SettingsView(APIView):

    @extend_schema(
        summary="Obtener configuraciones",
        description="Devuelve las configuraciones actuales desde settings.json",
        responses={200: SettingsSerializer},
        tags=["Settings"]
    )
    def get(self, request):
        settings_data = read_settings()
        serializer = SettingsSerializer(settings_data)
        return Response(serializer.data)

    @extend_schema(
        summary="Actualizar configuraciones",
        description="Modifica y guarda las configuraciones en settings.json, validando sus valores",
        request=SettingsSerializer,
        responses={200: SettingsSerializer},
        tags=["Settings"]
    )
    def put(self, request):
        serializer = SettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Validar y preparar los datos antes de guardar
        try:
            validated_data = validate_and_prepare(serializer.validated_data)
        except ValueError as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        save_settings(validated_data)
        return Response({"success": True, "message": "Configuraciones actualizadas correctamente.", "data": validated_data})
