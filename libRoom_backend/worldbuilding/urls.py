from django.urls import path
from .views import WorldIndexView, WorldAddEntryView, WorldEntryDetailView, WorldEntrySectionEditView

urlpatterns = [
    path('world/', WorldIndexView.as_view(), name='world-index'),
    path('world/add/', WorldAddEntryView.as_view(), name='world-add'),
    path('world/<str:category>/<str:id>/', WorldEntryDetailView.as_view(), name='world-entry-detail'),
    path('world/<str:category>/<str:id>/section/', WorldEntrySectionEditView.as_view(), name='world-entry-section-edit'),
]
