import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/export_options.dart';

class ExportService {
  final String baseUrl;

  ExportService(this.baseUrl);

  Future<void> exportProject(ExportOptions options) async {
    final url = Uri.parse('$baseUrl/api/export/');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(options.toJson()),
    );

    if (response.statusCode != 200) {
      throw Exception('Error en la exportación: ${response.body}');
    }
  }
}
