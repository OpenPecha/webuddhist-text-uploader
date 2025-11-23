from pymongo import MongoClient

# MongoDB connection string
MONGO_URI = "mongodb+srv://webuddhist_db_user:JkasiqFZoQ4eLDVr@webuddhist-tst.b1zlfci.mongodb.net/"

# Database name (update this if different)
DB_NAME = "webuddhist"

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Access the database and collection
db = client[DB_NAME]
segments_collection = db['Segment']

# Text ID to delete
text_id_to_delete = "ababe817-f52f-4bd3-b5ef-5e639d109bee"

# Delete documents with the specified text_id
result = segments_collection.delete_many({"text_id": text_id_to_delete})

# Print the result
print(f"Deleted {result.deleted_count} document(s) with text_id: {text_id_to_delete}")

# Close the connection
client.close()

