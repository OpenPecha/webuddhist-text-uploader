from typing import Any
from uploader_app.collection.collection_repository import get_collections
from uploader_app.config import OpenPechaAPIURL, COLLECTION_LANGUAGES

class CollectionService:

    def upload_collections(self):
        # Step 1: fetch top most collections from the remote API
        collections_by_language = self.get_collections_service()

        # Step 2: build the multilingual payload, combining entries that share the
        # same `_id` into a single document with language-keyed `titles` and
        # `descriptions`.
        multilingual_payload = self.build_multilingual_payload(collections_by_language)
        print(multilingual_payload)


    def get_collections_service(self, parent_id: str | None = None):
        return get_collections(
            OpenPechaAPIURL.DEVELOPMENT.value, COLLECTION_LANGUAGES,
            parent_id=parent_id
        )

    def build_multilingual_payload(
        self, collections_by_language: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Create a payload that combines collections with the same `_id` across
        multiple languages into a single multilingual document.

        Input (from `get_collections`):

        [
            {
                "language": "en",
                "collections": [
                    {
                        "_id": {"$oid": "..."},
                        "slug": "Liturgy",
                        "title": "Liturgy",
                        "description": "Prayers and rituals",
                        "parent_id": null,
                        "has_sub_child": true
                    },
                    ...
                ],
            },
            {
                "language": "bo",
                "collections": [
                    {
                        "_id": {"$oid": "..."},
                        "slug": "Liturgy",
                        "title": "ཁ་འདོན།",
                        "description": "ཆོ་ག་དང་འདོན་ཆ།",
                        "parent_id": null,
                        "has_sub_child": true
                    },
                    ...
                ],
            },
        ]

        Output:

        [
            {
                "_id": {"$oid": "..."},
                "slug": "Liturgy",
                "titles": {
                    "en": "Liturgy",
                    "bo": "ཁ་འདོན།",
                },
                "descriptions": {
                    "en": "Prayers and rituals",
                    "bo": "ཆོ་ག་དང་འདོན་ཆ།",
                },
                "parent_id": null,
                "has_sub_child": true,
            },
            ...
        ]
        """

        combined: dict[str, dict[str, Any]] = {}

        for entry in collections_by_language:
            language = entry["language"]
            for collection in entry["collections"]:
                # --- ID handling -------------------------------------------------
                # Upstream API sometimes returns `_id` (Mongo-style) and in other
                # cases returns a plain `id` field (as in your example).
                raw_id = collection.get("_id")
                if raw_id is None:
                    raw_id = collection.get("id")

                # If we *still* don't have an ID, skip this record – we can't
                # reliably merge it across languages.
                if raw_id is None:
                    continue

                # Normalise ID to a string key, while preserving the original value
                if isinstance(raw_id, dict) and "$oid" in raw_id:
                    id_key = str(raw_id["$oid"])
                else:
                    id_key = str(raw_id)

                # --- Parent / child flags ---------------------------------------
                # Support both the old (`parent_id`, `has_sub_child`) and the new
                # (`parent`, `has_child`) field names.
                parent_value = collection.get("parent_id", collection.get("parent"))
                has_sub_child_value = collection.get(
                    "has_sub_child", collection.get("has_child")
                )

                if id_key not in combined:
                    combined[id_key] = {
                        "collection_id": raw_id,
                        "slug": collection.get("slug"),
                        "titles": {},
                        # Always initialise description keys for all configured languages.
                        "description": {lang: "" for lang in COLLECTION_LANGUAGES},
                        "parent_id": parent_value,
                        "has_sub_child": has_sub_child_value,
                    }

                # --- Titles / descriptions --------------------------------------
                # Prefer simple `title` / `description` fields from the API. If the
                # API already returns language-keyed maps (`titles`, `descriptions`),
                # fall back to those.
                title_value = collection.get("title")
                if title_value is None:
                    title_value = collection.get("titles", {}).get(language)

                description_value = collection.get("description")
                if description_value is None:
                    description_value = collection.get("descriptions", {}).get(
                        language
                    )

                if title_value is not None:
                    combined[id_key]["titles"][language] = title_value

                    # If we don't already have a slug and this is the English entry,
                    # use the English title as the slug as a sensible default.
                    if language == "en" and not combined[id_key].get("slug"):
                        combined[id_key]["slug"] = title_value

                if description_value is not None:
                    combined[id_key]["description"][language] = description_value

        # Return a simple list for easier downstream processing
        return list(combined.values())
