from enum import Enum

import os

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNhbmR1cGxvYnphbmdAZ21haWwuY29tIiwibmFtZSI6ImxvYnphbmcgc2FuZHVwIiwiaXNzIjoiaHR0cHM6Ly9wZWNoYS5vcmciLCJhdWQiOiJodHRwczovL3BlY2hhLm9yZyIsImlhdCI6MTc2MzE0NTczNSwiZXhwIjoxNzYzMzI1NzM1fQ.Svwk5iKe-26vUp9ZvTqHCDC3oFs5BEVV9UJHwwCKyTs"

APPLICATION = "webuddhist"

COLLECTION_LANGUAGES = ["bo", "en"]

# CSV file used to log which texts have already been uploaded.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEXT_UPLOAD_LOG_FILE = os.path.join(BASE_DIR, "text_upload_log.csv")

class TextType(Enum):
    COMMENTARY = "commentary"
    ROOT = "root"
    TRANSLATION = "translation"
    TRANSLATION_SOURCE = "translation_source"

class OpenPechaAPIURL(Enum):
    DEVELOPMENT = "https://api-l25bgmwqoa-uc.a.run.app"

class SQSURL(Enum):
    DEVELOPMENT = "https://sqs-uploader-service.onrender.com"


class DestinationURL(Enum):
    LOCAL = "http://127.0.0.1:8000/api/v1"

class OpenPechaAPIURL(Enum):
    DEVELOPMENT = "https://api-l25bgmwqoa-uc.a.run.app/"

class SQSURL(Enum):
    DEVELOPMENT = "https://sqs-uploader-service.onrender.com/"


class DestinationURL(Enum):
    LOCAL = "http://127.0.0.1:8000/api/v1"