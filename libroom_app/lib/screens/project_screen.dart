import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import '../models/project_model.dart';
import '../services/project_services.dart';
import '../widgets/sidebar_widget.dart'; 

class CreateProjectScreen extends StatefulWidget {
  const CreateProjectScreen({super.key});

  @override
  _CreateProjectScreenState createState() => _CreateProjectScreenState();
}

class _CreateProjectScreenState extends State<CreateProjectScreen> {
  final _service = ProjectService();

  String selectedTemplate = 'Prose';
  String type = '';
  int chapters = 1;
  int scenes = 1;
  int wordsPerScene = 100;
  int totalWords = 100;
  String? lastDirectory;

  final _title = "My Project";
  final _author = "Anonymous";

  @override
  Widget build(BuildContext context) {
    totalWords = scenes * wordsPerScene * (type == 'novel' ? chapters : 1);

    return Scaffold(
      body: Row(
        children: [
          const Sidebar(), 

          Expanded(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 40.0, vertical: 50),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Center(
                    child: Text(
                      'Create a new project',
                      style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                    ),
                  ),
                  const SizedBox(height: 58),
                  Text('Pick a template', style: TextStyle(fontSize: 18)),
                  const SizedBox(height: 10),
                  templateButton('Prose', ''),
                  templateButton('Tale', 'short_story'),
                  templateButton('Novel', 'novel'),
                  const SizedBox(height: 30),
                  if (type != '') statisticsEditor(),
                  const SizedBox(height: 30),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      ElevatedButton(
                        onPressed: openFile,
                        child: const Text('Open File'),
                      ),
                      const SizedBox(width: 20),
                      ElevatedButton(
                        onPressed: createProject,
                        child: const Text('Create'),
                      ),
                    ],
                  )
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget templateButton(String name, String value) {
    final isSelected = selectedTemplate == name;
    return GestureDetector(
      onTap: () {
        setState(() {
          selectedTemplate = name;
          type = value;
        });
      },
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 5),
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        decoration: BoxDecoration(
          color: isSelected ? Colors.blue[100] : Colors.grey[200],
          borderRadius: BorderRadius.circular(10),
        ),
        child: Text(name),
      ),
    );
  }

  Widget statisticsEditor() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (type == 'novel')
          numberEditor("No. of chapters", chapters, (val) {
            setState(() => chapters = val);
          }),
        numberEditor("No. of scenes", scenes, (val) {
          setState(() => scenes = val);
        }),
        numberEditor("Words per scene", wordsPerScene, (val) {
          setState(() => wordsPerScene = val);
        }),
        const SizedBox(height: 10),
        Text("Total words: $totalWords", style: const TextStyle(fontSize: 16)),
      ],
    );
  }

  Widget numberEditor(String label, int value, Function(int) onChanged) {
    return Row(
      children: [
        Text("$label: "),
        SizedBox(
          width: 60,
          child: TextField(
            keyboardType: TextInputType.number,
            onChanged: (val) {
              final parsed = int.tryParse(val);
              if (parsed != null) onChanged(parsed);
            },
            controller: TextEditingController(text: value.toString()),
          ),
        ),
        IconButton(
          icon: const Icon(Icons.remove),
          onPressed: () => onChanged(value > 1 ? value - 1 : 1),
        ),
        IconButton(
          icon: const Icon(Icons.add),
          onPressed: () => onChanged(value + 1),
        ),
      ],
    );
  }

  Future<void> openFile() async {
    final result = await FilePicker.platform.getDirectoryPath();
    if (result != null) {
      lastDirectory = result;

      final settingsFile = File('$result/settings.json');
      final prefsFile = File('$result/preferences.json');

      if (await settingsFile.exists()) {
        final content = await settingsFile.readAsString();
        final data = content.isNotEmpty ? content : '{}';
        print("Settings: $data");
      }
      if (await prefsFile.exists()) {
        final content = await prefsFile.readAsString();
        final data = content.isNotEmpty ? content : '{}';
        print("Preferences: $data");
      }
    }
  }

  Future<void> createProject() async {
    final project = Project(
      title: _title,
      author: _author,
      type: type,
      numberOfChapters: chapters,
      scenesByChapter: scenes,
      wordsByScene: wordsPerScene,
    );

    final success = await _service.createProject(project);

    if (success) {
      final settings = await _service.getSettings();
      final preferences = await _service.getPreferences();

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Proyecto creado con éxito")),
      );

      print("Settings: $settings");
      print("Preferences: $preferences");
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Error al crear proyecto")),
      );
    }
  }
}
