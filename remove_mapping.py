from pymongo import MongoClient

# MongoDB connection string
MONGO_URI = "mongodb+srv://webuddhist_db_user:os9meNVni6FqC7if@webuddhist-prd.stty4w4.mongodb.net/"

# Database name (update this if different)
DB_NAME = "webuddhist"

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Access the database and collection
db = client[DB_NAME]
segments_collection = db['Segment']
text_id: str = "1a71aee2-0134-4945-ba0e-f169cf4ff6bb"

# Empty the entire mapping list from all documents
result = segments_collection.update_many(
    {},  # Empty filter matches all documents
    {"$set": {"mapping": []}}
)

# Print the result
print(f"Matched {result.matched_count} document(s)")
print(f"Modified {result.modified_count} document(s)")
print(f"Emptied mapping list from all segments with text_id: {text_id}")

# Close the connection
client.close()

array_version = [
    "1d1850a4-0748-4a73-b899-4faca34ccccf",
    "64011d92-cc92-4a66-b906-2a0e85bda256",
    "d4e2f1e3-96c5-4af2-8963-7d779d000e4a"
]

array_commentary = [
    "1a71aee2-0134-4945-ba0e-f169cf4ff6bb",
    "96385368-d6f8-4dff-aeab-bb4e4a9ed554"
]