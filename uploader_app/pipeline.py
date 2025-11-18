import asyncio

from uploader_app.collection.collection_service import CollectionService
from uploader_app.text_group.text_groups_service import TextGroupsService
from uploader_app.segments.segment_service import SegmentService
from uploader_app.table_of_contents.toc_service import TocService
from uploader_app.mappings.mapping_service import MappingService

async def pipeline():

    # collection upload
    collection = CollectionService()
    await collection.upload_collections()

    print("collection uploaded successfully")

    # # text group upload
    # text_group = TextGroupsService()
    # await text_group.upload_tests_new_service()

    print("text group uploaded successfully")

    #segment upload

    # segment = SegmentService()
    # await segment.upload_segments()
    print("segment uploaded successfully")

    #toc upload
    # toc = TocService()
    # await toc.upload_toc()
    print("toc uploaded successfully")

    #trigger mapping service
    # mapping = MappingService()
    # await mapping.trigger_mapping_service()
    # print("mapping triggered successfully")


if __name__ == "__main__":
    asyncio.run(pipeline())