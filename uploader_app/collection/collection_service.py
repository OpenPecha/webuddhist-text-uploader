from typing import Any
from uploader_app.collection.collection_repository import get_collections
from uploader_app.config import OpenPechaAPIURL, COLLECTION_LANGUAGES


class CollectionService:

    def upload_collections(self):

        self.build_recursive_multilingual_payloads()


    def get_collections_service(self, parent_id: str | None = None):
        return get_collections(
            OpenPechaAPIURL.DEVELOPMENT.value, COLLECTION_LANGUAGES,
            parent_id=parent_id
        )

    def build_recursive_multilingual_payloads(
        self, parent_id: str | None = None
    ) -> list[dict[str, Any]]:
    
        # Fetch collections for this level from the remote API.
        collections_by_language = self.get_collections_service(parent_id=parent_id)

        # Build the multilingual payload for the current level.
        multilingual_payloads = self.build_multilingual_payload(
            collections_by_language
        )
        print(multilingual_payloads, "\n\n\n")
        # For each payload that has children, fetch and attach them recursively.
        for payload in multilingual_payloads:
            has_sub_child = payload.get("has_sub_child") or payload.get("has_child")

            if not has_sub_child:
                payload["children"] = []
                continue

            # Normalise the ID that should be used as `parent_id` for the next level
            raw_id = payload.get("pecha_collection_id")
            next_parent_id: str | None
            if isinstance(raw_id, dict) and "$oid" in raw_id:
                next_parent_id = str(raw_id["$oid"])
            elif raw_id is not None:
                next_parent_id = str(raw_id)
            else:
                next_parent_id = None

            # If we don't have a usable parent id, we can't descend further.
            if next_parent_id is None:
                payload["children"] = []
                continue

            payload["children"] = self.build_recursive_multilingual_payloads(
                parent_id=next_parent_id
            )

        return multilingual_payloads


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

        Output (per-language list):

        [
            {
                "language": "en",
                "pecha_collection_id": {"$oid": "..."},
                "slug": "Liturgy",
                "titles": {"en": "Liturgy"},
                "descriptions": {"en": "Prayers and rituals"},
                "parent_id": null,
                "has_sub_child": true,
            },
            {
                "language": "bo",
                "pecha_collection_id": {"$oid": "..."},
                "slug": "Liturgy",
                "titles": {"bo": "ཁ་འདོན།"},
                "descriptions": {"bo": "ཆོ་ག་དང་འདོན་ཆ།"},
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
                raw_id = collection.get("id")

                # Normalise ID to a string key, while preserving the original value
                if isinstance(raw_id, dict) and "$oid" in raw_id:
                    id_key = str(raw_id["$oid"])
                else:
                    id_key = str(raw_id)

                # --- Parent / child flags ---------------------------------------
                parent_value = collection.get("parent_id", collection.get("parent"))
                has_sub_child_value = collection.get(
                    "has_sub_child", collection.get("has_child")
                )

                if id_key not in combined:
                    combined[id_key] = {
                        "pecha_collection_id": raw_id,
                        "slug": collection.get("slug"),
                        "titles": {},
                        # Always initialise description keys for all configured languages.
                        "descriptions": {lang: "" for lang in COLLECTION_LANGUAGES},
                        "parent_id": parent_value,
                        "has_sub_child": has_sub_child_value,
                    }

                # --- Titles / descriptions --------------------------------------
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

                    # Always use the English title as the slug so that all
                    # per-language payloads sharing this collection ID have a
                    # consistent, human-readable slug.
                    if language == "en":
                        combined[id_key]["slug"] = title_value

                if description_value is not None:
                    # Ensure the descriptions dictionary exists (it should from
                    # initialisation, but we guard just in case).
                    if "descriptions" not in combined[id_key]:
                        combined[id_key]["descriptions"] = {}
                    combined[id_key]["descriptions"][language] = description_value

        # First, collapse all languages into combined multilingual nodes, then
        # expand back out into the desired per-language payload format.
        combined_list = list(combined.values())
        return self.expand_to_per_language_payloads(combined_list)

    # ------------------------------------------------------------------
    # Helpers for per-language expansion
    # ------------------------------------------------------------------

    def expand_to_per_language_payloads(
        self, multilingual_collections: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Convert combined multilingual collection entries into a list of
        per-language payloads with this shape:

            {
                "pecha_collection_Id": "<id>",
                "parent": "<parent_id>" | null,
                "slug": "<english-title>",
                "language": "<lang>",
                "title": { "<lang>": "<title>" },
                "descriptions": { "<lang>": "<description>" } | {}
            }

        Each language present in `titles` becomes its own payload object.
        """
        per_language: list[dict[str, Any]] = []

        for collection in multilingual_collections:
            per_language.extend(
                self._split_collection_by_language(collection)
            )

        return per_language

    def _split_collection_by_language(
        self, collection: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """
        Take a single multilingual collection node and split it into
        multiple per-language payloads matching the desired format.
        """
        results: list[dict[str, Any]] = []
        titles: dict[str, Any] = collection.get("titles", {})
        descriptions: dict[str, Any] = collection.get("descriptions", {}) or {}

        # Use the English title as the slug for all languages that share
        # this pecha_collection_id. If no English title is present, fall
        # back to the collection's existing slug.
        english_title = titles.get("en")
        slug_value = english_title or collection.get("slug")

        for lang, title_value in titles.items():
            payload: dict[str, Any] = {
                # Match the desired external format for per-language payloads.
                "pecha_collection_id": collection.get("pecha_collection_id"),
                "parent_id": collection.get("parent_id"),
                "slug": slug_value,
                "language": lang,
                "titles": {lang: title_value},
                "descriptions": {},
            }

            # Preserve child information if present on the combined node.
            if "has_sub_child" in collection:
                payload["has_sub_child"] = collection["has_sub_child"]
            elif "has_child" in collection:
                payload["has_sub_child"] = collection["has_child"]

            # Only set descriptions for this language if one is available.
            desc_value = descriptions.get(lang)
            if desc_value is not None:
                payload["descriptions"][lang] = desc_value

            results.append(payload)

        return results

