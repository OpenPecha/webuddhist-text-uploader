from uploader_app.collection.collection_service import CollectionService


def pipeline():

    #collection upload
    collection = CollectionService()
    collection.upload_collections()



if __name__ == "__main__":
    pipeline()