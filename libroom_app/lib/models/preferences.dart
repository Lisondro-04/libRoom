class Preferences {
  final String theme;
  final int fontSize;
  final String font;
  final String skin;
  final int goal;
  final int goalPerSession;
  final bool focusButton;
  final bool showLateralMenu;
  final bool spellCheck;
  final bool globalTips;
  final String? basePath;

  Preferences({
    required this.theme,
    required this.fontSize,
    required this.font,
    required this.skin,
    required this.goal,
    required this.goalPerSession,
    required this.focusButton,
    required this.showLateralMenu,
    required this.spellCheck,
    required this.globalTips,
    this.basePath,
  });

  factory Preferences.fromJson(Map<String, dynamic> json) {
    return Preferences(
      theme: json['theme'],
      fontSize: json['font_size'],
      font: json['font'],
      skin: json['skin'],
      goal: json['goal'],
      goalPerSession: json['goal_per_session'],
      focusButton: json['focus_button'],
      showLateralMenu: json['show_lateral_menu'],
      spellCheck: json['spell_check'],
      globalTips: json['global_tips'],
      basePath:  json['base_path'],
    );
  }
  Preferences copyWith({
    String? theme,
    int? fontSize,
    String? font,
    String? skin,
    int? goal,
    int? goalPerSession,
    bool? focusButton,
    bool? showLateralMenu,
    bool? spellCheck,
    bool? globalTips,
    String? basePath,
  }) {
    return Preferences(
      theme: theme ?? this.theme,
      fontSize: fontSize ?? this.fontSize,
      font: font ?? this.font,
      skin: skin ?? this.skin,
      goal: goal ?? this.goal,
      goalPerSession: goalPerSession ?? this.goalPerSession,
      focusButton: focusButton ?? this.focusButton,
      showLateralMenu: showLateralMenu ?? this.showLateralMenu,
      spellCheck: spellCheck ?? this.spellCheck,
      globalTips: globalTips ?? this.globalTips,
      basePath: basePath ?? this.basePath,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'theme': theme,
      'font_size': fontSize,
      'font': font,
      'skin': skin,
      'goal': goal,
      'goal_per_session': goalPerSession,
      'focus_button': focusButton,
      'show_lateral_menu': showLateralMenu,
      'spell_check': spellCheck,
      'global_tips': globalTips,
      'base_path': basePath,
    };
  }
}
