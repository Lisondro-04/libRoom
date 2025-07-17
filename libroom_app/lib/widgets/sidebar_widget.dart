import 'package:flutter/material.dart';

class Sidebar extends StatelessWidget {
  const Sidebar({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 200,
      color: Colors.grey[200],
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          InkWell(
            onTap: () => Navigator.pushReplacementNamed(context, '/project'),
            child: Container(
              padding: EdgeInsets.all(16),
              child: Row(
                children: [
                  Icon(Icons.home),
                  SizedBox(width: 8),
                  Text('LibRoom', style: TextStyle(fontWeight: FontWeight.bold)),
                ],
              ),
            ),
          ),
          _navButton(context, 'General', '/general'),
          _navButton(context, 'Characters', '/characters'),
          _navButton(context, 'Outline', '/outline'),
          _navButton(context, 'World', '/world'),
          _navButton(context, 'Editor', '/editor'),
          _navButton(context, 'Notes', '/notes'),
          _navButton(context, 'Export', '/export'),
          _navButton(context, 'Settings', '/settings'),
          //_navButton(context, 'Preferences', '/preferences'),
        ],
      ),
    );
  }

  Widget _navButton(BuildContext context, String label, String route) {
    return TextButton(
      onPressed: () => Navigator.pushReplacementNamed(context, route),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        child: Align(
          alignment: Alignment.centerLeft,
          child: Text(label, style: TextStyle(fontSize: 16)),
        ),
      ),
    );
  }
}
