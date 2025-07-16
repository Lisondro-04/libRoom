from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers  import SceneDetailSerializer, SceneUpdateSerializer, GoalUpdateSerializer, RenameSerializer
from .utils import read_scene_file, write_scene_file, get_scene_path_by_id
from libRoom_backend.settings import CURRENT_PROJECT_PATH
import os

@extend_schema(
    summary="Obtener una escena por ID",
    responses={200: SceneDetailSerializer},
    tags=["Editor"]
)

class SceneRetrieView(APIView):
    def get(self, request, scene_id):
        path = get_scene_path_by_id(scene_id, CURRENT_PROJECT_PATH)
        if not path:
            return Response({"error": "Scene was not found"}, status=404)
        data = read_scene_file(path)
        return Response(data)
    
@extend_schema(
    summary="Actualizar contenido y metadatos de una escena.",
    request=SceneUpdateSerializer,
    responses={200: SceneDetailSerializer},
    tags=["Editor"]
)

class SceneUpdateView(APIView):
    def patch(self, request, scene_id):
        path = get_scene_path_by_id(scene_id, CURRENT_PROJECT_PATH)
        if not path:
            return Response({"error": "Scene not found"}, status=404)
        data = read_scene_file(path)
        updated = request.data
        data.update(updated)
        data['wordCount'] = len(data['content'])
        write_scene_file(path, data)
        return Response(data)
    
@extend_schema(
    summary="Actualizar objetivo de palabras",
    request=GoalUpdateSerializer, 
    responses={200: SceneDetailSerializer},
    tags=["Editor"]
)

class SceneGoalUpdateView(APIView):
    def patch(self, request, scene_id):
        path = get_scene_path_by_id(scene_id, CURRENT_PROJECT_PATH)
        if not path:
            return Response({"eror": "Scene not found"}, status=404)
        data = read_scene_file(path)
        data('setGoal') = request.data['setGoal']
        write_scene_file(path, data)
        return Response(data)
    
@extend_schema(
    summary="Renombrar escena",
    request=RenameSerializer,
    tags=["Editor"]
)

class RenameSceneView(APIView):
    def pathc(self, request):
        old_id = request.data['old_id']
        new_title = request.data['new_title']
        old_path =  get_scene_path_by_id(old_id, CURRENT_PROJECT_PATH)
        if not old_path:
            return Response({"error": "Scene not found"}, status=404)
        new_filename = f"{new_title.lowe().replace(' ', '_')}.md"
        new_path = old_path.parent /new_filename

        os.rename(old_path, new_path)
        data = read_scene_file(new_path)
        data['title'] = new_title
        write_scene_file(new_path, data)
        return Response({"message": "Scene renamed succesfully", "new_path": str(new_path)})
