from django.urls import path
from .views import CreateProjectView, ProjectView

urlpatterns = [
    path('api/project/', ProjectView.as_view(), name='get_project'),
    path('api/project/create', CreateProjectView.as_view(), name='create_project'),
]