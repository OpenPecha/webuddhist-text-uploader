from typing import Any, List

import asyncio
import requests

from uploader_app.config import OpenPechaAPIURL, DestinationURL, ACCESS_TOKEN, SQSURL


async def get_segments_annotation(pecha_text_id: str) -> list[dict[str, Any]]:
    """
    Fetch the list of segment annotations for a given Pecha text (instance).
    """
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


async def get_segments_by_id(annotation_id: str) -> dict[str, Any]:
    """
    Fetch a single segmentation annotation by its ID.
    """
    url = (
        f"{OpenPechaAPIURL.DEVELOPMENT.value}/v2/annotations/{annotation_id}"
    )

    response = await asyncio.to_thread(
        requests.get,
        url,
    )
    response.raise_for_status()

    return response.json()


async def get_segment_content(
    segment_id: List[str], pecha_text_id: str
) -> list[dict[str, Any]]:

    url = (
        f"{OpenPechaAPIURL.DEVELOPMENT.value}"
        f"/v2/instances/{pecha_text_id}/segment-content"
    )

    # The API accepts multiple segment IDs either as repeated query params
    # or as a single comma-separated string.
    # To maximize compatibility with the backend implementation, we
    # send them as a single comma-separated string:
    #   ?segment_id=SEG001,SEG002,SEG003
    params = {
        "segment_id": ",".join(segment_id),
    }

    response = await asyncio.to_thread(
        requests.get,
        url,
        params=params,
    )
    response.raise_for_status()

    return response.json()


async def post_segments(
    text_id: str,
    segments: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Create segments in the webuddhist backend.

    This wraps a `POST /segments` call to the destination API and sends a
    JSON body shaped as:

        {
          "text_id": "string",
          "segments": [
            {
              "content": "string",
              "type": "source",
              "mapping": []
            }
          ]
        }
    """
    url = f"{DestinationURL.LOCAL.value}/segments"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload: dict[str, Any] = {
        "text_id": text_id,
        "segments": segments,
    }

    response = await asyncio.to_thread(
        requests.post,
        url,
        headers=headers,
        json=payload,
    )

    if not response.ok:
        print(
            "POST /segments failed "
            f"(text_id={text_id}) status={response.status_code} "
            f"body={response.text}"
        )
        response.raise_for_status()

    return response.json()


async def get_manifestation_by_text_id(text_id: str) -> dict[str, Any]:
    url = f"{SQSURL.DEVELOPMENT.value}/relation/{text_id}"

    response = await asyncio.to_thread(requests.post, url)
    response.raise_for_status()
    return response.json()


