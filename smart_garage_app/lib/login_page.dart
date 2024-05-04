import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'garage_control.dart';

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final FirebaseFirestore _db = FirebaseFirestore.instance;
  String? _selectedUser;
  final TextEditingController _passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color.fromRGBO(2, 44, 67, 1),
        title: Text('Login', style: TextStyle(color: Colors.white)),
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: EdgeInsets.all(32.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Image.asset('assets/logo.png', width: 300, height: 300),
              SizedBox(height: 40),
              Text('WELCOME!', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.blueGrey[800])),
              SizedBox(height: 20),
              StreamBuilder<QuerySnapshot>(
                stream: _db.collection('AllowedUsers').snapshots(),
                builder: (context, snapshot) {
                  if (!snapshot.hasData) return CircularProgressIndicator();
                  var docs = snapshot.data!.docs;
                  List<DropdownMenuItem<String>> dropdownItems = docs.map((doc) {
                    return DropdownMenuItem<String>(
                      value: doc['name'],
                      child: Text(doc['name']),
                    );
                  }).toList();
                  return DropdownButtonFormField<String>(
                    decoration: InputDecoration(
                      enabledBorder: OutlineInputBorder(
                        borderSide: BorderSide(color: Colors.blueGrey[300]!, width: 2),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      filled: true,
                      fillColor: Colors.grey[200],
                    ),
                    hint: Text("Who are you?"),
                    value: _selectedUser,
                    onChanged: (value) {
                      setState(() {
                        _selectedUser = value;
                        _passwordController.clear();
                      });
                    },
                    items: dropdownItems,
                    validator: (value) => value == null ? 'Please select a user' : null,
                  );
                },
              ),
              SizedBox(height: 20),
              TextField(
                controller: _passwordController,
                enabled: _selectedUser != null,
                decoration: InputDecoration(
                  labelText: _selectedUser == "Developer" ? "Developer Password" : "User Password",
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  prefixIcon: Icon(Icons.lock_outline),
                ),
                obscureText: true,
              ),
              SizedBox(height: 30),
              ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Color.fromRGBO(2, 44, 67, 1),
                  padding: EdgeInsets.symmetric(horizontal: 50, vertical: 15),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                onPressed: _selectedUser == null ? null : () => _login(),
                child: Text('Login', style: TextStyle(fontSize: 16)),
              ),
              SizedBox(height: 40),
              Align(
                alignment: Alignment.bottomLeft,
                child: Text('Developed by Nahom Abera', style: TextStyle(fontSize: 12, color: Colors.grey)),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _login() async {
    if (_selectedUser != null && _passwordController.text.isNotEmpty) {
      String correctPassword = _selectedUser == "Developer" ? "xyz001" : "abc001";
      if (_passwordController.text == correctPassword) {
        await _db.collection('UserLogs').add({
          'name': _selectedUser,
          'timestamp': FieldValue.serverTimestamp()
        });
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => GarageControlPage()));
      } else {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Incorrect password')));
      }
    }
  }
}
