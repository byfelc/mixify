from pymongo import MongoClient
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path='myapp\.env')
MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client['mixifydb']

collections = db.list_collection_names()
for collection in collections:
    print(collection)

