import 'package:flutter/material.dart';
import '../models/preferences.dart';
import '../services/preferences_services.dart';

class PreferencesScreen extends StatefulWidget {
  final PreferencesService service;

  const PreferencesScreen({super.key, required this.service});

  @override
  State<PreferencesScreen> createState() => _PreferencesScreenState();
}

class _PreferencesScreenState extends State<PreferencesScreen> {
  Preferences? _prefs;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _loadPrefs();
  }

  Future<void> _loadPrefs() async {
    try {
      final prefs = await widget.service.fetchPreferences();
      setState(() {
        _prefs = prefs;
        _loading = false;
      });
    } catch (e) {
      print("Error loading preferences: $e");
    }
  }

  void _save() async {
    if (_prefs != null) {
      await widget.service.updatePreferences(1, _prefs!); // Ajusta el ID según tu backend
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Preferences updated')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Preferences')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _buildDropdown('Theme', _prefs!.theme, ['default', 'dark', 'light'], (val) {
            setState(() => _prefs = _prefs!.copyWith(theme: val));
          }),
          _buildDropdown('Font', _prefs!.font, ['Times New Roman', 'Arial', 'Courier'], (val) {
            setState(() => _prefs = _prefs!.copyWith(font: val));
          }),
          _buildDropdown('Skin', _prefs!.skin, ['coffee-talk', 'minimal', 'retro'], (val) {
            setState(() => _prefs = _prefs!.copyWith(skin: val));
          }),
          _buildNumberInput('Font Size', _prefs!.fontSize, (val) {
            setState(() => _prefs = _prefs!.copyWith(fontSize: val));
          }),
          _buildNumberInput('Overall Goal', _prefs!.goal, (val) {
            setState(() => _prefs = _prefs!.copyWith(goal: val));
          }),
          _buildNumberInput('Goal Per Session', _prefs!.goalPerSession, (val) {
            setState(() => _prefs = _prefs!.copyWith(goalPerSession: val));
          }),
          _buildSwitch('Focus Button', _prefs!.focusButton, (val) {
            setState(() => _prefs = _prefs!.copyWith(focusButton: val));
          }),
          _buildSwitch('Show Lateral Menu', _prefs!.showLateralMenu, (val) {
            setState(() => _prefs = _prefs!.copyWith(showLateralMenu: val));
          }),
          _buildSwitch('Spell Check', _prefs!.spellCheck, (val) {
            setState(() => _prefs = _prefs!.copyWith(spellCheck: val));
          }),
          _buildSwitch('Global Tips', _prefs!.globalTips, (val) {
            setState(() => _prefs = _prefs!.copyWith(globalTips: val));
          }),
          const SizedBox(height: 20),
          ElevatedButton(onPressed: _save, child: const Text('Save')),
        ],
      ),
    );
  }

  Widget _buildDropdown(String label, String value, List<String> options, Function(String) onChanged) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label),
        DropdownButton<String>(
          value: value,
          onChanged: (val) => onChanged(val!),
          items: options.map((e) => DropdownMenuItem(value: e, child: Text(e))).toList(),
        ),
        const SizedBox(height: 10),
      ],
    );
  }

  Widget _buildNumberInput(String label, int value, Function(int) onChanged) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label),
        TextFormField(
          initialValue: value.toString(),
          keyboardType: TextInputType.number,
          onChanged: (val) => onChanged(int.tryParse(val) ?? value),
        ),
        const SizedBox(height: 10),
      ],
    );
  }

  Widget _buildSwitch(String label, bool value, Function(bool) onChanged) {
    return SwitchListTile(
      title: Text(label),
      value: value,
      onChanged: onChanged,
    );
  }
}
