from rest_framework import serializers

class ProjectCreationSerializer(serializers.Serializer):
    title = serializers.CharField()
    author = serializers.CharField()
    type = serializers.ChoiceField(choices=["novel", "short_story"])
    number_of_chapters = serializers.IntegerField()
    scenes_by_chapter = serializers.IntegerField()
    words_by_scene = serializers.IntegerField()
    directory_path = serializers.CharField(required=False)


class ProjectSerializer(serializers.Serializer):
    title = serializers.CharField()
    author = serializers.CharField()
    series = serializers.CharField()
    volume = serializers.CharField()
    genres = serializers.CharField()
    license = serializers.CharField()
    email = serializers.CharField()
    outline_path = serializers.CharField()
    characters_path = serializers.CharField()
    world_path = serializers.CharField()
    notes_path = serializers.CharField()
    settings_file = serializers.CharField()
    preferences_file = serializers.CharField()
    summary_file = serializers.CharField()
    tags_file = serializers.CharField()
    plots_file = serializers.CharField()
    total_words_goal = serializers.IntegerField()
    words_by_scene = serializers.IntegerField()
    words_by_chapter = serializers.IntegerField()
    number_of_chapters = serializers.IntegerField()
    scenes_by_chapter = serializers.CharField()
