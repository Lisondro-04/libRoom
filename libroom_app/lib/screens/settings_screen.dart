import 'package:flutter/material.dart';
import '../services/settings_services.dart';
import '../models/settings.dart';

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
      appBar: AppBar(title: Text('Settings')),
      body: FutureBuilder<Setting>(
        future: _settingsFuture,
        builder: (context, snapshot) {
          if (snapshot.hasData) {
            final setting = snapshot.data!;
            return ListView(
              padding: EdgeInsets.all(16),
              children: [
                _buildDropdown('Interface Language', setting.interfaceLanguage, interfaceLanguages, (val) => setting.interfaceLanguage = val!),
                _buildDropdown('Interface Font', setting.interfaceFont, interfaceFonts, (val) => setting.interfaceFont = val!),
                _buildDropdown('Interface Font Size', setting.interfaceFontSize.toString(), interfaceFontSizes, (val) => setting.interfaceFontSize = int.parse(val!)),
                _buildDropdown('Project Save Location', setting.defaultProjectSaveLocation, projectSaveLocations, (val) => setting.defaultProjectSaveLocation = val!),
                _buildDropdown('Auto-save Frequency', setting.autoSaveFrequency, autoSaveFrequencies, (val) => setting.autoSaveFrequency = val!),
                _buildDropdown('Export Location', setting.defaultExportLocation, exportLocations, (val) => setting.defaultExportLocation = val!),
                ElevatedButton(
                  onPressed: () async {
                    await _service.updateSettings(setting);
                    ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Settings updated!')));
                  },
                  child: Text('Save Changes'),
                ),
              ],
            );
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }
          return Center(child: CircularProgressIndicator());
        },
      ),
    );
  }

  Widget _buildDropdown(String label, String value, List<String> items, ValueChanged<String?> onChanged) {
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
