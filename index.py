import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create Flask app instance
app = Flask(__name__)

# Retrieve MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")

# Establish MongoDB connection
client = MongoClient(MONGO_URI)

@app.route('/', methods=['GET'])
def index():
    return "Welcome to the MongoDB API"

@app.route('/add_data', methods=['POST'])
def add_data():
    try:
        data = request.json
        db_name = data['db_name']
        collection_name = data['collection_name']
        new_data = data['data']
        
        # Connect to the database and collection
        db = client[db_name]
        collection = db[collection_name]

        # Insert the data into the collection
        result = collection.insert_one(new_data)
        
        return jsonify({"message": "Data added successfully", "inserted_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/delete_data', methods=['POST'])
def delete_data():
    try:
        data = request.json
        db_name = data['db_name']
        collection_name = data['collection_name']
        filter_data = data['filter']
        
        # Connect to the database and collection
        db = client[db_name]
        collection = db[collection_name]

        # Delete the data based on the filter
        result = collection.delete_one(filter_data)
        
        if result.deleted_count > 0:
            return jsonify({"message": "Data deleted successfully"}), 200
        else:
            return jsonify({"message": "No matching data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    try:
        data = request.json
        db_name = data['db_name']
        collection_name = data['collection_name']
        filter_data = data.get('filter', {})  # Default to an empty filter (get all data)
        
        # Connect to the database and collection
        db = client[db_name]
        collection = db[collection_name]

        # Fetch data based on the filter
        result = collection.find(filter_data)
        
        # Convert MongoDB result to a list of dictionaries
        result_list = [document for document in result]
        
        return jsonify({"data": result_list}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
