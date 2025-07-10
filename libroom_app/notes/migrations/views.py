from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import Note
from .serializers import NoteSerializer, NoteContentSerializer
from .utils import get_next_note_id, save_note_content, read_note_content, delete_note_file, count_words

class NoteListCreateView(APIView):
    @extend_schema(
        summary="List all notes or filter by linked_type",
        responses=NoteSerializer(many=True),
        tags=["Notes"]
    )
    def get(self, request):
        linked_type = request.query_params.get('linked_type')
        if linked_type:
            notes = Note.objects.filter(linked_type=linked_type)
        else:
            notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Create new note",
        request=NoteContentSerializer,
        responses=NoteSerializer,
        tags=["Notes"]
    )
    def post(self, request):
        content_serializer = NoteContentSerializer(data=request.data)
        content_serializer.is_valid(raise_exception=True)
        content = content_serializer.validated_data['content']

        new_id = get_next_note_id()
        wordcount = count_words(content)

        note = Note.objects.create(
            id=new_id,
            title=request.data.get('title', 'Untitled Note'),
            linked_type=request.data.get('linked_type', 'glob'),
            target_id=request.data.get('target_id'),
            word_count=wordcount
        )

        save_note_content(new_id, content)
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class NoteDetailView(APIView):
    @extend_schema(
        summary="Get note content",
        responses=NoteContentSerializer,
        tags=["Notes"]
    )
    def get(self, request, note_id):
        content = read_note_content(note_id)
        return Response({"content": content})

    @extend_schema(
        summary="Update note content",
        request=NoteContentSerializer,
        responses=NoteSerializer,
        tags=["Notes"]
    )
    def patch(self, request, note_id):
        note = Note.objects.get(pk=note_id)
        content_serializer = NoteContentSerializer(data=request.data)
        content_serializer.is_valid(raise_exception=True)
        content = content_serializer.validated_data['content']
        save_note_content(note_id, content)

        note.word_count = count_words(content)
        note.save()

        serializer = NoteSerializer(note)
        return Response(serializer.data)

    @extend_schema(
        summary="Delete note",
        tags=["Notes"]
    )
    def delete(self, request, note_id):
        note = Note.objects.get(pk=note_id)
        note.delete()
        delete_note_file(note_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

class NotesByTagView(APIView):
    @extend_schema(
        summary="Get notes by linked_type",
        responses=NoteSerializer(many=True),
        tags=["Notes"]
    )
    def get(self, request, tag):
        notes = Note.objects.filter(linked_type=tag)
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
