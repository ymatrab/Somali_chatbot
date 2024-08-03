import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


service_account_key_path = 'med-assistant-296af-firebase-adminsdk-nj0ez-af721bdf4c.json'


# Initialize the Firebase app with the service account key
cred = credentials.Certificate(service_account_key_path)


# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

def verify_connection(user_id):
    try:
        # Attempt to read a document from the 'users' collection
        doc_ref = db.collection('users').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return True
        else:
            return False
    except Exception as e:
        print(f'An error occurred: {e}')

def get_memory(chat_id):
    try:
        # Attempt to read a document from the 'users' collection
        doc_ref = db.collection('chat').document(chat_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return False
    except Exception as e:
        print(f'An error occurred: {e}')

def message_from_chat(chat):
    message={}
    if chat['type']=='text':
        message['role']=chat['role']
        message['text']=chat['text']['value']
    elif chat['type']=='image':
        message['role']=chat['role']
        message['text']=chat['message']['content']
    return message


