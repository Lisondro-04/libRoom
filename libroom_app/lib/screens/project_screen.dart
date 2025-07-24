import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import '../models/project_model.dart';
import '../services/project_services.dart';
import '../widgets/sidebar_widget.dart';
import '../globals.dart' as globals;

class CreateProjectScreen extends StatefulWidget {
  const CreateProjectScreen({super.key});

  @override
  _CreateProjectScreenState createState() => _CreateProjectScreenState();
}

class _CreateProjectScreenState extends State<CreateProjectScreen> {
  final _service = ProjectService();

  String selectedTemplate = '';
  String type = '';
  int chapters = 1;
  int scenes = 1;
  int wordsPerScene = 100;
  int totalWords = 100;

  String? basePath; // Ruta base seleccionada por usuario (sin nombre del proyecto aún)
  String projectName = ''; // Nombre del proyecto ingresado por el usuario

  final _titleController = TextEditingController();

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
              child: SingleChildScrollView(
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
                    const Text(
                      'Select Project Type',
                      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 10),
                    templateButton('Tale', 'short_story'),
                    templateButton('Novel', 'novel'),
                    const SizedBox(height: 30),
                    if (type != '') statisticsEditor(),
                    const SizedBox(height: 30),

                    // Input para nombre del proyecto (solo visible si tipo seleccionado)
                    if (type != '')
                      TextField(
                        controller: _titleController,
                        decoration: const InputDecoration(
                          labelText: 'Project Name',
                          border: OutlineInputBorder(),
                        ),
                        onChanged: (val) {
                          setState(() {
                            projectName = val.trim();
                          });
                        },
                      ),
                    if (type != '') const SizedBox(height: 20),

                    Row(
                      mainAxisAlignment: MainAxisAlignment.end,
                      children: [
                        ElevatedButton(
                          onPressed: openProject,
                          child: const Text('Open File'),
                        ),
                        const SizedBox(width: 20),
                        ElevatedButton(
                          onPressed: createProject,
                          child: const Text('Create'),
                        ),
                      ],
                    ),
                    if (basePath != null)
                      Padding(
                        padding: const EdgeInsets.only(top: 20),
                        child: Text('Selected base folder: $basePath'),
                      ),
                  ],
                ),
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
          projectName = '';
          _titleController.clear();
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

  Future<void> openProject() async {
    final result = await FilePicker.platform.getDirectoryPath();
    if (result != null) {
      basePath = result;
      globals.basePath = result;

      final settingsFile = File('$result/settings.json');
      final prefsFile = File('$result/preferences.json');

      if (await settingsFile.exists()) {
        final content = await settingsFile.readAsString();
        print("Settings: $content");
      }
      if (await prefsFile.exists()) {
        final content = await prefsFile.readAsString();
        print("Preferences: $content");
      }

      setState(() {});
    }
  }

  Future<void> createProject() async {
    if (projectName.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please enter a project name")),
      );
      return;
    }

    // Pido seleccionar la carpeta base donde crear el proyecto
    final selectedDir = await FilePicker.platform.getDirectoryPath();
    if (selectedDir == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please select a folder to create the project")),
      );
      return;
    }

    final newProjectPath = '$selectedDir/$projectName';
    final dir = Directory(newProjectPath);

    if (await dir.exists()) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("A project with that name already exists in this location")),
      );
      return;
    }

    final project = Project(
      title: projectName,
      author: "Anonymous",
      type: type,
      numberOfChapters: chapters,
      scenesByChapter: scenes,
      wordsByScene: wordsPerScene,
      basePath: newProjectPath,
    );

    final success = await _service.createProject(project);

    if (success) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Project created successfully")),
      );
      setState(() {
        basePath = newProjectPath;
        globals.basePath = newProjectPath;
      });
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Error creating project")),
      );
    }
  }
}
