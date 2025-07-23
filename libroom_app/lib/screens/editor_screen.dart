import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../widgets/sidebar_widget.dart'; 

class EditorScreen extends StatefulWidget {
  const EditorScreen({super.key});

  @override
  State<EditorScreen> createState() => _EditorScreenState();
}

class _EditorScreenState extends State<EditorScreen> {
  final _titleController = TextEditingController();
  final _linkedToController = TextEditingController();
  final _contentController = TextEditingController();
  bool _isLoading = false;

  Future<void> _submitNote() async {
    setState(() => _isLoading = true);

    final res = await http.post(
      Uri.parse('http://127.0.0.1:8000/api/notes/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'title': _titleController.text,
        'linked_to': _linkedToController.text,
        'content': _contentController.text,
      }),
    );

    setState(() => _isLoading = false);

    if (!mounted) return;

    if (res.statusCode == 201) {
      Navigator.pop(context);
    } else {
      showDialog(
        context: context,
        builder: (_) => AlertDialog(
          title: const Text("Error"),
          content: Text("No se pudo guardar la nota.\nCódigo: ${res.statusCode}"),
          actions: [TextButton(onPressed: () => Navigator.pop(context), child: const Text("OK"))],
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          const Sidebar(), 

          Expanded(
            child: Column(
              children: [
                AppBar(
                  backgroundColor: Colors.deepPurple,
                  title: const Text('Escribir Nota'),
                ),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: [
                        TextField(
                          controller: _titleController,
                          style: const TextStyle(color: Colors.white),
                          decoration: const InputDecoration(
                            labelText: 'Título',
                            labelStyle: TextStyle(color: Colors.white70),
                          ),
                        ),
                        const SizedBox(height: 12),
                        TextField(
                          controller: _linkedToController,
                          style: const TextStyle(color: Colors.white),
                          decoration: const InputDecoration(
                            labelText: 'Vinculado a',
                            labelStyle: TextStyle(color: Colors.white70),
                          ),
                        ),
                        const SizedBox(height: 12),
                        Expanded(
                          child: Container(
                            color: Colors.black,
                            padding: const EdgeInsets.all(12),
                            child: TextField(
                              controller: _contentController,
                              maxLines: null,
                              expands: true,
                              style: const TextStyle(color: Colors.white),
                              decoration: const InputDecoration.collapsed(
                                hintText: "Contenido de la nota",
                                hintStyle: TextStyle(color: Colors.grey),
                              ),
                            ),
                          ),
                        ),
                        const SizedBox(height: 12),
                        ElevatedButton(
                          onPressed: _isLoading ? null : _submitNote,
                          child: _isLoading
                              ? const CircularProgressIndicator(color: Colors.white)
                              : const Text('Guardar Nota'),
                        ),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
      backgroundColor: Colors.grey[900],
    );
  }
}
