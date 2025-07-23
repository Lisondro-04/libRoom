from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from pathlib import Path
import json

from .serializers import ProjectSerializer, ProjectCreationSerializer
from .project_initializer import (
    create_base_files,
    generate_project_json,
    create_chapter_scene_structure,
)
from .utils import get_project_json


class CreateProjectView(APIView):
    serializer_class = ProjectCreationSerializer

    @extend_schema(
        summary="Crear un nuevo proyecto",
        request=ProjectCreationSerializer,
        responses={201: ProjectSerializer}
    )
    def post(self, request):
        data = request.data

        project_name = data.get("title")
        if not project_name:
            return Response({"error": "El campo 'title' es obligatorio"}, status=400)

        custom_dir = data.get("base_path")
        if custom_dir:
            base_path = Path(custom_dir).expanduser().resolve() / project_name
        else:
            base_path = Path.home() / "projects" / project_name  # Ruta por defecto opcional

        try:
            base_path.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            return Response({"error": "El proyecto ya existe en esta ubicación."}, status=400)

        create_base_files(base_path)
        generate_project_json(base_path, data)

        create_chapter_scene_structure(
            base_path,
            data['number_of_chapters'] if data['type'] == 'novel' else 1,
            data['scenes_by_chapter'],
            data['words_by_scene']
        )

        try:
            with open(base_path / "project.json") as f:
                result = json.load(f)
            return Response(result, status=201)
        except FileNotFoundError:
            return Response({"error": "No se pudo crear el archivo project.json"}, status=500)


class ProjectView(APIView):
    @extend_schema(
        summary="Obtener datos del proyecto",
        responses={200: ProjectSerializer}
    )
    def get(self, request):
        data = request.data
        try:
            project_path = Path(data.get("base_path")).expanduser().resolve()
            project_json = project_path / "project.json"

            if not project_json.exists():
                return Response({"error": "project.json no encontrado"}, status=404)

            with open(project_json) as f:
                data = json.load(f)
                return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    @extend_schema(
        summary="Actualizar project.json",
        request=ProjectSerializer,
        responses={200: ProjectSerializer}
    )
    def put(self, request):
        data = request.data
        try:
            project_path = Path(data.get("base_path")).expanduser().resolve()
            project_json = project_path / "project.json"

            with open(project_json, "w") as f:
                json.dump(data, f, indent=2)
            return Response(data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


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
            return Response({"error": "project.json no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InitProjectView(APIView):
    @extend_schema(summary="Inicializar proyecto desde plantilla")
    def post(self, request):
        try:
            project_path = Path(request.data.get("base_path")).expanduser().resolve()

            (project_path / "outline").mkdir(parents=True, exist_ok=True)
            (project_path / "characters").mkdir(parents=True, exist_ok=True)
            (project_path / "world").mkdir(parents=True, exist_ok=True)
            (project_path / "notes").mkdir(parents=True, exist_ok=True)

            (project_path / "settings.json").write_text('{}')
            (project_path / "preferences.json").write_text('{}')
            (project_path / "summary.txt").write_text('Short summary.')
            (project_path / "tags.txt").write_text('')
            (project_path / "plots.txt").write_text('')

            return Response({"status": "initialized"}, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
