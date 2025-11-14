import asyncio

from uploader_app.collection.collection_service import CollectionService
from uploader_app.text_group.text_groups_service import TextGroupsService


async def pipeline():

    #collection upload
    # collection = CollectionService()
    # await collection.upload_collections()

    #text group upload
    text_group = TextGroupsService()
    await text_group.upload_text_groups()


if __name__ == "__main__":
    asyncio.run(pipeline())