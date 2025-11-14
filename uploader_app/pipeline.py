from uploader_app.collection.collection_service import CollectionService
import asyncio

async def pipeline():

    #collection upload
    collection = CollectionService()
    await collection.upload_collections()



if __name__ == "__main__":
    asyncio.run(pipeline())