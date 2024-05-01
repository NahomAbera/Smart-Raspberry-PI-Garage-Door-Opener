import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("C:/Users/nahom/OneDrive/Documents/Projects/Smart_Raspberry_PI_Garage_Door_Opener/Firebase/garagedoorbackend-firebase-adminsdk-k64wf-23f215d05e.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def update_command(door_id, command):
    doc_ref = db.collection(u'Commands').document(f'{door_id}_command')

    command_data = {
        'door_id': door_id,
        'command': command,
        'timestamp': firestore.SERVER_TIMESTAMP,
        'executed': False
    }

    doc_ref.set(command_data, merge=True)
    print(f"Command '{command}' updated for {door_id}.")

if __name__ == '__main__':
    while True:
        door_id = input("Enter door ID (door1 or door2): ")
        command = input("Enter command (open or close): ")
        update_command(door_id, command)
