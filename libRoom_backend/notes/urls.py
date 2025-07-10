from django.urls import path
from .views import NoteListCreateView, NoteRetrieveUpdateDeleteView, NoteByTagView

urlpatterns = [
    path('', NoteListCreateView.as_view(), name='note-list-create'),
    path('<str:id>/', NoteRetrieveUpdateDeleteView.as_view(), name='note-detail'),
    path('by-tag/<str:tag>/', NoteByTagView.as_view(), name='note-by-tag'),
]
