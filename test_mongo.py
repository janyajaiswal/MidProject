# test_mongo.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGO_URI")
client = MongoClient(uri)

try:
    print("✅ Databases:", client.list_database_names())
except Exception as e:
    print("❌ Error:", e)
