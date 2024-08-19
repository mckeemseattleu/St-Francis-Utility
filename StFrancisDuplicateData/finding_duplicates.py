import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initializing Firebase only if it hasn't been initialized yet
if not firebase_admin._apps:
    # Loading the credentials from the downloaded Firebase Admin SDK JSON file
    cred = credentials.Certificate("key.json")  # Instead of key.json put path to your service account key
    # Initializing the Firebase app with these credentials
    firebase_admin.initialize_app(cred)

# Getting a Firestore client to interact with the Firestore database
db = firestore.client()

def fetch_data(collection_name):
    """
    In this we fetched all documents from the Client Firestore collection.

    :param collection_name: Name of the collection from which to fetch data.
    :return: A list of dictionaries, each representing a document in the collection.
    """
    # Referencing the collection in Firestore
    collection_ref = db.collection(collection_name)
    # Streaming all documents in the collection
    docs = collection_ref.stream()
    # Initializing an empty list to hold the document data
    data = []
    for doc in docs:
        # Converting each document to a dictionary
        doc_dict = doc.to_dict()
        # Adding the document ID to the dictionary for reference
        doc_dict['doc_id'] = doc.id
        # Appending the document dictionary to the data list
        data.append(doc_dict)
    return data

def find_duplicates(data, key_fields):
    """
    In this section we are indentifying duplicate documents based on three key fields.

    :param data: List of document dictionaries fetched from Firestore.
    :param key_fields: List of field names that should be used to identify duplicates.
    :return: A list of dictionaries representing duplicate documents.
    """
    seen = {}  # It is a Dictionary to keep track of unique documents
    duplicates = []  # A List to store duplicate documents
    for item in data:
        # Creating a tuple key from the specified fields in the document
        key = tuple(item[field] for field in key_fields)
        if key in seen:
            # If the key is already seen, this document is a duplicate
            duplicates.append(item)
        else:
            # If the key is new, store the document ID for future reference
            seen[key] = item['doc_id']
    return duplicates

def main():
    """
    This is the main function to initiate fetching data, finding duplicates, and saving them to a file.
    """
    collection_name = 'clients'  # Name of the Firestore collection to analyze
    key_fields = ['firstNameLower', 'lastNameLower', 'birthday']  # Fields to check for duplicates 
    # You can put fields according to your requirement

    # Step 1: Fetching all data from the clients collection
    data = fetch_data(collection_name)

    # Step 2: Identifying duplicates based on the specified key fields
    duplicates = find_duplicates(data, key_fields)
    print(f"Found {len(duplicates)} duplicate records based on the fields: {key_fields}")

    # Saving the duplicates to a JSON file for later review and removal
    if duplicates:
        with open('duplicates.json', 'w') as f:
            json.dump(duplicates, f, indent=4)  # Saving with indentation for readability
        print("Duplicates have been saved to duplicates.json")
    else:
        print("No duplicates found.")

if __name__ == "__main__":
    # Executing the main function when the script is run
    main()
