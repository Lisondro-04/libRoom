from django.shortcuts import render
import json
import os
from pathlib import Path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import ProjectSerializer, ProjectCreationSerializer
from .project_initializer import (
    create_base_files,
    generate_project_json,
    create_chapter_scene_structure,
)
from .utils import get_project_json

PROJECT_ROOT= Path ("/user/projects/") # cambia a la raíz real
CURRENT_PROJECT = PROJECT_ROOT / "current" # puede actualizarse dinámicamente
PROJECT_PATH = CURRENT_PROJECT # alias para otras vistas
class CreateProjectView(APIView):
    @extend_schema(
        summary="Crear un nuevo proyecto",
        request=ProjectCreationSerializer,
        responses={201: ProjectSerializer}
    )
    def post(self, request):
        data = request.data

        CURRENT_PROJECT.mkdir(parents=True, exist_ok=True)

        create_base_files(CURRENT_PROJECT)
        generate_project_json(CURRENT_PROJECT, data)

        if data['type'] == "novel":
            create_chapter_scene_structure(CURRENT_PROJECT, data['number_of_chapters'], data['scenes_by_chapter'], data['words_by_scene'])
        elif data['type']== "short_story":
            #en caso de cuento, solo escenas, sin estructura por capítulos
            create_chapter_scene_structure(CURRENT_PROJECT, 1, data['scenes_by_chapter'], data['words_by_scene'])

        with open(CURRENT_PROJECT / "project.json") as f:
            result = json.load(f)
        return Response(result, status=201)

class ProjectView(APIView):

    @extend_schema(
        summary="Obtener datos del proyecto",
        responses={200: ProjectSerializer}
    )

    def get(self, request):
        with open(PROJECT_ROOT / "project.json") as f:
            data = json.load(f)
            return Response(data)
        
    @extend_schema(
        summary="Actualizar project.json",
        request=ProjectSerializer,
        responses={200: ProjectSerializer}
    )
    def put(self, request):
        data = request.data
        with open(PROJECT_ROOT / "project.json", "w") as f:
            json.dump(data, f, indent=2)
        return Response(data)
    

class ReloadProjectView(APIView):
    @extend_schema(
        summary="Recargar el archivo project.json",
        responses={200: "project.json cargado correctamente", 404: "Archivo no encontrado"}
    )
    def get(self, request):
        try:
            data = get_project_json()
            return Response(data, status=status.HTTP_200_OK)
        except FileNotFoundError:
            return Response({"eror": "project.json no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InitProjectView(APIView):
    """
    Incializa carpetas y archivos básicos para una obra nueva
    """

    @extend_schema(summary="Inicializar proyecto desde plantilla")
    def post(self, request):
        #Crear
        os.makedirs(PROJECT_PATH / "outline", exist_ok=True)
        os.makedirs(PROJECT_PATH / "characters", exist_ok=True)
        os.makedirs(PROJECT_PATH / "world", exist_ok=True)
        os.makedirs(PROJECT_PATH / "notes", exist_ok=True)

        (PROJECT_PATH / "settings.json").write_text('{}')
        (PROJECT_PATH / "preferences.json").write_text('{}')
        (PROJECT_PATH / "summary.txt").write_text('Short summary.')
        (PROJECT_PATH / "tags.txt").write_text('')
        (PROJECT_PATH / "plots.txt").write_text('')

        return Response({"status": "initialized"}, status=201)
    
