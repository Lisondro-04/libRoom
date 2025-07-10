from rest_framework import serializers

class SettingsSerializer(serializers.Serializer):
    language = serializers.ChoiceField(choices=['es', 'en-US'])
    ui_font = serializers.CharField(max_length=100)
    ui_font_size = serializers.IntegerField(min_value=8, max_value=72)
    default_project_path = serializers.CharField(max_length=500)
    autosave_frequency = serializers.ChoiceField(choices=['off', '1min', '5min', '10min', 'on_change'])
    default_export_path = serializers.CharField(max_length=500)
    cloud_sync_path = serializers.CharField(max_length=500)
    cloud_autosave_frequency = serializers.ChoiceField(choices=['off', '1min', '5min', '10min', 'on_change'])
