from rest_framework import serializers

class SceneDetailSerializer(serializers.Serializer):
    ID = serializers.CharField()
    title = serializers.CharField()
    POV = serializers.CharField()
    label = serializers.IntegerField()
    status = serializers.CharField()
    compile =  serializers.IntegerField()
    setGoal = serializers.IntegerField()
    wordCount = serializers.IntegerField()
    content =  serializers.CharField()

class SceneUpdateSerializer(serializers.Serializer):
    base_path = serializers.CharField()
    title = serializers.CharField(required=False)
    POV = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    label = serializers.IntegerField(required=False)
    status = serializers.CharField(required=False)
    compile =  serializers.IntegerField(required=False)
    setGoal = serializers.IntegerField(required=False)
    wordCount = serializers.IntegerField(required=False)
    content =  serializers.CharField(required=False)

class GoalUpdateSerializer(serializers.Serializer):
    base_path = serializers.CharField()
    setGoal = serializers.IntegerField()

class RenameSerializer(serializers.Serializer):
    base_path = serializers.CharField()
    old_id = serializers.CharField()
    new_title = serializers.CharField()

class RenameResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    new_path = serializers.CharField()