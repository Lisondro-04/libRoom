from django.urls import path
from .views import NoteListCreateView, NoteDetailView, NotesByTagView

urlpatterns = [
    path('notes/', NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<str:note_id>/', NoteDetailView.as_view(), name='note-detail'),
    path('notes/by-tag/<str:tag>/', NotesByTagView.as_view(), name='notes-by-tag'),
]
