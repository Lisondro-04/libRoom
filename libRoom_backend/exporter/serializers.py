from rest_framework import serializers

class ExportTextTransformationsSerializer(serializers.Serializer):
    double_quotes = serializers.ListField(
        child=serializers.CharField(), required=False,
        help_text='Ej: ["\"", "«»"]'
    )
    single_quotes = serializers.ListField(
        child=serializers.CharField(), required=False,
        help_text="Ej: [\"'\", \"‹›\"]"
    )
    long_dash = serializers.CharField(required=False, help_text='Ej: "---" se convierte en "—"')
    custom_replacements = serializers.DictField(
        child=serializers.CharField(), required=False,
        help_text='Reemplazos personalizados, ej: {"[...]": "…"}'
    )
    remove_multiple_spaces = serializers.BooleanField(required=False)

class BlockSeparatorsSerializer(serializers.Serializer):
    between_chapters = serializers.CharField(default="\n\n")
    between_chapter_and_scene = serializers.CharField(default="---")
    between_scenes = serializers.CharField(default="\n\n")

class ExportConfigSerializer(serializers.Serializer):
    format = serializers.ChoiceField(
        choices=["pdf", "txt", "md", "docx", "odt"]
    )
    include_chapters = serializers.BooleanField(default=True)
    include_scenes = serializers.BooleanField(default=True)
    status_filter = serializers.ListField(
        child=serializers.IntegerField(), required=False,
        help_text="Filtra por estados de capítulo/escena. Ej: [2, 3]"
    )
    text_transformations = ExportTextTransformationsSerializer(required=False)
    block_separators = BlockSeparatorsSerializer(required=False)
    include_toc = serializers.BooleanField(default=False)

class ExportResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    output_path = serializers.CharField()
