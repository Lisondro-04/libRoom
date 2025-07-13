from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .serializers import PreferencesSerializer
from .utils import read_preferences, write_preferences, update_total_words_goal_in_project

class PreferencesView(APIView):

    @extend_schema(
        summary="Obtener preferencias del usuario",
        description="Devuelve las configuraciones actuales desde preferences.json",
        responses={200: PreferencesSerializer}
    )
    def get(self, request):
        prefs = read_preferences()
        return Response(prefs)

    @extend_schema(
        summary="Actualizar preferencias",
        description="Modifica y guarda las preferencias en preferences.json y actualiza project.json si es necesario.",
        request=PreferencesSerializer,
        responses={200: PreferencesSerializer}
    )
    def put(self, request):
        serializer = PreferencesSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            write_preferences(data)
            update_total_words_goal_in_project(data['total_words_goal'])
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
