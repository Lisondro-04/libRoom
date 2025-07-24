import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/project_model.dart';
import '../globals.dart' as globals;

class ProjectService {
  final String baseUrl = 'http://127.0.0.1:8000/api';
  
  Future<bool> createProject(Project project) async {
    final response = await http.post(
      Uri.parse('$baseUrl/project/create'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(project.toJson()),
    );
    return response.statusCode == 201;
  }

  Future<Map<String, dynamic>> getSettings() async {
    final uri = Uri.parse('$baseUrl/settings/').replace(queryParameters: {
      'basePath': globals.basePath ?? '',
    });

    final response = await http.get(uri);
    if (response.statusCode == 200){
      return jsonDecode(response.body);
    }
    throw Exception("Failed to load settings");
  }

  Future<Map<String, dynamic>> getPreferences() async {
    final uri = Uri.parse('$baseUrl/preferences/').replace(queryParameters:{
      'base_path': globals.basePath ?? '',
    });

    final response = await http.get(uri);
    if (response.statusCode == 200){
      return jsonDecode(response.body);
    }

    throw Exception("Failed to load preferences");
  }
}

