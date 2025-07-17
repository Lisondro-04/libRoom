import 'package:flutter/material.dart';
import '../services/settings_services.dart';
import '../models/settings.dart';
import '../widgets/sidebar_widget.dart';

class SettingsScreen extends StatefulWidget {
  @override
  _SettingsScreenState createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final _service = SettingsService();
  late Future<Setting> _settingsFuture;

  final interfaceLanguages = ['en-US', 'es-ES'];
  final interfaceFonts = ['Lora', 'Roboto', 'Open Sans'];
  final interfaceFontSizes = ['10', '12', '14', '16'];
  final projectSaveLocations = ['Projects folder', 'Desktop', 'Documents'];
  final autoSaveFrequencies = ['1 minute', '5 minutes', '10 minutes'];
  final exportLocations = ['Exports folder', 'Desktop', 'Documents'];

  @override
  void initState() {
    super.initState();
    _settingsFuture = _service.fetchSettings();
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
                  title: const Text('Settings'),
                  backgroundColor: Colors.deepPurple,
                ),
                Expanded(
                  child: FutureBuilder<Setting>(
                    future: _settingsFuture,
                    builder: (context, snapshot) {
                      if (snapshot.hasData) {
                        final setting = snapshot.data!;
                        return ListView(
                          padding: const EdgeInsets.all(16),
                          children: [
                            _buildDropdown(
                              label: 'Interface Language',
                              value: setting.interfaceLanguage,
                              items: interfaceLanguages,
                              onChanged: (val) {
                                setState(() {
                                  setting.interfaceLanguage = val!;
                                });
                              },
                            ),
                            _buildDropdown(
                              label: 'Interface Font',
                              value: setting.interfaceFont,
                              items: interfaceFonts,
                              onChanged: (val) {
                                setState(() {
                                  setting.interfaceFont = val!;
                                });
                              },
                            ),
                            _buildDropdown(
                              label: 'Interface Font Size',
                              value: setting.interfaceFontSize.toString(),
                              items: interfaceFontSizes,
                              onChanged: (val) {
                                setState(() {
                                  setting.interfaceFontSize = int.parse(val!);
                                });
                              },
                            ),
                            _buildDropdown(
                              label: 'Project Save Location',
                              value: setting.defaultProjectSaveLocation,
                              items: projectSaveLocations,
                              onChanged: (val) {
                                setState(() {
                                  setting.defaultProjectSaveLocation = val!;
                                });
                              },
                            ),
                            _buildDropdown(
                              label: 'Auto-save Frequency',
                              value: setting.autoSaveFrequency,
                              items: autoSaveFrequencies,
                              onChanged: (val) {
                                setState(() {
                                  setting.autoSaveFrequency = val!;
                                });
                              },
                            ),
                            _buildDropdown(
                              label: 'Export Location',
                              value: setting.defaultExportLocation,
                              items: exportLocations,
                              onChanged: (val) {
                                setState(() {
                                  setting.defaultExportLocation = val!;
                                });
                              },
                            ),
                            const SizedBox(height: 20),
                            ElevatedButton(
                              onPressed: () async {
                                await _service.updateSettings(setting);
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(content: Text('Settings updated!')),
                                );
                              },
                              child: const Text('Save Changes'),
                            ),
                          ],
                        );
                      } else if (snapshot.hasError) {
                        return Center(child: Text('Error: ${snapshot.error}'));
                      }
                      return const Center(child: CircularProgressIndicator());
                    },
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDropdown({
    required String label,
    required String value,
    required List<String> items,
    required ValueChanged<String?> onChanged,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        children: [
          Expanded(flex: 2, child: Text(label)),
          Expanded(
            flex: 3,
            child: DropdownButton<String>(
              value: value,
              isExpanded: true,
              onChanged: onChanged,
              items: items.map<DropdownMenuItem<String>>((String val) {
                return DropdownMenuItem<String>(
                  value: val,
                  child: Text(val),
                );
              }).toList(),
            ),
          ),
        ],
      ),
    );
  }
}