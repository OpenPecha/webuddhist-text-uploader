from typing import Any

import asyncio
import requests

from uploader_app.config import OpenPechaAPIURL


async def get_segments_annotation(pecha_text_id: str) -> list[dict[str, Any]]:

    instances_url = f"{OpenPechaAPIURL.DEVELOPMENT.value}/v2/instances/{pecha_text_id}"
    params = {"annotation": "true"}

    # `requests` is synchronous; run it in a thread so callers can still await.
    response = await asyncio.to_thread(
        requests.get,
        instances_url,
        params=params,
    )
    response.raise_for_status()

    # The API is expected to return JSON, usually a list of instances/segments.
    return response.json()


async def get_annotation_by_id(annotation_id: str) -> dict[str, Any]:

    url = (
        f"{OpenPechaAPIURL.DEVELOPMENT.value}/v2/annotations/{annotation_id}"
    )

    response = await asyncio.to_thread(
        requests.get,
        url,
    )
    response.raise_for_status()

    return response.json()


