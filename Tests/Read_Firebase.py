import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

cred = credentials.Certificate("C:/Users/nahom/OneDrive/Documents/Projects/Smart_Raspberry_PI_Garage_Door_Opener/Firebase/garagedoorbackend-firebase-adminsdk-k64wf-23f215d05e.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def watch_commands():
    commands_ref = db.collection(u'Commands')

    def on_snapshot(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            print(f"Command ID: {doc.id}, Data: {doc.to_dict()}")
        print('Waiting for changes')

    commands_ref.on_snapshot(on_snapshot)

if __name__ == '__main__':
    print("Starting to watch commands...")
    watch_commands()
    while True:
        time.sleep(1)
