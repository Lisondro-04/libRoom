from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'linked_type', 'linked_target_id', 'word_count', 'created_at', 'updated_at']
    search_fields = ['title', 'linked_target_id']
    list_filter = ['linked_type']
