from rest_framework import serializers

class SettingsSerializer(serializers.Serializer):
    language = serializers.ChoiceField(choices=["es", "en-US"])
    ui_font = serializers.CharField()
    ui_font_size = serializers.IntegerField()
    default_project_path = serializers.CharField()
    autosave_frequency = serializers.ChoiceField(choices=["off", "1min", "5min", "10min", "on_change"])
    default_export_path = serializers.CharField()
    cloud_sync_path = serializers.CharField()
    cloud_autosave_frequency = serializers.ChoiceField(choices=["off", "1min", "5min", "10min", "on_change"])
