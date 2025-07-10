from rest_framework import serializers
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            'id',
            'title',
            'linked_type',
            'linked_target_id',
            'content',
            'word_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'word_count', 'created_at', 'updated_at']
