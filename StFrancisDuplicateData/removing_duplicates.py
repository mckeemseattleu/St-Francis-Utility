import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initializing Firebase only if it hasn't been initialized yet
if not firebase_admin._apps:
    # Load the credentials from the downloaded Firebase Admin SDK JSON file
    cred = credentials.Certificate("key.json")  # Instead of key.json put path to your service account key
    # Initialize the Firebase app with these credentials
    firebase_admin.initialize_app(cred)

# Getting a Firestore client to interact with the Firestore database
db = firestore.client()

def remove_duplicates(collection_name, duplicates):
    """
    In this section we are remove duplicate documents from the client Firestore collection.

    :param collection_name: Name of the collection from which to remove duplicates.
    :param duplicates: List of dictionaries representing duplicate documents to remove.
    """
    # Referencing the collection in Firestore
    collection_ref = db.collection(collection_name)
    for item in duplicates:
        # Extracting the document ID from the duplicate item
        doc_id = item['doc_id']
        # Deleting the document with the specified ID
        collection_ref.document(doc_id).delete()
        print(f"Deleted duplicate document with id: {doc_id}")

def main():
    """
    This is the main function to arrange loading duplicates and removing them from the Firestore collection.
    """
    collection_name = 'clients'  # This is theName of the Firestore collection to clean

    # Loading the list of duplicates from the JSON file
    try:
        with open('duplicates.json', 'r') as f:
            duplicates = json.load(f)  # Loading the list of duplicates from the file
    except FileNotFoundError:
        print("duplicates.json file not found. Please run the script to find duplicates first.")
        return

    # Removing the duplicates from the Firestore collection
    if duplicates:
        remove_duplicates(collection_name, duplicates)
    else:
        print("No duplicates found to remove.")

if __name__ == "__main__":
    main()
