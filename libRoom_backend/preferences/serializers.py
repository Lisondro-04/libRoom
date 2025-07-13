from rest_framework import serializers

class PreferencesSerializer(serializers.Serializer):
    theme = serializers.ChoiceField(choices=["light-theme", "dark-theme", "system-default"])
    editor_font = serializers.CharField()
    font_size = serializers.IntegerField()
    skin = serializers.ChoiceField(choices=["among-us", "walter-white", "coffee-talk"])
    total_words_goal = serializers.IntegerField()
    session_goal = serializers.IntegerField()
    focus_button = serializers.ChoiceField(choices=["on", "off"])
    show_lateral_menu = serializers.ChoiceField(choices=["on", "off"])
    auto_spell_check = serializers.ChoiceField(choices=["on", "off"])
    global_tips = serializers.ChoiceField(choices=["on", "off"])
