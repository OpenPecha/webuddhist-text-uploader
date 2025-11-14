from enum import Enum

import os

ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")

APPLICATION = "webuddhist"

COLLECTION_LANGUAGES = ["bo", "en"]

TEXT_TYPE = ["version", "commentary"]

class OpenPechaAPIURL(Enum):
    DEVELOPMENT = "https://api-l25bgmwqoa-uc.a.run.app"

class DestinationURL(Enum):
    LOCAL = "http://127.0.0.1:8000/api/v1"
