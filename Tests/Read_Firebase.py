import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

def watch_garage_doors():
    doc_ref = db.collection(u'GarageDoors')

    def on_snapshot(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            print(f"Door ID: {doc.id}, Status: {doc.to_dict()}")
        print('Waiting for changes...')

    doc_ref.on_snapshot(on_snapshot)

if __name__ == '__main__':
    print("Starting to watch garage door statuses...")
    watch_garage_doors()
    while True:
        time.sleep(1)
