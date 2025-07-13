from rest_framework import serializers

class ChapterCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    label = serializers.IntegerField()
    setGoal = serializers.IntegerField()

class ChapterResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    title = serializers.CharField()
    path = serializers.CharField()
    wordCount = serializers.IntegerField()
    scenes_ids = serializers.ListField(child=serializers.CharField())

class RenameSerializer(serializers.Serializer):
    old_path = serializers.CharField()
    new_name = serializers.CharField()

class MoveSceneSerializer(serializers.Serializer):
    scene_id = serializers.CharField()
    from_chapter = serializers.CharField()
    to_chapter = serializers.CharField()

class GoalUpdateSerializer(serializers.Serializer):
    goal = serializers.IntegerField()
