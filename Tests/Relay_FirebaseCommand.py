import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import credentials, firestore
import time
from datetime import datetime

import time

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT)     
GPIO.output(7, GPIO.HIGH)   
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.HIGH)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.HIGH)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, GPIO.HIGH)

cred = credentials.Certificate('garagedoorbackend-firebase-adminsdk-k64wf-23f215d05e.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

RELAY_PINS = {'door1': 7, 'door2': 13}


def read_command():
    for door_id, pin in RELAY_PINS.items():
        com = db.collection('Commands').document(f'{door_id}').get()
        stt = db.collection('CurrentStatus').document(f'{door_id}').get()
        print(stt,"\n")
        print(com,"\n")
        if com.exists and stt.exists:
            command = com.to_dict().get('command', '')
            current_status = stt.to_dict().get('status', '')
            print(current_status," current status\n")
            print(command ," command\n")

            if current_status == 'opening' or current_status == 'closing':
                continue
            elif current_status != command:
                GPIO.output(pin, GPIO.LOW)
                time.sleep(1)  
                GPIO.output(pin, GPIO.HIGH) 
                time.sleep(2)  
                db.collection('CurrentStatus').document(door_id).set({'status': command}, merge=True)


def main():
    while True:
        read_command()
        time.sleep(1) 

if __name__ == '__main__':
    main()