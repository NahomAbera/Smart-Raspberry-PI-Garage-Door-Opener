import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

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
        backgroundColor: Color.fromRGBO(2, 44, 67, 1), 
        title: Text('Smart Garage', style: TextStyle(color: Colors.white)),
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(32.0),  
        child: Column(
          children: [
            doorPanel('door1'),
            SizedBox(height: 25),  
            doorPanel('door2'),
            SizedBox(height: 40),
              Align(
                alignment: Alignment.bottomLeft,
                child: Text('Developed by Nahom Abera', style: TextStyle(fontSize: 12, color: Colors.grey)),
              ),
          ],
          
        ),
      ),
    );
  }

  Widget doorPanel(String doorId) {
    return Card(
      elevation: 4.0,
      child: Padding(
        padding: EdgeInsets.all(24.0),
        child: Container(
          width: double.infinity, 
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Text(doorId.toUpperCase(), style: Theme.of(context).textTheme.headline5),  
              SizedBox(height: 20),
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
                      Image.asset('assets/${doorStatus}.png', width: 100, height: 100),
                      SizedBox(height: 20),
                      Text("Status: $doorStatus", style: TextStyle(fontSize: 21, fontWeight: FontWeight.bold)),
                      SizedBox(height: 20),
                      if (doorStatus == 'open' || doorStatus == 'close')
                        doorControlButtons(doorStatus, doorId),
                    ],
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget doorControlButtons(String status, String doorId) {
    return ElevatedButton(
      onPressed: () => sendCommand(status == 'close' ? 'open' : 'close', doorId),
      child: Text(status == 'close' ? 'Open' : 'Close'),
      style: ElevatedButton.styleFrom(
        backgroundColor: status == 'close' ? Colors.green : Colors.redAccent,
        padding: EdgeInsets.symmetric(horizontal: 30, vertical: 20),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
    );
  }

  void sendCommand(String command, String doorId) {
    _db.collection('Commands').doc(doorId).set({'command': command});
  }
}
