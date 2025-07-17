import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class WorldIndexPage extends StatefulWidget {
  const WorldIndexPage({super.key});

  @override
  State<WorldIndexPage> createState() => _WorldIndexPageState();
}

class _WorldIndexPageState extends State<WorldIndexPage> {
  Map<String, dynamic> worldIndex = {};

  @override
  void initState() {
    super.initState();
    _loadIndex();
  }

  Future<void> _loadIndex() async {
    final res = await http.get(Uri.parse('https://miapi.com/api/world/'));
    if (res.statusCode == 200) {
      if (!mounted) return; // <-- Protección
      setState(() {
        worldIndex = jsonDecode(res.body);
      });
    }
  }

  Future<void> _createIndex() async {
    final res = await http.post(Uri.parse('https://miapi.com/api/world/'));
    if (res.statusCode == 201 || res.statusCode == 200) {
      if (!mounted) return; // <-- Protección
      await _loadIndex();
    }
  }

  Future<void> _deleteEntry(String category, String id) async {
    final res = await http.delete(Uri.parse('https://miapi.com/api/world/$category/$id/'));
    if (res.statusCode == 204) {
      if (!mounted) return; // <-- Protección
      await _loadIndex();
    }
  }

  void _openEditor(String category, String id, String title) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => EditSectionPage(category: category, id: id, title: title),
      ),
    );
  }

  void _openNewEntry() {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => const AddEntryPage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[900],
      appBar: AppBar(
        backgroundColor: Colors.deepPurple,
        title: const Text('World Index'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: _openNewEntry,
          ),
          IconButton(
            icon: const Icon(Icons.sync),
            onPressed: _createIndex,
          ),
        ],
      ),
      body: worldIndex.isEmpty
          ? const Center(child: CircularProgressIndicator())
          : ListView(
              padding: const EdgeInsets.all(12),
              children: worldIndex.entries.expand((entry) {
                final category = entry.key;
                final items = entry.value as List;
                return [
                  Text(category.toUpperCase(), style: const TextStyle(color: Colors.white70)),
                  const SizedBox(height: 6),
                  ...items.map((e) => Card(
                        color: Colors.grey[800],
                        child: ListTile(
                          title: Text(e['title'], style: const TextStyle(color: Colors.white)),
                          subtitle: Text(e['id'], style: const TextStyle(color: Colors.white38)),
                          trailing: IconButton(
                            icon: const Icon(Icons.delete, color: Colors.redAccent),
                            onPressed: () => _deleteEntry(category, e['id']),
                          ),
                          onTap: () => _openEditor(category, e['id'], e['title']),
                        ),
                      ))
                ];
              }).toList(),
            ),
    );
  }
}

class AddEntryPage extends StatefulWidget {
  const AddEntryPage({super.key});

  @override
  State<AddEntryPage> createState() => _AddEntryPageState();
}

class _AddEntryPageState extends State<AddEntryPage> {
  final _titleController = TextEditingController();
  String _selectedCategory = 'places';
  final List<String> categories = ['places', 'objects', 'cities', 'other'];

  Future<void> _submit() async {
    final res = await http.post(
      Uri.parse('https://miapi.com/api/world/add/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'title': _titleController.text,
        'category': _selectedCategory,
      }),
    );
    if (res.statusCode == 201) {
      if (!mounted) return; // <-- Protección
      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[900],
      appBar: AppBar(
        backgroundColor: Colors.deepPurple,
        title: const Text('Nueva Entrada'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _titleController,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(labelText: 'Título', labelStyle: TextStyle(color: Colors.white70)),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              value: _selectedCategory,
              dropdownColor: Colors.grey[800],
              items: categories.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
              onChanged: (value) => setState(() => _selectedCategory = value!),
              decoration: const InputDecoration(labelText: 'Categoría', labelStyle: TextStyle(color: Colors.white70)),
            ),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: _submit,
              child: const Text('Crear'),
            )
          ],
        ),
      ),
    );
  }
}

class EditSectionPage extends StatefulWidget {
  final String category;
  final String id;
  final String title;

  const EditSectionPage({super.key, required this.category, required this.id, required this.title});

  @override
  State<EditSectionPage> createState() => _EditSectionPageState();
}

class _EditSectionPageState extends State<EditSectionPage> {
  final _sectionController = TextEditingController();
  final _sectionNameController = TextEditingController(text: 'Description');

  Future<void> _loadSection() async {
    final res = await http.get(Uri.parse('https://miapi.com/api/world/${widget.category}/${widget.id}/'));
    if (res.statusCode == 200) {
      if (!mounted) return; // <-- Protección
      _sectionController.text = res.body;
    }
  }

  Future<void> _saveSection() async {
    await http.patch(
      Uri.parse('https://miapi.com/api/world/${widget.category}/${widget.id}/section/'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'title': _sectionNameController.text,
        'category': widget.category,
        'content': _sectionController.text,
      }),
    );
  }

  @override
  void initState() {
    super.initState();
    _loadSection();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[900],
      appBar: AppBar(
        backgroundColor: Colors.deepPurple,
        title: Text(widget.title),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: _sectionNameController,
              style: const TextStyle(color: Colors.white70),
              decoration: const InputDecoration(labelText: 'Sección (#)', labelStyle: TextStyle(color: Colors.white70)),
            ),
            const SizedBox(height: 8),
            Expanded(
              child: Container(
                color: Colors.black,
                padding: const EdgeInsets.all(12),
                child: TextField(
                  controller: _sectionController,
                  maxLines: null,
                  expands: true,
                  style: const TextStyle(color: Colors.white),
                  decoration: const InputDecoration.collapsed(hintText: "Contenido de la sección", hintStyle: TextStyle(color: Colors.grey)),
                ),
              ),
            ),
            const SizedBox(height: 12),
            ElevatedButton(
              onPressed: _saveSection,
              child: const Text('Guardar Sección'),
            ),
          ],
        ),
      ),
    );
  }
}
