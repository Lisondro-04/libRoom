class ExportOptions {
  final String exportTo;
  final bool level1FolderTitle;
  final bool level1FolderText;
  final bool level2FolderTitle;
  final bool level2FolderText;
  final bool level1Text;
  final bool level2Text;
  final String tagFilter;
  final String statusFilter;

  ExportOptions({
    required this.exportTo,
    this.level1FolderTitle = false,
    this.level1FolderText = false,
    this.level2FolderTitle = false,
    this.level2FolderText = false,
    this.level1Text = false,
    this.level2Text = false,
    this.tagFilter = '',
    this.statusFilter = '',
  });

  ExportOptions copyWith({
    String? exportTo,
    bool? level1FolderTitle,
    bool? level1FolderText,
    bool? level2FolderTitle,
    bool? level2FolderText,
    bool? level1Text,
    bool? level2Text,
    String? tagFilter,
    String? statusFilter,
  }) {
    return ExportOptions(
      exportTo: exportTo ?? this.exportTo,
      level1FolderTitle: level1FolderTitle ?? this.level1FolderTitle,
      level1FolderText: level1FolderText ?? this.level1FolderText,
      level2FolderTitle: level2FolderTitle ?? this.level2FolderTitle,
      level2FolderText: level2FolderText ?? this.level2FolderText,
      level1Text: level1Text ?? this.level1Text,
      level2Text: level2Text ?? this.level2Text,
      tagFilter: tagFilter ?? this.tagFilter,
      statusFilter: statusFilter ?? this.statusFilter,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'export_to': exportTo,
      'level1_folder_title': level1FolderTitle,
      'level1_folder_text': level1FolderText,
      'level2_folder_title': level2FolderTitle,
      'level2_folder_text': level2FolderText,
      'level1_text': level1Text,
      'level2_text': level2Text,
      'tag_filter': tagFilter,
      'status_filter': statusFilter,
    };
  }
}
