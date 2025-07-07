from rest_framework import serializers

class ProjectCreationSerializer(serializers.Serializer):
    title = serializers.CharField()
    author = serializers.CharField()
    type = serializers.ChoiceField(choices=["novel", "short_story"])
    number_of_chapters = serializers.IntegerField()
    scenes_by_chapter = serializers.IntegerField()
    words_by_scene = serializers.IntegerField()


class ProjectSerializer(serializers.Serializer):
    title = serializers.CharField()
    author = serializers.CharField()
    outline_path = serializers.CharField()
    characters_path = serializers.CharField()
    world_path = serializers.CharField()
    notes_path = serializers.CharField()
    settings_file = serializers.CharField()
    preferences_file = serializers.CharField()
    summary_file = serializers.CharField()
    tags_file = serializers.CharField()
    plots_file = serializers.CharField()
    total_words_goal = serializers.CharField()
    words_by_scene = serializers.CharField()
    words_by_chapter = serializers.CharField()
    number_of_chapters = serializers.CharField()
    scenes_by_chapter = serializers.CharField()
