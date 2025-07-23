from rest_framework import serializers


class CharacterMetaSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=["main", "secondary"])
    path = serializers.CharField(read_only=True)


class CharacterCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=["main", "secondary"])
    base_path = serializers.CharField()


class SectionPatchSerializer(serializers.Serializer):
    section = serializers.CharField(help_text="Markdown section title to overwrite")
    content = serializers.CharField(help_text="New markdown body for that section")
    base_path = serializers.CharField