import 'package:flutter/material.dart';
import '../models/export_options.dart';
import '../services/export_services.dart';
import '../widgets/sidebar_widget.dart'; 
import '../globals.dart' as globals;

class ExportScreen extends StatefulWidget {
  const ExportScreen({super.key});

  @override
  State<ExportScreen> createState() => _ExportScreenState();
}

class _ExportScreenState extends State<ExportScreen> {
  ExportOptions _options = ExportOptions(exportTo: 'txt',);
  final _service = ExportService('http://127.0.0.1:8000'); 
  Future<void> _submitExport() async {
    try {
      final exportOptions = _options.copyWith(basePath: globals.basePath);
      await _service.exportProject(exportOptions);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Exportación exitosa')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error al exportar: $e')),
      );
    }
  }

  Widget _buildCheckbox(String label, bool value, Function(bool?) onChanged) {
    return Row(
      children: [
        Checkbox(value: value, onChanged: onChanged),
        Text(label),
      ],
    );
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
                  title: const Text('Export Project'),
                  backgroundColor: Colors.deepPurple,
                ),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: ListView(
                      children: [
                        const Text('Export to:'),
                        DropdownButton<String>(
                          value: _options.exportTo,
                          onChanged: (value) {
                            setState(() {
                              _options = _options.copyWith(exportTo: value);
                            });
                          },
                          items: ['pdf', 'txt', 'md', 'docx', 'odt', 'epub']
                              .map((e) => DropdownMenuItem(
                                  value: e, child: Text(e.toUpperCase())))
                              .toList(),
                        ),
                        const Divider(),
                        const Text('Select content to export:'),
                        _buildCheckbox(
                            'Level 1 Folder Title',
                            _options.level1FolderTitle,
                            (val) => setState(() => _options =
                                _options.copyWith(level1FolderTitle: val))),
                        _buildCheckbox(
                            'Level 2 Folder Title',
                            _options.level2FolderTitle,
                            (val) => setState(() => _options =
                                _options.copyWith(level2FolderTitle: val))),
                        _buildCheckbox(
                            'Level 1 Folder Text',
                            _options.level1FolderText,
                            (val) => setState(() => _options =
                                _options.copyWith(level1FolderText: val))),
                        _buildCheckbox(
                            'Level 2 Folder Text',
                            _options.level2FolderText,
                            (val) => setState(() => _options =
                                _options.copyWith(level2FolderText: val))),
                        _buildCheckbox(
                            'Level 1 Text',
                            _options.level1Text,
                            (val) => setState(() =>
                                _options.copyWith(level1Text: val))),
                        _buildCheckbox(
                            'Level 2 Text',
                            _options.level2Text,
                            (val) => setState(() =>
                                _options.copyWith(level2Text: val))),
                        const Divider(),
                        const Text('Filters:'),
                        TextField(
                          decoration:
                              const InputDecoration(labelText: 'Tag Filter'),
                          onChanged: (val) => setState(() =>
                              _options = _options.copyWith(tagFilter: val)),
                        ),
                        TextField(
                          decoration: const InputDecoration(
                              labelText: 'Status Filter'),
                          onChanged: (val) => setState(() =>
                              _options = _options.copyWith(statusFilter: val)),
                        ),
                        const SizedBox(height: 20),
                        ElevatedButton(
                          onPressed: _submitExport,
                          child: const Text('Export Project'),
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
    );
  }
}
