from django.urls import path
from .views import CreateProjectView, ProjectView

urlpatterns = [
    path('project/', ProjectView.as_view(), name='get_project'),
    path('project/create', CreateProjectView.as_view(), name='create_project'),
]