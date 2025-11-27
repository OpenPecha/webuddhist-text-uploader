from pymongo import MongoClient
import json
from bson import json_util
import uuid

# MongoDB connection string
MONGO_URI = "mongodb+srv://webuddhist_db_user:JkasiqFZoQ4eLDVr@webuddhist-tst.b1zlfci.mongodb.net/"

# Database name (update this if different)
DB_NAME = "webuddhist"

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Access the database and collection
db = client[DB_NAME]
segments_collection = db['Segment']
# text_id: str = "1a71aee2-0134-4945-ba0e-f169cf4ff6bb"


texts_collection = db['Text']

# Category ID to search for
category_id = "692570ca5bec0cce6528319d"

# Find all texts with the specified category
texts = texts_collection.find({"categories": {"$in": [category_id]}})

# Collect all text IDs
text_ids = []
pecha_text_ids = []

print(f"Texts with category: {category_id}\n")

text_ids = [str(uuid.UUID(bytes=text['_id'])) for text in texts]


array_commentary = [
    'bcb2be93-4ad2-4576-9a28-dc1d6245f7dd',
    '621b9afe-ddb1-45c3-b7c4-2e6f23788af9',
    '3be107d1-f043-457f-8cc8-67ca77bc53d7',
    '0e1bd2e0-5871-452a-840b-6b3512a04ed0',
    'd932cdeb-2097-4940-b62b-ad0ce7ca60ce',
    '85e13537-4014-43dd-8ecf-e6137e539e5a',
    'd33049b3-dddf-4f93-9bce-d0bcce60ff03',
    '553ebef0-7819-453e-9231-5178aa8cf1ec',
    '3586c85d-f415-4b76-a37b-ea290908ee39',
    '990131ab-dea4-43d3-bb97-e5dc7605ccfb',
    'abf411a8-efdd-4944-8959-6ec2901e5506',
    'ea5db2d8-e2cf-40c6-92b6-ec49e6d9dd59',
    'ea42ee34-bd12-47de-bd68-3c7560df166b',
    '69a82639-9290-4eac-80a1-147c653b35d4',
    '2afd27d6-b25e-4d0e-ac78-172c2f1fce12',
    '35907da7-da6f-4f4a-9c40-79270169a1ca',
    '37847f2a-cbe2-4b77-871f-ec0b1e23b6c6',
    '6d58b29c-9e01-46f6-9591-24071016fc1f',
    '2ec147de-5db2-4640-886b-a16f6d290ac2',
    '82aa2476-ded2-4cbc-9521-000b60fd37c6',
    '21e805a8-a6b2-4003-b054-43f50fa726ec',
    '3c804c3a-18ac-4495-bbc0-2eccbf2d1607',
    'c90730cc-1981-49bf-beac-d14180ba9199',
    '07a4ffd9-36fe-4a8b-86b2-bc50f3549dfe',
    '45c2e6b6-1212-4663-91f1-a5fee2f847a3',
    '6656bb41-ef85-4a7b-b03f-bc011ffe70a7',		
    '0edbd855-2713-4eb7-9ca0-22fa8b4199fd',		
    'b433d9c0-6b58-4aa8-b214-a2575d9d3efc',		
    '8b636c81-1ee4-4c40-bf4a-95b1604171e4',		
]
	

#Empty the entire mapping list from all documents
result = segments_collection.update_many(
    {"text_id": {"$in": array_commentary}},  # Empty filter matches all documents
    {"$set": {"mapping": []}}
)
print("result: ", result)
# Close the connection
client.close()

