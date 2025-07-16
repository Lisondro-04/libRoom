// services/settings_service.dart

import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/settings.dart';

class SettingsService {
  final String baseUrl = 'http://127.0.0.1:8000/api/settings/';

  Future<Setting> fetchSettings() async {
    final response = await http.get(Uri.parse(baseUrl));

    if (response.statusCode == 200) {
      return Setting.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load settings');
    }
  }

  Future<void> updateSettings(Setting setting) async {
    final response = await http.put(
      Uri.parse(baseUrl),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(setting.toJson()),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to update settings');
    }
  }
}
