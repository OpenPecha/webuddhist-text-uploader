from enum import Enum

import os

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InNhbmR1cGxvYnphbmdAZ21haWwuY29tIiwibmFtZSI6ImxvYnphbmcgc2FuZHVwIiwiaXNzIjoiaHR0cHM6Ly9wZWNoYS5vcmciLCJhdWQiOiJodHRwczovL3BlY2hhLm9yZyIsImlhdCI6MTc2MzEyNTg3NywiZXhwIjoxNzYzMzA1ODc3fQ.x9Lo7SlYddSIqfjjIAFqGeP61EVyBxSiF-tgyItEIgs"

APPLICATION = "webuddhist"

COLLECTION_LANGUAGES = ["bo", "en"]

TEXT_TYPE = ["version", "commentary"]

class OpenPechaAPIURL(Enum):
    DEVELOPMENT = "https://api-l25bgmwqoa-uc.a.run.app"

class DestinationURL(Enum):
    LOCAL = "http://127.0.0.1:8000/api/v1"
