import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class NotesPage extends StatefulWidget {
  const NotesPage({super.key});

  @override
  State<NotesPage> createState() => _NotesPageState();
}

class _NotesPageState extends State<NotesPage> {
  List<dynamic> notes = [];
  bool loading = true;
  String? selectedNoteId;
  String noteContent = '';

  @override
  void initState() {
    super.initState();
    fetchNotes();
  }

  Future<void> fetchNotes() async {
    final response = await http.get(Uri.parse('http://127.0.0.1:8000/api/notes/'));
    if (response.statusCode == 200) {
      setState(() {
        notes = json.decode(response.body);
        loading = false;
      });
    }
  }

  Future<void> fetchNoteContent(String id) async {
    final response = await http.get(Uri.parse('http://localhost:8000/api/notes/$id/'));
    if (response.statusCode == 200) {
      setState(() {
        selectedNoteId = id;
        noteContent = json.decode(response.body)['content'];
      });
    }
  }

  Future<void> deleteNote(String id) async {
    await http.delete(Uri.parse('http://localhost:8000/api/notes/$id/'));
    fetchNotes();
    setState(() {
      selectedNoteId = null;
      noteContent = '';
    });
  }

  Future<void> createNote() async {
    final response = await http.post(
      Uri.parse('http://localhost:8000/api/notes/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'title': 'Nueva nota',
        'linked_to': null,
        'content': ''
      }),
    );
    if (response.statusCode == 201) {
      fetchNotes();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notas'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: createNote,
          )
        ],
      ),
      body: loading
          ? const Center(child: CircularProgressIndicator())
          : Row(
              children: [
                Container(
                  width: 300,
                  decoration: BoxDecoration(
                    border: Border(right: BorderSide(color: Colors.grey.shade300)),
                  ),
                  child: ListView.builder(
                    itemCount: notes.length,
                    itemBuilder: (context, index) {
                      final note = notes[index];
                      return ListTile(
                        title: Text(note['title'] ?? 'Sin título'),
                        subtitle: note['linked_to'] != null ? Text('Vinculado a: ${note['linked_to']}') : null,
                        onTap: () => fetchNoteContent(note['id']),
                        trailing: IconButton(
                          icon: const Icon(Icons.delete, color: Colors.red),
                          onPressed: () => deleteNote(note['id']),
                        ),
                      );
                    },
                  ),
                ),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: selectedNoteId == null
                        ? const Center(child: Text('Selecciona una nota'))
                        : SingleChildScrollView(child: Text(noteContent)),
                  ),
                ),
              ],
            ),
    );
  }
}
