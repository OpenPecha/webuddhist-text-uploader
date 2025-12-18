from enum import Enum

import os

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFkbWlucGVjaGFAZ21haWwuY29tIiwibmFtZSI6InBlY2hhIGFkbWluIiwiaXNzIjoiaHR0cHM6Ly9wZWNoYS12Mi5vcmciLCJhdWQiOiJodHRwczovL3BlY2hhLXYyLm9yZyIsImlhdCI6MTc2NDI1MTExNSwiZXhwIjoxNzgyMjUxMTE1fQ._g6IarwqG3tvw90NKKVJVeeP9aO5IxXcmINu7gnX9M0"

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
    LOCAL = "https://webuddhist-tst-backend.onrender.com/api/v1"

