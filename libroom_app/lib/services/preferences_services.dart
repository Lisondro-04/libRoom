import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/preferences.dart';

class PreferencesService {
  final String baseUrl;
  final String authToken;

  PreferencesService({required this.baseUrl, required this.authToken});

  Future<Preferences> fetchPreferences() async {
    final response = await http.get(
      Uri.parse('$baseUrl/preferences/'),
      headers: {
        'Authorization': 'Bearer $authToken',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      final Map<String, dynamic> data = jsonDecode(response.body);
      return Preferences.fromJson(data);
    } else {
      throw Exception('Failed to load preferences');
    }
  }

  Future<void> updatePreferences(int id, Preferences prefs) async {
    final response = await http.put(
      Uri.parse('$baseUrl/preferences/$id/'),
      headers: {
        'Authorization': 'Bearer $authToken',
        'Content-Type': 'application/json',
      },
      body: jsonEncode(prefs.toJson()),
    );

    if (response.statusCode != 200 && response.statusCode != 204) {
      throw Exception('Failed to update preferences');
    }
  }
}
