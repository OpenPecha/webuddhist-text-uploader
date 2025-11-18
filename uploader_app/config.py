from enum import Enum

import os

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNhbmR1cGxvYnphbmdAZ21haWwuY29tIiwibmFtZSI6ImxvYnphbmcgc2FtZHVwIiwiaXNzIjoiaHR0cHM6Ly9wZWNoYS12Mi5vcmciLCJhdWQiOiJodHRwczovL3BlY2hhLXYyLm9yZyIsImlhdCI6MTc2MzQ1OTk3NiwiZXhwIjoxNzgxNDU5OTc2fQ.YaTA5LPVCQhCbdVIfN7EA6a0lljJN2OV57srGZGF-HQ"

APPLICATION = "webuddhist"

COLLECTION_LANGUAGES = ["bo", "en"]

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


VERSION_TEXT_TYPE = [TextType.TRANSLATION.value, TextType.ROOT.value, TextType.TRANSLATION_SOURCE.value, TextType.NONE.value]


class OpenPechaAPIURL(Enum):
    DEVELOPMENT = "https://api-l25bgmwqoa-uc.a.run.app"

class SQSURL(Enum):
    DEVELOPMENT = "https://sqs-uploader-service.onrender.com"


class DestinationURL(Enum):
    LOCAL = "https://webuddhist-dev-backend.onrender.com/api/v1"

