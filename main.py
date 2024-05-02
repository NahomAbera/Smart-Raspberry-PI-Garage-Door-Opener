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
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO pins
RELAY_PINS = {'door1': 17, 'door2': 27}
MAGNETIC_SWITCHES = {'door1': [22, 23], 'door2': [24, 25]}

# Set up relay pins
for pin in RELAY_PINS.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)  # Relays are active low

# Set up magnetic switch pins
for pins in MAGNETIC_SWITCHES.values():
    for pin in pins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize door status to monitor changes
last_status = {door_id: None for door_id in MAGNETIC_SWITCHES}

def read_command():
    for door_id, pin in RELAY_PINS.items():
        doc = db.collection('Commands').document(f'{door_id}_command').get()

        if doc.exists:
            command = doc.to_dict().get('command', '')

            if command == 'open' or command == 'close':
                # Activate the relay (simulate button press)
                GPIO.output(pin, GPIO.LOW)  # Assume LOW to activate
                time.sleep(1)  # Hold the button for 1 second

                # Deactivate the relay (release button)
                GPIO.output(pin, GPIO.HIGH)  # Assume HIGH to deactivate
                time.sleep(2)  # Wait for 2 seconds before any further action

def update_status_and_log():
    for door_id, pins in MAGNETIC_SWITCHES.items():
        # Read the current status from the switches
        if GPIO.input(pins[0]) == GPIO.LOW or GPIO.input(pins[1]) == GPIO.LOW:
            current_status = 'open'
        else:
            current_status = 'closed'

        # Retrieve the last recorded command to determine if the door is opening or closing
        command_doc = db.collection('Commands').document(f'{door_id}_command').get()
        if command_doc.exists:
            last_command = command_doc.to_dict().get('command', '')

            # Determine transitional states based on the last command
            if last_command == 'open' and current_status == 'closed':
                current_status = 'opening'
            elif last_command == 'close' and current_status == 'open':
                current_status = 'closing'

        # Check for status change and update Firestore and logs if there is a change
        if last_status[door_id] != current_status:
            last_status[door_id] = current_status
            
            # Update the current status in Firestore
            db.collection('CurrentStatus').document(door_id).set({'status': current_status}, merge=True)

            # Log the change
            db.collection('Logs').add({
                'door': door_id,
                'status': f'door {current_status}',
                'timestamp': datetime.now()
            })

def main():
    while True:
        read_command()
        update_status_and_log()
        time.sleep(1) 

if __name__ == '__main__':
    main()