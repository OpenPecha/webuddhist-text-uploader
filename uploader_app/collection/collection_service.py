from typing import Any
from uploader_app.collection.collection_repository import get_collections
from uploader_app.config import OpenPechaAPIURL, COLLECTION_LANGUAGES

class CollectionService:

    def upload_collections(self):
        """
        Entry point for building the collection payload tree.

        This will:
        - Fetch top‑level collections (no `parent_id`)
        - Recursively fetch and attach child collections for any collection that
          reports `has_sub_child` / `has_child` from the API.
        """

        multilingual_payloads = self.build_recursive_multilingual_payloads()
        flattened_payloads = self.flatten_recursive_multilingual_payloads(multilingual_payloads)
        print(flattened_payloads)


    def get_collections_service(self, parent_id: str | None = None):
        return get_collections(
            OpenPechaAPIURL.DEVELOPMENT.value, COLLECTION_LANGUAGES,
            parent_id=parent_id
        )

    def build_recursive_multilingual_payloads(
        self, parent_id: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Recursively build multilingual payloads starting from the given parent.

        For the root call (`parent_id=None`), this returns a list of top‑level
        collections. For each collection that has children, a `children` key is
        added containing the same multilingual payload structure for its
        sub‑collections.
        """
        # Fetch collections for this level
        collections_by_language = self.get_collections_service(parent_id=parent_id)

        # Build the multilingual payload for the current level
        multilingual_payloads = self.build_multilingual_payload(
            collections_by_language
        )

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

    def flatten_recursive_multilingual_payloads(
        self, recursive_payloads: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """
        Flatten a tree of multilingual payloads (with `children`) into a single
        list.

        Each node in the returned list is a shallow copy of the original payload
        without the `children` key, so that it can easily be used in contexts
        that expect a flat collection list (e.g. bulk upload).
        """
        flat: list[dict[str, Any]] = []

        def _flatten(nodes: list[dict[str, Any]]) -> None:
            for node in nodes:
                children = node.get("children") or []

                # Copy everything except `children` for the flat representation
                flat_node = {key: value for key, value in node.items() if key != "children"}
                flat.append(flat_node)

                if children:
                    _flatten(children)

        _flatten(recursive_payloads)
        return flat

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
                raw_id = collection.get("id")

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
                        "pecha_collection_id": raw_id,
                        "slug": collection.get("slug"),
                        "titles": {},
                        # Always initialise description keys for all configured languages.
                        "descriptions": {lang: "" for lang in COLLECTION_LANGUAGES},
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
