import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:smart_garage_app/garage_control.dart';
import 'auth_wrapper.dart'; 
import 'garage_control.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(SmartGarage());
}

class SmartGarage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Smart Garage',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        scaffoldBackgroundColor: Colors.white,
        buttonTheme: ButtonThemeData(
          buttonColor: Colors.blue,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18.0)),
          padding: EdgeInsets.symmetric(horizontal: 20.0, vertical: 10.0),
        ),
      ),
      home: AuthWrapper(), 
    );
  }
}
