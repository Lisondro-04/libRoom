from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter

# GET all notes / POST new note
@extend_schema(
    summary="Listar todas las notas o crear nueva nota",
    request=NoteSerializer,
    responses={200: NoteSerializer(many=True), 201: NoteSerializer},
    tags=["Notes"]
)
class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

# GET, PATCH, DELETE single note
@extend_schema(
    summary="Obtener, actualizar o eliminar una nota por ID",
    responses={200: NoteSerializer},
    tags=["Notes"]
)
class NoteRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    lookup_field = 'id'

# GET by tag
@extend_schema(
    summary="Obtener notas filtradas por tipo de asociación (tag)",
    parameters=[OpenApiParameter("tag", str, OpenApiParameter.PATH)],
    responses={200: NoteSerializer(many=True)},
    tags=["Notes"]
)
class NoteByTagView(generics.ListAPIView):
    serializer_class = NoteSerializer

    def get_queryset(self):
        tag = self.kwargs['tag']
        return Note.objects.filter(linked_type=tag)
