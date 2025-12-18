from pymongo import MongoClient
import uuid
from bson import Binary

# MongoDB connection string
MONGO_URI = "mongodb+srv://webuddhist_db_user:JkasiqFZoQ4eLDVr@webuddhist-tst.b1zlfci.mongodb.net/"

# Database name (update this if different)
DB_NAME = "webuddhist"

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Access the database and collection
db = client[DB_NAME]
segments_collection = db['Segment']
result = segments_collection.delete_many(
     {"text_id":"8ffc349e-a7c0-4c93-b550-9b88a0e72202"}
 )
print("result: ", result)
