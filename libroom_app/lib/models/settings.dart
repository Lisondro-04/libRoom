class Setting {
  String interfaceLanguage;
  String interfaceFont;
  int interfaceFontSize;
  String defaultProjectSaveLocation;
  String autoSaveFrequency;
  String defaultExportLocation;
  String? basePath;

  Setting({
    required this.interfaceLanguage,
    required this.interfaceFont,
    required this.interfaceFontSize,
    required this.defaultProjectSaveLocation,
    required this.autoSaveFrequency,
    required this.defaultExportLocation,
    this.basePath,
  });

  factory Setting.fromJson(Map<String, dynamic> json) {
    return Setting(
      interfaceLanguage: json['interface_language'],
      interfaceFont: json['interface_font'],
      interfaceFontSize: json['interface_font_size'],
      defaultProjectSaveLocation: json['default_project_save_location'],
      autoSaveFrequency: json['auto_save_frequency'],
      defaultExportLocation: json['default_export_location'],
      basePath: json['base_path'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'interface_language': interfaceLanguage,
      'interface_font': interfaceFont,
      'interface_font_size': interfaceFontSize,
      'default_project_save_location': defaultProjectSaveLocation,
      'auto_save_frequency': autoSaveFrequency,
      'default_export_location': defaultExportLocation,
      'base_path': basePath,
    };
  }
}
