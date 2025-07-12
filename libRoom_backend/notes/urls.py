from django.urls import path
from . import views


urlpatterns = [
    path('notes/', views.NotesListView.as_view()),       # GET para listar, POST para crear
    path('notes/<str:note_id>/', views.NoteDetailView.as_view()),  # GET, DELETE nota individual
]
