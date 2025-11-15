from typing import Any

from uploader_app.text_group.text_group_repository import (
    get_texts,
    get_text_groups,
    post_group,
    get_critical_instances,
    post_text,
)
from uploader_app.collection.collection_repository import get_collection_by_pecha_collection_id
from uploader_app.config import TextType
from uploader_app.text_group.text_group_model import TextGroupPayload


class TextGroupsService:
    def __init__(self):
        self.version_group_id: str | None = None
        self.commentary_group_id: str | None = None
        self.text_ids: list[str] = []

    async def upload_text_groups(self) -> dict[str, list[dict[str, Any]]]:
        texts = await self.get_text_groups_service()
        for text in texts:

            # Fetch all groups for the selected text.
            text_groups = await get_text_groups(text["id"])

            # Group them by type for downstream use.
            # Remove any group with type 'translation_source' from text_groups
            filtered_text_groups = [
                group
                for group in text_groups["texts"]
                if group.get("type") != TextType.TRANSLATION_SOURCE.value
            ]
            grouped_text_by_type = self.group_texts_by_type({"texts": filtered_text_groups})

            # Upload groups to webuddhist backend
            for key in grouped_text_by_type.keys():
                group_response = await post_group(key)
                if key == "text":
                    self.version_group_id = group_response["id"]
                elif key == "commentary":
                    self.commentary_group_id = group_response["id"]

            # Upload texts to webuddhist backend
            for text in grouped_text_by_type["text"]:
                print("text version>>>>>>>>>>>>>>>>>>>>>>>>>",text)

                text_payload = await self._filter_text_groups(
                    text, self.version_group_id, type="version"
                )
                text_response = await post_text(text_payload)
                self.text_ids.append(text_response["id"])

            for text in grouped_text_by_type["commentary"]:
                text_payload = await self._filter_text_groups(
                    text,
                    self.commentary_group_id,
                    type="commentary"
                )
                text_response = await post_text(text_payload)
                self.text_ids.append(text_response["id"])
                print("text response commentary>>>>>>>>>>>>>>>>>>>>>>>>>",text_response)

        return grouped_text_by_type

    async def get_text_groups_service(self, type: str | None = None):
        return await get_texts(type)

    async def _filter_text_groups(
        self, text: dict[str, Any], group_id: str | None, type: str
    ) -> TextGroupPayload:
        # Fetch critical instances for this text so we can map ID and source.
        critical_instances = await get_critical_instances(text["id"])

        critical_instance = critical_instances[0]

        raw_title = ''

        for title in text["title"].values():
            raw_title = title
            break

        categories = [text["category_id"]] if text["category_id"] else []
        return TextGroupPayload(
            pecha_text_id=critical_instance["id"],
            title=raw_title,
            language=text.get("language"),
            isPublished=text.get("isPublished", False),
            group_id=group_id,
            published_by="",
            type=type,
            categories=categories,  
            views=text.get("views", 0),
            source_link=critical_instance["source"],
            ranking=text.get("ranking"),
            license=text.get("license"),
        )

    def _extract_collection_id(self, data: Any) -> str | None:
        """
        Normalise a collection API response into a single string ID.

        The `/collections` endpoint may return:
          - a single object with `id`, `_id`, or `collection_id`
          - a list of such objects
          - a wrapper object like `{"collections": [ ... ]}`
        This helper tries to handle all of those cases and returns the first
        usable ID as a string, or `None` if none can be found.
        """
        # If we were given a list, look at the first element.
        if isinstance(data, list):
            if not data:
                return None
            data = data[0]

        # If the response is wrapped, unwrap the first collection item.
        if isinstance(data, dict) and "collections" in data:
            collections = data.get("collections") or []
            if isinstance(collections, list) and collections:
                return self._extract_collection_id(collections[0])

        if not isinstance(data, dict):
            return None

        raw_id = data.get("id") or data.get("_id") or data.get("collection_id")

        if isinstance(raw_id, dict) and "$oid" in raw_id:
            return str(raw_id["$oid"])
        if raw_id is not None:
            return str(raw_id)

        return None

    def group_texts_by_type(
        self, groups_payload: dict[str, Any]
    ) -> dict[str, list[dict[str, Any]]]:
        texts = groups_payload.get("texts", [])

        versions: list[dict[str, Any]] = []
        commentaries: list[dict[str, Any]] = []

        for item in texts:
            item_type = item.get("type")

            # Only keep root and translation in versions.
            if item_type in {TextType.TRANSLATION.value, TextType.ROOT.value}:
                versions.append(item)
            elif item_type == TextType.COMMENTARY.value:
                commentaries.append(item)

        return {
            "text": versions,
            "commentary": commentaries,
        }
