from django.urls import path
from .views import ExportProjectView

urlpatterns = [
    path('api/export/', ExportProjectView.as_view(), name='export'),
]
