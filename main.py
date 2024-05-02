import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import credentials, firestore
import time
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate('path/to/your/firebase-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# GPIO Setup
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
GPIO.setwarnings(False)

# Define GPIO pins
RELAY_PINS = {'door1': 17, 'door2': 27}
MAGNETIC_SWITCHES = {'door1': [22, 23], 'door2': [24, 25]}  # Two switches per door

# Set up relay pins
for pin in RELAY_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Relays are usually active low

# Set up magnetic switch pins
for pins in MAGNETIC_SWITCHES.values():
    for pin in pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_command():
    for door_id, pin in RELAY_PINS.items():
        doc = db.collection('Commands').document(f'{door_id}_command').get()
        if doc.exists:
            command = doc.to_dict().get('command', '')
            if command == 'open':
                GPIO.output(pin, GPIO.LOW)  # Assume LOW to open
            elif command == 'close':
                GPIO.output(pin, GPIO.HIGH)  # Assume HIGH to close

def update_status_and_log():
    for door_id, pins in MAGNETIC_SWITCHES.items():
        # Example logic for determining door status
        if GPIO.input(pins[0]) == GPIO.LOW or GPIO.input(pins[1]) == GPIO.LOW:
            status = 'open'
        else:
            status = 'close'
        
        # Update CurrentStatus collection
        db.collection('CurrentStatus').document(door_id).set({'status': status})

        # Save the change to Logs collection
        db.collection('Logs').add({
            'door': door_id,
            'status': f'door {status}',
            'timestamp': datetime.now()
        })

def main():
    while True:
        read_command()
        update_status_and_log()
        time.sleep(1)  

if __name__ == '__main__':
    main()