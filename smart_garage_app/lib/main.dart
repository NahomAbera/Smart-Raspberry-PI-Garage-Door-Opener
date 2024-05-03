import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(MyApp());
}
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Garage',
      theme: ThemeData(
        primarySwatch: Colors.blue, 
        scaffoldBackgroundColor: Color.fromARGB(255, 255, 255, 255), 
        buttonTheme: ButtonThemeData(
          buttonColor: Colors.blue, 
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18.0)),
          padding: EdgeInsets.symmetric(horizontal: 20.0, vertical: 10.0),
        ),
      ),
      home: GarageControlPage(),
    );
  }
}

class GarageControlPage extends StatefulWidget {
  @override
  _GarageControlPageState createState() => _GarageControlPageState();
}

class _GarageControlPageState extends State<GarageControlPage> {
  final FirebaseFirestore _db = FirebaseFirestore.instance;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Smart Garage'),
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16.0),
        child: Column(
          children: [
            doorPanel('door1'),
            SizedBox(height: 30), 
            doorPanel('door2'),
          ],
        ),
      ),
    );
  }

  Widget doorPanel(String doorId) {
    return Card( 
      elevation: 4.0,
      
      child: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Text(doorId.toUpperCase(), style: Theme.of(context).textTheme.headline6),
            SizedBox(height: 10),
            StreamBuilder<DocumentSnapshot>(
              stream: _db.collection('CurrentStatus').doc(doorId).snapshots(),
              builder: (context, snapshot) {
                if (!snapshot.hasData || snapshot.data == null || snapshot.data!.data() == null) {
                  return CircularProgressIndicator();
                }
                var status = snapshot.data!.data()! as Map<String, dynamic>;
                var doorStatus = status['status'] as String;
                return Column(
                  children: [
                    Image.asset('assets/${doorStatus}.png', width: 200, height: 200),
                    SizedBox(height: 20),
                    doorControlButtons(doorStatus, doorId),
                  ],
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget doorControlButtons(String status, String doorId) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        if (status == 'close')
          ElevatedButton(
            onPressed: () => sendCommand('open', doorId),
            child: Text('Open'),
            style: ElevatedButton.styleFrom(backgroundColor: Color.fromARGB(255, 4, 53, 250)), 
          ),
        if (status == 'open')
          ElevatedButton(
            onPressed: () => sendCommand('close', doorId),
            child: Text('Close'),
            style: ElevatedButton.styleFrom(backgroundColor: Color.fromARGB(255, 238, 46, 7)),
          ),
      ],
    );
  }

  void sendCommand(String command, String doorId) {
    _db.collection('Commands').doc(doorId).set({'command': command});
  }
}
