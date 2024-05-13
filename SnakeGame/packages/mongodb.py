import json
import os
from pymongo import MongoClient

from bson import ObjectId

DB_DIR = 'db'
DB_FILE = 'data.json'

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['game_database']
collection = db['game_sessions']


def cleanup_database():
    collection.delete_many({})


# Function to check if the database location and file exist
def check_database_existence():
    if os.path.exists(DB_DIR) and os.path.isfile(os.path.join(DB_DIR, DB_FILE)):
        # Check if file is not empty
        if os.path.getsize(os.path.join(DB_DIR, DB_FILE)) > 0:
            return True
    return False


# Function to read data from JSON file
def read_data_from_file(filename):
    with open(filename, 'r') as file:
        return json.load(file)


# Function to write data to JSON file
def write_data_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)


# Function to store game result in MongoDB
def store_game_result(name, score):
    collection.insert_one({'name': name, 'score': score})


# Function to initialize the database with JSON data
def initialize_database_from_file(filename):
    if check_database_existence():
        data = read_data_from_file(filename)
        if data:  # Check if data is not empty
            collection.insert_many(data)


# Function to convert MongoDB documents to JSON-serializable format
def convert_to_json_serializable(documents):
    for doc in documents:
        doc['_id'] = str(doc['_id'])  # Convert ObjectId to string
    return documents


# Function to dump data to JSON upon application closure
def dump_data_to_file(filename):
    data = list(collection.find())
    data = convert_to_json_serializable(data)  # Convert MongoDB documents to JSON-serializable format
    write_data_to_file(data, filename)


# Function to initialize the database
def initialize_database():
    if not check_database_existence():
        # Create database directory if it doesn't exist
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)
        # Create empty data file
        with open(os.path.join(DB_DIR, DB_FILE), 'w') as file:
            json.dump([], file)
    else:
        initialize_database_from_file(os.path.join(DB_DIR, DB_FILE))


def check_player_exists(name):
    return collection.find_one({'name': name})


def get_top_scores():
    try:
        # Assuming `collection` is defined within this module or initialized in a function that sets it up
        return list(collection.find().sort("score", -1))
    except Exception as e:
        print(f"Failed to fetch top scores: {e}")
        return []
