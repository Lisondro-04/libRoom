from django.urls import path
from .views import (
    SceneRetrieView,
    SceneUpdateView, 
    SceneGoalUpdateView, 
    RenameSceneView,
)

urlpatterns = [
    path('scenes/<str:scene_id>/', SceneRetrieView.as_view()),
    path('scenes/<str:scene_id>/goal/', SceneGoalUpdateView.as_view()),
    path('scenes/<str:scene_id>/', SceneUpdateView.as_view()),
    path('rename/scene/', RenameSceneView.as_view()),
]
