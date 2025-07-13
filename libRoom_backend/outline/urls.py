from django.urls import path
from .views import (
    OutlineTreeView,
    CreateChapterView,
)

urlpatterns = [
    path("", OutlineTreeView.as_view(), name="outline-tree"),
    path("chapters/", CreateChapterView.as_view(), name="create-chapter"),
    # Añadir luego: rename, move, delete, update_goal, etc.
]
