from typing import Any

import asyncio
import requests

from uploader_app.config import OpenPechaAPIURL, DestinationURL, ACCESS_TOKEN
from uploader_app.text_group.text_group_model import TextGroupPayload


async def get_texts(type: str | None = None) -> list[dict[str, Any]]:
    texts_url = f"{OpenPechaAPIURL.DEVELOPMENT.value}/v2/texts"

    # `requests` is synchronous; run it in a thread so callers can still await.
    params = {
        "type": type,
    }
    response = await asyncio.to_thread(requests.get, texts_url, params=params)
    response.raise_for_status()

    return response.json()


async def get_related_texts(text_id: str) -> list[dict[str, Any]]:
    related_texts_url = f"{OpenPechaAPIURL.DEVELOPMENT.value}/v2/instances/{text_id}/related"
    response = await asyncio.to_thread(requests.get, related_texts_url)
    response.raise_for_status()
    return response.json()

async def get_text_instances(text_id: str, type: str) -> list[dict[str, Any]]:
    instances_url = f"{OpenPechaAPIURL.DEVELOPMENT.value}/v2/texts/{text_id}/instances"
    params = {
        "type": type,
    }
    response = await asyncio.to_thread(requests.get, instances_url, params=params)
    response.raise_for_status()
    return response.json()

async def get_text_groups(text_id: str) -> list[dict[str, Any]]:
    groups_url = f"{OpenPechaAPIURL.DEVELOPMENT.value}/v2/texts/{text_id}/group"

    response = await asyncio.to_thread(requests.get, groups_url)
    response.raise_for_status()

    return response.json()


async def post_group(type: str) -> dict[str, Any]:
    """
    Create a text group in the destination (webuddhist) backend.
    """
    url = f"{DestinationURL.LOCAL.value}/groups"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "type": type,
    }

    response = await asyncio.to_thread(
        requests.post,
        url,
        headers=headers,
        json=payload,
    )

    if not response.ok:
        # Print full details so we can see why the backend returned 4xx/5xx.
        print(
            f"POST /groups failed "
            f"(status={response.status_code}) "
            f"body={response.text}"
        )
        response.raise_for_status()

    return response.json()

async def get_critical_instances(text_id: str) -> list[dict[str, Any]]:
    instances_url = f"{OpenPechaAPIURL.DEVELOPMENT.value}/v2/texts/{text_id}/instances"
    params = {"instance_type": "critical"}

    response = await asyncio.to_thread(
        requests.get,
        instances_url,
        params=params,
    )
    response.raise_for_status()

    return response.json()


async def post_text(text_payload: TextGroupPayload) -> dict[str, Any]:

    url = f"{DestinationURL.LOCAL.value}/texts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = text_payload.model_dump()

    response = await asyncio.to_thread(
        requests.post,
        url,
        headers=headers,
        json=payload,
    )

    if not response.ok:
        print(
            f"POST /texts failed "
            f"(status={response.status_code}) "
            f"body={response.text}"
        )
        response.raise_for_status()

    return response.json()
