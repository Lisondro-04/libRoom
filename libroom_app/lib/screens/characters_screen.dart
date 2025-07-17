import 'package:flutter/material.dart';

class CharactersScreen extends StatefulWidget {
  const CharactersScreen({super.key});

  @override
  State<CharactersScreen> createState() => _CharactersScreenState();
}

class _CharactersScreenState extends State<CharactersScreen> {
  String selectedSection = 'Physical Appearance';
  String sectionContent = 'Lorem ipsum dolor sit amet...'; // Se puede cargar desde backend
  String characterName = 'Character Chosen Name';

  final List<String> menuItems = [
    'General',
    'Characters',
    'Scheme',
    'World',
    'Write',
    'Notes',
    'Export',
    'Settings',
    'Preferences',
  ];

  final List<String> sections = [
    'Physical Appearance',
    'Background',
    'Personality',
    'Skills',
    'Relationships',
    'Arc Summary',
    'Important Info',
    'Stats',
    'Other',
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          // Left Sidebar
          Container(
            width: 140,
            color: Colors.grey[200],
            child: Column(
              children: [
                Container(
                  padding: const EdgeInsets.all(16),
                  child: const Text(
                    'LibRoom',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 18,
                    ),
                  ),
                ),
                const Divider(),
                ...menuItems.map((item) => Padding(
                      padding: const EdgeInsets.symmetric(vertical: 4.0),
                      child: TextButton(
                        onPressed: () {},
                        child: Text(item),
                      ),
                    )),
              ],
            ),
          ),

          // Main Area
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  const Text(
                    'Characters',
                    style: TextStyle(
                      fontSize: 26,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 12),

                  // Filters + Button
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          DropdownButton<String>(
                            value: 'Main Characters',
                            items: ['Main Characters', 'All']
                                .map((e) => DropdownMenuItem(
                                      value: e,
                                      child: Text(e),
                                    ))
                                .toList(),
                            onChanged: (_) {},
                          ),
                          const SizedBox(width: 12),
                          DropdownButton<String>(
                            value: 'Secondary Characters',
                            items: ['Secondary Characters', 'All']
                                .map((e) => DropdownMenuItem(
                                      value: e,
                                      child: Text(e),
                                    ))
                                .toList(),
                            onChanged: (_) {},
                          ),
                        ],
                      ),
                      ElevatedButton(
                        onPressed: () {},
                        child: const Text('New Character'),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  // Main content
                  Expanded(
                    child: Row(
                      children: [
                        // Left section selector
                        Container(
                          width: 220,
                          color: Colors.grey[800],
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.stretch,
                            children: [
                              Container(
                                color: Colors.black87,
                                padding: const EdgeInsets.all(12),
                                child: Text(
                                  characterName,
                                  style: const TextStyle(
                                    color: Colors.white,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                              ),
                              Expanded(
                                child: ListView(
                                  children: sections.map((section) {
                                    return TextButton(
                                      style: TextButton.styleFrom(
                                        backgroundColor: section == selectedSection
                                            ? Colors.grey[700]
                                            : Colors.grey[900],
                                        foregroundColor: Colors.white,
                                        padding: const EdgeInsets.symmetric(
                                            vertical: 12, horizontal: 16),
                                      ),
                                      onPressed: () {
                                        setState(() {
                                          selectedSection = section;
                                          // Aquí deberías cargar el contenido real del backend
                                          sectionContent =
                                              'Contenido de $section...';
                                        });
                                      },
                                      child: Text(section),
                                    );
                                  }).toList(),
                                ),
                              ),
                            ],
                          ),
                        ),

                        // Right editor panel
                        Expanded(
                          child: Container(
                            color: Colors.grey[300],
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  selectedSection,
                                  style: const TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 12),
                                Expanded(
                                  child: TextField(
                                    controller: TextEditingController(
                                        text: sectionContent),
                                    maxLines: null,
                                    expands: true,
                                    decoration: const InputDecoration(
                                      border: OutlineInputBorder(),
                                      filled: true,
                                      fillColor: Colors.white,
                                    ),
                                    onChanged: (value) {
                                      // Aquí se puede hacer un debounce + PATCH al backend
                                    },
                                  ),
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
            ),
          ),
        ],
      ),
    );
  }
}
