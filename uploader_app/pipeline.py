import asyncio

from uploader_app.collection.collection_service import CollectionService
from uploader_app.text_group.text_groups_service import TextGroupsService


async def pipeline():

    #collection upload
    collection = CollectionService()
    await collection.upload_collections()

    print("collection uploaded successfully")

    #text group upload
    text_group = TextGroupsService()
    await text_group.upload_text_groups()

    print("text group uploaded successfully")


if __name__ == "__main__":
    asyncio.run(pipeline())