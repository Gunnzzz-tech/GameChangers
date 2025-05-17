import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';

import 'helmet_detection.dart';
import 'speed_detection.dart';
import 'ambulance_detection.dart';

void main() => runApp(SafetyDetectionApp());

class SafetyDetectionApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Safety Detection',
      theme: ThemeData(
        scaffoldBackgroundColor: Colors.white,
        //primarySwatch: Colors.blue,
        fontFamily: 'Montserrat',
      ),
      home: HomePage(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class HomePage extends StatelessWidget {
  void _showUploadOptions(BuildContext context) {
    showModalBottomSheet(
      context: context,
      shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) {
        return Wrap(
          children: [
            ListTile(
              leading: Icon(Icons.folder_open),
              title: Text('Pick Video from Device'),
              onTap: () async {
                Navigator.pop(context);
                FilePickerResult? result = await FilePicker.platform.pickFiles(
                  type: FileType.video,
                );
                if (result != null) {
                  final filePath = result.files.single.path!;
                  ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                    content: Text('Selected: $filePath'),
                  ));
                  // You can now send this video path to your backend or detection page
                }
              },
            ),
            ListTile(
              leading: Icon(Icons.link),
              title: Text('Enter Video URL'),
              onTap: () {
                Navigator.pop(context);
                _showURLDialog(context);
              },
            ),
          ],
        );
      },
    );
  }

  void _showURLDialog(BuildContext context) {
    final TextEditingController urlController = TextEditingController();
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: Text('Enter Video URL'),
        content: TextField(
          controller: urlController,
          decoration: InputDecoration(hintText: 'https://...'),
        ),
        actions: [
          TextButton(
            child: Text('Cancel'),
            onPressed: () => Navigator.pop(context),
          ),
          ElevatedButton(
            child: Text('Submit'),
            onPressed: () {
              Navigator.pop(context);
              final url = urlController.text;
              if (url.isNotEmpty) {
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                  content: Text('Video URL: $url'),
                ));
                // You can now send this URL to your backend or detection page
              }
            },
          ),
        ],
      ),
    );
  }

  Widget _buildCard(String title, IconData icon, VoidCallback onTap) {
    return Card(
      color:Color.fromRGBO(145, 139, 139, 1.0),
      elevation: 4,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: ListTile(
        contentPadding: EdgeInsets.all(20),
        leading: Icon(icon, size: 32),
        title: Text(title, style: TextStyle(fontSize: 18, color:Color.fromRGBO(250, 250, 250, 1))),
        onTap: onTap,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Safety Detection Dashboard')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            _buildCard('Helmet Detection', Icons.security, () {
              Navigator.push(context,
                  MaterialPageRoute(builder: (_) => HelmetDetectionPage()));
            }),
            _buildCard('Speed Detection', Icons.speed, () {
              Navigator.push(context,
                  MaterialPageRoute(builder: (_) => SpeedDetectionPage()));
            }),
            _buildCard('Ambulance Detection', Icons.local_hospital, () {
              Navigator.push(context,
                  MaterialPageRoute(builder: (_) => AmbulanceDetectionPage()));
            }),
            SizedBox(height: 20),
            ElevatedButton.icon(
              icon: Icon(Icons.video_file, color:Colors.white),
              label: Text('Upload Video', style:TextStyle(color:Colors.white)),
              onPressed: () => _showUploadOptions(context),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.grey[600], // Change to any color you want
                //padding: EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                padding: EdgeInsets.symmetric(horizontal: 24, vertical: 16),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
