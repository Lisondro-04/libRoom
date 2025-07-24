import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../widgets/sidebar_widget.dart';
import '../globals.dart' as globals;

class EditorScreen extends StatefulWidget {
  const EditorScreen({super.key});

  @override
  State<EditorScreen> createState() => _EditorScreenState();
}

class _EditorScreenState extends State<EditorScreen> {
  final _titleController = TextEditingController();
  final _contentController = TextEditingController();
  final _goalController = TextEditingController();
  final _povController = TextEditingController();

  String _status = '';
  int _wordCount = 0;
  int _setGoal = 0;
  bool _isLoading = false;

  List<String> _statuses = [];
  List<String> _characters = [];
  List<String> _chapters = [];
  List<String> _scenes = [];
  String? _selectedChapter;
  String? _selectedScene;

  String? _sceneId;

  @override
  void initState() {
    super.initState();
    _loadMetadataOptions();
  }

  Future<void> _loadMetadataOptions() async {
    // Simular carga de capítulos/escenas
    setState(() {
      _chapters = ['Cap 1', 'Cap 2'];
      _scenes = ['scene_001', 'scene_002'];
    });
  }

  Future<void> _loadScene(String sceneId) async {
    setState(() {
      _isLoading = true;
    });

    final res = await http.get(Uri.parse('http://127.0.0.1:8000/api/scenes/$sceneId/'));

    if (res.statusCode == 200) {
      final data = json.decode(res.body);
      setState(() {
        _sceneId = sceneId;
        _titleController.text = data['title'];
        _contentController.text = data['content'];
        _povController.text = data['POV'] ?? '';
        _status = data['status'] ?? '';
        _setGoal = data['setGoal'] ?? 0;
        _wordCount = _countWords(data['content']);
        _goalController.text = _setGoal.toString();
        _isLoading = false;
      });
    } else {
      setState(() {
        _isLoading = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Error al cargar escena')),
      );
    }
  }

  int _countWords(String text) {
    return text.trim().isEmpty ? 0 : text.trim().split(RegExp(r'\\s+')).length;
  }

  Future<void> _saveScene() async {
    if (_sceneId == null) return;

    final res = await http.patch(
      Uri.parse('http://127.0.0.1:8000/api/scenes/$_sceneId/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'base_path': globals.basePath,
        'title': _titleController.text,
        'content': _contentController.text,
        'POV': _povController.text,
        'status': _status,
        'setGoal': _setGoal,
        'wordCount': _countWords(_contentController.text),
      }),
    );

    if (res.statusCode == 200) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Escena guardada')),
      );
    }
  }

  Widget _buildChapterSceneSelector() {
    return Column(
      children: [
        DropdownButtonFormField<String>(
          decoration: const InputDecoration(labelText: 'Capítulo'),
          value: _selectedChapter,
          items: _chapters.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
          onChanged: (val) => setState(() => _selectedChapter = val),
        ),
        if (_selectedChapter != null)
          DropdownButtonFormField<String>(
            decoration: const InputDecoration(labelText: 'Escena'),
            value: _selectedScene,
            items: _scenes.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
            onChanged: (val) {
              setState(() {
                _selectedScene = val;
              });
              if (val != null) {
                _loadScene(val);
              }
            },
          ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[900],
      body: Row(
        children: [
          const Sidebar(),
          Expanded(
            flex: 7,
            child: Column(
              children: [
                Container(
                  padding: const EdgeInsets.all(12),
                  color: Colors.deepPurple,
                  width: double.infinity,
                  child: Text(
                    _titleController.text.isEmpty ? 'Editor' : _titleController.text,
                    style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                ),
                Expanded(
                  child: Row(
                    children: [
                      Expanded(
                        flex: 2,
                        child: SingleChildScrollView(
                          padding: const EdgeInsets.all(12),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              _buildChapterSceneSelector(),
                              const SizedBox(height: 16),
                              if (_sceneId != null) _buildMetadataEditor(),
                            ],
                          ),
                        ),
                      ),
                      Expanded(
                        flex: 5,
                        child: Padding(
                          padding: const EdgeInsets.all(16),
                          child: _isLoading || _sceneId == null
                              ? const Center(child: Text('Selecciona una escena para editar', style: TextStyle(color: Colors.white60)))
                              : Column(
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
                                    Expanded(
                                      child: Container(
                                        color: Colors.black,
                                        padding: const EdgeInsets.all(12),
                                        child: TextField(
                                          controller: _contentController,
                                          maxLines: null,
                                          expands: true,
                                          onChanged: (val) => setState(() => _wordCount = _countWords(val)),
                                          style: const TextStyle(color: Colors.white),
                                          decoration: const InputDecoration.collapsed(
                                            hintText: "Contenido de la escena...",
                                            hintStyle: TextStyle(color: Colors.grey),
                                          ),
                                        ),
                                      ),
                                    ),
                                    const SizedBox(height: 12),
                                    ElevatedButton(
                                      onPressed: _saveScene,
                                      child: const Text("Guardar Escena"),
                                    ),
                                  ],
                                ),
                        ),
                      ),
                      Expanded(
                        flex: 3,
                        child: Container(
                          color: Colors.grey[850],
                          child: const Center(
                            child: Text("Notas", style: TextStyle(color: Colors.white60)),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMetadataEditor() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        DropdownButtonFormField<String>(
          value: _status,
          decoration: const InputDecoration(labelText: 'Estatus'),
          items: _statuses.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
          onChanged: (val) => setState(() => _status = val ?? ''),
        ),
        DropdownButtonFormField<String>(
          value: _povController.text,
          decoration: const InputDecoration(labelText: 'POV'),
          items: _characters.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
          onChanged: (val) => setState(() => _povController.text = val ?? ''),
        ),
        TextFormField(
          controller: _goalController,
          keyboardType: TextInputType.number,
          decoration: const InputDecoration(labelText: 'Objetivo en palabras'),
          onChanged: (val) => _setGoal = int.tryParse(val) ?? 0,
        ),
      ],
    );
  }
}
