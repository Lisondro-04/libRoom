from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from pathlib import Path
from datetime import datetime
from .serializers import NoteSerializer
from . import utils

class NotesListView(APIView):
    @extend_schema(
        summary="Listar todas las notas o filtradas por tipo",
        responses={200: NoteSerializer(many=True)},
        tags=["Notes"]
    )
    def get(self, request):
        base_path = request.query_params.get("base_path")
        if not base_path:
            return Response({"error": "base_path es requerido"}, status=400)

        tag = request.query_params.get("type", None)
        index = utils.load_index(base_path)["notes"]
        if tag:
            index = [n for n in index if n["linked_to"]["type"] == tag]
        return Response(index)

    @extend_schema(
        summary="Crear nueva nota",
        request=NoteSerializer,
        responses={201: NoteSerializer},
        tags=["Notes"]
    )
    def post(self, request):
        base_path = request.data.get("base_path")
        if not base_path:
            return Response({"error": "base_path es requerido"}, status=400)

        data = request.data
        note_id = utils.get_next_id(base_path)
        now = datetime.utcnow().isoformat()

        tag = data.get('linked_to', '')
        tag_type, target_id = tag.split("|") if "|" in tag else (tag, None)

        wc = utils.save_note_md(base_path, note_id, data['title'], tag, data['content'])

        new_note = {
            "id": note_id,
            "title": data["title"],
            "linked_to": {
                "type": tag_type,
                "target_id": target_id
            },
            "word_count": wc,
            "created_at": now,
            "updated_at": now
        }

        index = utils.load_index(base_path)
        index["notes"].append(new_note)
        utils.save_index(base_path, index)
        return Response(new_note, status=status.HTTP_201_CREATED)

class NoteDetailView(APIView):
    @extend_schema(
        summary="Obtener el contenido completo de una nota",
        responses={200: NoteSerializer, 404: None},
        tags=["Notes"]
    )
    def get(self, request, note_id):
        base_path = request.query_params.get("base_path")
        if not base_path:
            return Response({"error": "base_path es requerido"}, status=400)

        content = utils.load_note_md(base_path, note_id)
        if content is None:
            return Response({"error": "Nota no encontrada"}, status=404)
        # Busca metadatos en el índice
        index = utils.load_index(base_path)
        note_meta = next((n for n in index["notes"] if n["id"] == note_id), None)
        if not note_meta:
            return Response({"error": "Nota no encontrada"}, status=404)
        # Retorna datos completos
        response_data = {
            "id": note_meta["id"],
            "title": note_meta["title"],
            "linked_to": note_meta["linked_to"],
            "word_count": note_meta["word_count"],
            "created_at": note_meta["created_at"],
            "updated_at": note_meta["updated_at"],
            "content": content
        }
        return Response(response_data)

    @extend_schema(
        summary="Eliminar una nota",
        responses={204: None, 404: None},
        tags=["Notes"]
    )
    def delete(self, request, note_id):
        base_path = request.query_params.get("base_path")
        if not base_path:
            return Response({"error": "base_path es requerido"}, status=400)

        index = utils.load_index(base_path)
        note = next((n for n in index["notes"] if n["id"] == note_id), None)
        if not note:
            return Response({"error": "Nota no encontrada"}, status=404)
        # Quitar del índice
        index["notes"] = [n for n in index["notes"] if n["id"] != note_id]
        utils.save_index(base_path, index)
        # Borrar archivo .md
        file_path = Path(base_path) / f"{note_id}.md"
        if file_path.exists():
            file_path.unlink()
        return Response(status=204)
