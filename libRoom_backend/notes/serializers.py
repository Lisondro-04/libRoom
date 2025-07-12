from rest_framework import serializers

class NoteSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    linked_to = serializers.CharField()
    content = serializers.CharField()

