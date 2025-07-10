from django.urls import path
from .views import SettingsView

urlpatterns = [
    path('api/settings/', SettingsView.as_view(), name='api-settings'),
]
