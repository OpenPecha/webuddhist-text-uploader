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

text = db['Text']
toc = db['TableOfContent']
excluded_text_ids = [
        "ce887ec9-c794-41b3-ad99-2e61eb6f9c55",
        "67fdab62-7bd7-479d-b4ec-13379f974f54",
        "40d1fb48-daa7-42c6-a345-72070419f384",
        "2dc311ad-2247-4aeb-b6e8-6d427c9b602b",
        "4f20670b-630f-4f0e-8293-1fed4efd4f6a",
        "f056a57c-6f3d-473b-8229-50edd0e48d45",
        "6ddfd841-2baf-4c8f-bbda-f490cb164a0e",
        "60f68f0b-c309-4dd6-b66f-14c21fe4b1d0",
        "1caed009-6183-4146-8043-e6612de25165",
        "975383dd-682f-432e-b9ec-ba79b15af664",
        "344d89e2-a2c2-42a6-bd87-f3688485ff9c",
        "0325bec4-8d06-4885-9b42-2649630e1638",
        "db5c58ae-233b-44ea-95ad-31e0ca0ed523",
        "662d6a40-a84d-4238-9938-496704740791",
        "dcf6e456-8d89-4542-a11e-2c527130d238",
        "70bcbc27-76dd-4e8b-93c2-7468d4f9abac",
        "9a3b0366-88fc-4273-847d-7febd557c78c",
        "1d24e2bd-d200-4ce6-b1ea-37d211cc373f",
        "0e8dd555-ef57-4b4f-a58a-a38efdafb8b7"
    ]
# Empty the entire mapping list from all documents
# result = segments_collection.delete_many(
#     {"text_id": {"$in": excluded_text_ids}}
# )

# Convert UUID strings to Binary format (subType 04) to match MongoDB's storage
# binary_ids = [Binary(uuid.UUID(text_id).bytes, 4) for text_id in excluded_text_ids]

# result = text.delete_many({"_id": {"$in": binary_ids}})
# print("Deletion acknowledged: ", result.acknowledged)
# print("Number of documents deleted: ", result.deleted_count)
# if result.deleted_count > 0:
#     print(f"✓ Successfully deleted {result.deleted_count} document(s)")
# else:
#     print("✗ No documents were deleted - they may not exist or the IDs don't match")

result = toc.delete_many({"text_id": {"$in": excluded_text_ids}})