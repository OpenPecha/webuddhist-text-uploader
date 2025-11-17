from typing import Any
import asyncio
import requests
from uploader_app.config import DestinationURL, ACCESS_TOKEN

async def post_toc(toc_payload: dict[str, Any]):
    url = f"{DestinationURL.LOCAL.value}/texts/table-of-content"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    response = await asyncio.to_thread(requests.post, url, headers=headers, json=toc_payload)
    response.raise_for_status()
    return response.json()