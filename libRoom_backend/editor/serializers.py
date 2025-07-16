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
    setGoal = serializers.IntegerField()

class RenameSerializer(serializers.Serializer):
    old_id = serializers.CharField()
    new_title = serializers.CharField()
