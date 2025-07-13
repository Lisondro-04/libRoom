from rest_framework import serializers

class WorldIndexSerializer(serializers.Serializer):
    places = serializers.ListField(child=serializers.DictField(), default=[])
    objects = serializers.ListField(child=serializers.DictField(), default=[])
    cities = serializers.ListField(child=serializers.DictField(), default=[])
    custom = serializers.ListField(child=serializers.DictField(), default=[])

class NewEntrySerializer(serializers.Serializer):
    title = serializers.CharField()
    category = serializers.CharField()
