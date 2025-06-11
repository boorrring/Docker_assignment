from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv
import os
import time

load_dotenv()  # Load MongoDB URI from .env file

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB connection with retry logic
def connect_to_mongodb(max_retries=5, retry_delay=2):
    for attempt in range(max_retries):
        try:
            mongo_uri = os.getenv("MONGO_URI")
            print(f"Attempting to connect to MongoDB (attempt {attempt + 1}/{max_retries})")
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            # Test the connection
            client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            return client
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"Failed to connect to MongoDB: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Could not connect to MongoDB.")
                raise e

# Initialize MongoDB connection
try:
    client = connect_to_mongodb()
    db = client["todo_database"]
    collection = db["todo_items"]
except Exception as e:
    print(f"Error initializing MongoDB connection: {str(e)}")
    raise e

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    try:
        if not request.is_json:
            return jsonify({"status": "error", "message": "Content-Type must be application/json"}), 415

        data = request.get_json()
        print("Received data:", data)
        
        # Extract fields from JSON data
        item_id = data.get("itemId")
        item_uuid = data.get("itemUuid")
        item_hash = data.get("itemHash")
        item_name = data.get("itemName")
        item_desc = data.get("itemDescription")

        if not item_id or not item_uuid or not item_hash or not item_name or not item_desc:
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        # Create document to insert
        todo_item = {
            "id": item_id,
            "uuid": item_uuid,
            "hash": item_hash,
            "name": item_name,
            "description": item_desc
        }
        print("Inserting document:", todo_item)

        # Insert the document
        result = collection.insert_one(todo_item)
        print("Inserted document ID:", result.inserted_id)

        return jsonify({"status": "success", "message": "Item saved successfully"}), 200
    except Exception as e:
        print("Error in submit_todo_item:", str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
