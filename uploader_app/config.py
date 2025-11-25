from enum import Enum

import os

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWlucGVjaGFAZ21haWwuY29tIiwibmFtZSI6ImFkbWluIHBlY2hhIiwiaXNzIjoiaHR0cHM6Ly9wZWNoYS12Mi5vcmciLCJhdWQiOiJodHRwczovL3BlY2hhLXYyLm9yZyIsImlhdCI6MTc2Mzk2OTg1MiwiZXhwIjoxNzY1NzY5ODUyfQ.V0H88xbGk0bEwW_lNEIVV3bOzka4whn60TY7WxMfKGc"

APPLICATION = "webuddhist"

COLLECTION_LANGUAGES = ["bo", "en", "zh"]

# CSV file used to log which texts have already been uploaded.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEXT_UPLOAD_LOG_FILE = os.path.join(BASE_DIR, "text_upload_log.csv")
COLLECTION_UPLOAD_LOG_FILE = os.path.join(BASE_DIR, "collection_upload_log.csv")

class TextType(Enum):
    COMMENTARY = "commentary"
    ROOT = "root"
    TRANSLATION = "translation"
    TRANSLATION_SOURCE = "translation_source"
    NONE = None

VERSION_TEXT_TYPE = [TextType.TRANSLATION.value, TextType.ROOT.value, TextType.TRANSLATION_SOURCE.value, TextType.NONE.value, TextType.ROOT.value]


class OpenPechaAPIURL(Enum):
    DEVELOPMENT = "https://api-aq25662yyq-uc.a.run.app"

class SQSURL(Enum):
    DEVELOPMENT = "https://sqs-uploader-service.onrender.com"


class DestinationURL(Enum):
    LOCAL = "https://api.webuddhist.com/api/v1"

MAX_PROCESSING_CONCURRENCY = 4

