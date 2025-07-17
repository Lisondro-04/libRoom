import 'package:flutter/material.dart';

class GeneralDataScreen extends StatelessWidget {
  GeneralDataScreen({super.key});

  final TextEditingController titleController = TextEditingController();
  final TextEditingController seriesController = TextEditingController();
  final TextEditingController volumeController = TextEditingController();
  final TextEditingController genresController = TextEditingController();
  final TextEditingController licenseController = TextEditingController();
  final TextEditingController authorController = TextEditingController();
  final TextEditingController emailController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          // Sidebar
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
                ...[
                  'General',
                  'Characters',
                  'Scheme',
                  'World',
                  'Write',
                  'Notes',
                  'Export',
                  'Settings',
                  'Preferences'
                ].map((item) => Padding(
                      padding: const EdgeInsets.symmetric(vertical: 4.0),
                      child: TextButton(
                        onPressed: () {},
                        child: Text(item),
                      ),
                    )),
              ],
            ),
          ),

          // Main Content
          Expanded(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'General Data',
                    style: TextStyle(
                      fontSize: 26,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Here you can edit the metadata of your project.',
                    style: TextStyle(fontSize: 16),
                  ),
                  const SizedBox(height: 24),

                  // Form
                  Row(
                    children: [
                      // Column 1
                      Expanded(
                        child: Column(
                          children: [
                            buildField('Title', titleController),
                            buildField('Series', seriesController),
                            buildField('Volume', volumeController),
                            buildField('Genres', genresController),
                            buildField('License', licenseController),
                          ],
                        ),
                      ),
                      const SizedBox(width: 24),

                      // Column 2
                      Expanded(
                        child: Column(
                          children: [
                            buildField('Author', authorController),
                            buildField('E-mail', emailController),
                          ],
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 32),

                  // Buttons
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      ElevatedButton(
                        onPressed: () {
                          // Aquí iría la lógica para guardar
                        },
                        child: const Text('Save'),
                      ),
                      const SizedBox(width: 20),
                      OutlinedButton(
                        onPressed: () {
                          Navigator.pop(context);
                        },
                        child: const Text('Back to Menu'),
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

  Widget buildField(String label, TextEditingController controller) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6.0),
      child: TextField(
        controller: controller,
        decoration: InputDecoration(
          labelText: label,
          filled: true,
          fillColor: Colors.grey[300],
          border: const OutlineInputBorder(),
        ),
      ),
    );
  }
}
