import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/project_model.dart';

class ProjectService {
  final String baseUrl = 'http://127.0.0.1:8000/api';
  
  Future<bool> createProject(Project project) async {
    final response = await http.post(
      Uri.parse('$baseUrl/project/create'),
      headers: {'Content-Type': 'applications/json'},
      body: jsonEncode(project.toJson()),
    );
    return response.statusCode == 201;
  }

  Future<Map<String, dynamic>> getSettings() async {
    final response = await http.get(Uri.parse('$baseUrl/settings/'));
    if (response.statusCode == 200){
      return jsonDecode(response.body);
    }
    throw Exception("Failed to load settings");
  }

  Future<Map<String, dynamic>> getPreferences() async {
    final response = await http.get(Uri.parse('$baseUrl/preferences/'));
    if (response.statusCode == 200){
      return jsonDecode(response.body);
    }
    throw Exception("Failed to load preferences");
  }
}

