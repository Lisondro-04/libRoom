from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .serializers import (
    ChapterCreateSerializer, ChapterResponseSerializer,
    RenameSerializer, MoveSceneSerializer, GoalUpdateSerializer
)
from . import utils

@extend_schema(
    summary="Obtener estructura del proyecto",
    tags=["Outline"],
    responses={200: ChapterResponseSerializer(many=True)}
)
class OutlineTreeView(APIView):
    def get(self, request):
        base_path = request.query_params.get("base_path")
        if not base_path:
            return Response({"error": "Missing base_path"}, status=400)
        outline = []
        root = utils.get_outline_root(base_path)

        for chapter_dir in root.iterdir():
            if chapter_dir.is_dir():
                meta = chapter_dir / "chapter.md"
                if meta.exists():
                    data = meta.read_text(encoding="utf-8")
                    outline.append({
                        "id": chapter_dir.name,
                        "title": data.splitlines()[0].replace("title: ", ""),
                        "path": str(meta),
                        "wordCount": 0,  # Puedes implementar conteo real
                        "scenes_ids": []  # Lógica pendiente
                    })
        return Response(outline)


@extend_schema(
    summary="Crear capítulo",
    request=ChapterCreateSerializer,
    responses={201: ChapterResponseSerializer},
    tags=["Outline"]
)
class CreateChapterView(APIView):
    def post(self, request):
        base_path = request.query_params.get("base_path")
        if not base_path:
            return Response({"error": "Missing base_path"}, status=400)

        ser = ChapterCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        data = ser.validated_data
        root = utils.get_outline_root()
        cid = utils.generate_id("ch")

        chapter_dir = root / cid
        chapter_dir.mkdir(parents=True, exist_ok=True)

        meta = chapter_dir / "chapter.md"
        meta.write_text(
            f"title: {data['title']}\n"
            f"ID: {cid}\n"
            f"type: folder\n"
            f"label: {data['label']}\n"
            f"status: draft\n"
            f"compile: 0\n"
            f"setGoal: {data['setGoal']}\n"
            f"wordCount: 0\n"
            f"scenes_ids: []\n",
            encoding="utf-8"
        )

        return Response({
            "id": cid,
            "title": data["title"],
            "path": str(meta),
            "wordCount": 0,
            "scenes_ids": [],
        }, status=status.HTTP_201_CREATED)

