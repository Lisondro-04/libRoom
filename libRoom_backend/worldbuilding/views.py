from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from drf_spectacular.utils import extend_schema, OpenApiTypes
from .serializers import WorldIndexSerializer, NewEntrySerializer
from .world_manager import WorldManager
from serializers import serializers
from .world_manager import WorldManager
import json
import os

wm = WorldManager()

def get_world_root():
    try:
        with open(wm, 'r', encoding='utf-8') as f:
            project_data = json.load(f)
        return project_data.get('world_path', 'world')
    except Exception:
        return 'world'

wm = WorldManager(get_world_root())

class WorldIndexView(APIView):

    @extend_schema(
        summary="Obtener world.json índice",
        responses={200: WorldIndexSerializer}
    )
    def get(self, request):
        index = wm.get_index()
        return Response(index)

    @extend_schema(
        summary="Crear world.json y carpetas iniciales",
        responses={201: WorldIndexSerializer}
    )
    def post(self, request):
        wm.ensure_structure()
        return Response(wm.get_index(), status=status.HTTP_201_CREATED)


class WorldAddEntryView(APIView):

    @extend_schema(
        summary="Agregar nueva entrada .md a worldbuilding",
        request=NewEntrySerializer,
        responses={201: WorldIndexSerializer}
    )
    def post(self, request):
        serializer = NewEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            entry = wm.create_entry(data['category'], data['title'])
            return Response(entry, status=status.HTTP_201_CREATED)
        except FileExistsError as e:
            raise ValidationError(str(e))


class WorldEntryDetailView(APIView):

    @extend_schema(
        summary="Obtener contenido markdown de un archivo específico",
        responses={200: OpenApiTypes.STR}
    )
    def get(self, request, category, id):
        try:
            content = wm.read_entry(category, id)
            return Response(content)
        except FileNotFoundError:
            raise NotFound("Archivo no hallado")

    @extend_schema(
        summary="Eliminar una entrada del worldbuilding",
        responses={204: None}
    )
    def delete(self, request, category, id):
        try:
            wm.delete_entry(category, id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except FileNotFoundError:
            raise NotFound("Archivo no encontrado")


class WorldEntrySectionEditView(APIView):

    @extend_schema(
        summary="Editar sección específica de un archivo markdown",
        request=serializers.Serializer,  # Se espera {'content': str, 'section': str}
        responses={200: OpenApiTypes.STR}
    )
    def patch(self, request, category, id):
        content = request.data.get('content')
        section = request.data.get('section')
        if not content or not section:
            raise ValidationError("Faltan 'content' o 'section' en la petición.")

        try:
            wm.write_section(category, id, section, content)
            updated_content = wm.read_entry(category, id)
            return Response(updated_content)
        except FileNotFoundError:
            raise NotFound("Archivo no encontrado")
