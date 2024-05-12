import RPi.GPIO as GPIO
import firebase_admin
from firebase_admin import credentials, firestore
import time
from datetime import datetime
import threading

#Initialize Firebase
try:
    cred = credentials.Certificate('garagedoorbackend-firebase-adminsdk-k64wf-23f215d05e.json')
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print("Firebase initialization error:", e)
    exit(1)

#GPIO Setup
try:
    GPIO.setmode(GPIO.BOARD)  
    GPIO.setwarnings(False)
    GPIO.setup(29, GPIO.IN, GPIO.PUD_UP) #Door 1 is Closed sensor
    GPIO.setup(31, GPIO.IN, GPIO.PUD_UP) #Door 1 is Open sensor
    GPIO.setup(33, GPIO.IN, GPIO.PUD_UP) #Door 2 is Closed sensor
    GPIO.setup(37, GPIO.IN, GPIO.PUD_UP) #Door 2 is Open sensor

    GPIO.setup(7, GPIO.OUT)          #Door 1 Relay to Open Door
    GPIO.output(7, GPIO.HIGH)
    GPIO.setup(11, GPIO.OUT)     #Not in use
    GPIO.output(11, GPIO.HIGH)
    GPIO.setup(13, GPIO.OUT)     #Door 2 Relay to Open Door
    GPIO.output(13, GPIO.HIGH)
    GPIO.setup(15, GPIO.OUT)     #Not in use
    GPIO.output(15, GPIO.HIGH)
except Exception as e:
    print("GPIO setup error:", e)
    exit(1)

# Define GPIO pins
RELAY_PINS = {'door1': 7, 'door2': 13}
MAGNETIC_SWITCHES = {'door1': [29, 31], 'door2': [33, 37]}

def excute_command():
    try:
        for door_id, pin in RELAY_PINS.items():
            com = db.collection('Commands').document(f'{door_id}').get()
            stt = db.collection('CurrentStatus').document(f'{door_id}').get()
            if com.exists and stt.exists:
                current_command = com.to_dict().get('command', '')
                last_command = com.to_dict().get('last_command', '')
                current_status = stt.to_dict().get('status', '')

                if current_status == 'opening' or current_status == 'closing':
                    continue
                elif current_command != last_command:
                    GPIO.output(pin, GPIO.LOW)  
                    time.sleep(1)  
                    GPIO.output(pin, GPIO.HIGH)
                    time.sleep(1)
                    db.collection('Commands').document(door_id).set({'last_command': current_command}, merge=True)
    except Exception as e:
        print("Error in excute_command:", e)

def update_status():
    try:
        for door_id, pins in MAGNETIC_SWITCHES.items():
            lst_stt = db.collection('CurrentStatus').document(door_id).get()
            if lst_stt.exists:
                last_status = lst_stt.to_dict().get('status', '')
            switch_1 = GPIO.input(pins[0])
            switch_2 = GPIO.input(pins[1])

            if switch_1 == GPIO.LOW:
                current_status = 'open'
            elif switch_2 == GPIO.LOW:
                current_status = 'close'
            elif lst_stt.exists:
                if last_status == 'open' or last_status == 'closing':
                    current_status = 'closing'
                elif last_status == 'close' or last_status == 'opening':
                    current_status = 'opening'
                    
            if lst_stt.exists and current_status != last_status:
                db.collection('CurrentStatus').document(door_id).set({'status': current_status}, merge=True)
                if current_status in ['open', 'close']:
                    db.collection('Logs').add({
                        'door': door_id,
                        'status': f'door {current_status}ed',
                        'timestamp': datetime.now()
                    })
    except Exception as e:
        print("Error in update_status:", e)


def main():
    try:
        while True:
            excute_command()
            # update_status()
    finally:
        GPIO.cleanup()

# #Threaded version
# def main():
#     try:
#         excute_command_thread = threading.Thread(target=excute_command)
#         update_status_thread = threading.Thread(target=update_status)

#         excute_command_thread.start()
#         update_status_thread.start()

#         excute_command_thread.join()
#         update_status_thread.join()
#     finally:
#         GPIO.cleanup()

if __name__ == '__main__':
    main()