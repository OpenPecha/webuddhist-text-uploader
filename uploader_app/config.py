from enum import Enum

import os

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNhbmR1cGxvYnphbmdAZ21haWwuY29tIiwibmFtZSI6ImxvYnphbmcgc2FuZHVwIiwiaXNzIjoiaHR0cHM6Ly9wZWNoYS5vcmciLCJhdWQiOiJodHRwczovL3BlY2hhLm9yZyIsImlhdCI6MTc2MzU4MTQ5OCwiZXhwIjoxOTQzNTgxNDk4fQ.PzwqNRN0nUq3VhzT4CpcmT7ESkaRSPX30HF0lFtmKWA"

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

VERSION_TEXT_TYPE = [TextType.TRANSLATION.value, TextType.ROOT.value, TextType.TRANSLATION_SOURCE.value, TextType.NONE.value]


class OpenPechaAPIURL(Enum):
    DEVELOPMENT = "https://api-l25bgmwqoa-uc.a.run.app"

class SQSURL(Enum):
    DEVELOPMENT = "https://sqs-uploader-service.onrender.com"


class DestinationURL(Enum):
    LOCAL = "http://127.0.0.1:8000/api/v1"

