// screens/settings_screen.dart

import 'package:flutter/material.dart';
import '../services/settings_services.dart';
import '../models/settings.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  _SettingsScreenState createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final _service = SettingsService();
  late Future<Setting> _settingsFuture;

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
                _buildDropdown(
                  label: 'Interface Language',
                  value: setting.interfaceLanguage,
                  items: ['en-US', 'es-ES'],
                  onChanged: (val) {
                    setState(() {
                      setting.interfaceLanguage = val!;
                    });
                  },
                ),
                _buildDropdown(
                  label: 'Interface Font',
                  value: setting.interfaceFont,
                  items: ['Lora', 'Roboto'],
                  onChanged: (val) {
                    setState(() {
                      setting.interfaceFont = val!;
                    });
                  },
                ),
                // ... otros campos similares
                ElevatedButton(
                  onPressed: () async {
                    await _service.updateSettings(setting);
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Settings updated!')),
                    );
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
              items: items.map<DropdownMenuItem<String>>(
                (String val) {
                  return DropdownMenuItem<String>(
                    value: val,
                    child: Text(val),
                  );
                },
              ).toList(),
            ),
          ),
        ],
      ),
    );
  }
}
