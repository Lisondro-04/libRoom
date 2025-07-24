from django.urls import path
from .views import ExportProjectView

urlpatterns = [
    path('export/', ExportProjectView.as_view(), name='export'),
]
