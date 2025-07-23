from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import SettingsSerializer
from . import utils

class SettingsView(APIView):

    @extend_schema(
        summary="Obtener configuraciones",
        description="Devuelve las configuraciones actuales desde settings.json",
        responses={200: SettingsSerializer}
    )
    def get(self, request):
        base_path = request.query_params.get("base_path")
        if not base_path:
            return Response({"error": "base_path es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        settings = utils.read_settings(base_path)
        return Response(settings, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Actualizar configuraciones",
        description="Modifica y guarda las configuraciones en settings.json",
        request=SettingsSerializer,
        responses={200: SettingsSerializer}
    )
    def put(self, request):
        base_path = request.data.get("base_path")
        if not base_path:
            return Response({"error": "base_path es requerido"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SettingsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_data = serializer.validated_data

        # Validar y crear rutas si no existen
        utils.validate_and_create_paths(updated_data)

        # Guardar en settings.json
        utils.write_settings(base_path, updated_data)
        
        return Response({
            "success": True,
            "message": "Configuraciones actualizadas correctamente.",
            "data": updated_data
        }, status=status.HTTP_200_OK)
