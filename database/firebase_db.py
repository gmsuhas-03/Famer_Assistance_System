import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

# Path to firebase service account key
BASE_DIR = Path(__file__).resolve().parent.parent
KEY_PATH = BASE_DIR / "firebase_key.json"

def get_firestore_client():
    """
    Safe Firebase initialization (Windows & FastAPI friendly)
    """
    if not firebase_admin._apps:
        cred = credentials.Certificate(KEY_PATH)
        firebase_admin.initialize_app(cred)

    return firestore.client()
