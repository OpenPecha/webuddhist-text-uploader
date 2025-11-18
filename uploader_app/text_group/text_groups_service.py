from typing import Any, List
from bson import ObjectId

from uploader_app.config import VERSION_TEXT_TYPE

from uploader_app.text_group.text_group_repository import (
    get_texts,
    get_text_groups,
    post_group,
    get_critical_instances,
    post_text,
    get_related_texts,
    get_text_instances,
    get_text_related_by_work,
    get_text_metadata
)
from uploader_app.collection.collection_repository import get_collection_by_pecha_collection_id
from uploader_app.config import TextType
from uploader_app.text_group.text_group_model import TextGroupPayload
from uploader_app.text_group.text_upload_log import (
    has_been_uploaded,
    log_uploaded_text,
)
from uploader_app.collection.collection_upload_log import (
    get_parent_id_by_pecha_collection_id,
)


class TextGroupsService:
    def __init__(self):
        self.version_group_id: str | None = None
        self.commentary_group_id: str | None = None
        self.text_ids: list[str] = []


    async def upload_tests_new_service(self):

        texts = await self.get_texts_service()
        text_types = [text["type"] for text in texts]

        

        for text in texts:
            pass
            related_text_ids = []
            commentary_text_ids = []
            text_id = text["id"]
            text_related_by_work_response = await get_text_related_by_work(text_id)
            for key in text_related_by_work_response.keys():
                if text_related_by_work_response[key]["relation"] in VERSION_TEXT_TYPE:
                    expression_ids = text_related_by_work_response[key]["expression_ids"]
                    related_text_ids = expression_ids
                else:
                    commentary_ids = text_related_by_work_response[key]["expression_ids"]
                    commentary_text_ids = commentary_ids
            if text["type"] in VERSION_TEXT_TYPE:
                related_text_ids.append(text_id)
            else:
                commentary_text_ids.append(text_id)
            await self.get_text_meta_data_service(related_text_ids, "translation")
            await self.get_text_meta_data_service(commentary_text_ids, "commentary")


    async def get_text_meta_data_service(self, text_ids: List[str], type: str):
        if type == "translation":
            group_response = await post_group('text')
            group_id = group_response["id"]
            for text_id in text_ids:
                text_metadata = await get_text_metadata(text_id)
                await self.create_text_db(text_metadata, 'text', group_id)
        if type == "commentary":
            group_response = await post_group('commentary')
            group_id = group_response["id"]
            for text_id in text_ids:
                text_metadata = await get_text_metadata(text_id)
                await self.create_text_db(text_metadata, 'commentary', group_id)


    async def create_text_db(self, text_metadata: dict[str, Any], type: str, group_id: str):
        if type == "text":
            text_payload = await self._filter_text_groups(text_metadata, group_id, type="version")
            if text_payload is None:
                return
            pecha_id = text_payload.pecha_text_id

            # Skip upload if this text was already uploaded (checked via CSV log).
            if pecha_id and has_been_uploaded(pecha_id, text_payload.type):
                print(f"Skipping already uploaded version text: {pecha_id} >>> ({text_payload.title})"
                )
                return
            text_response = await post_text(text_payload)
            if pecha_id:
                log_uploaded_text(
                    pecha_text_id=pecha_id,
                    text_id=text_response["id"],
                    text_type=text_payload.type,
                    title=text_payload.title,
                    language=text_payload.language,
                    source_link=text_payload.source_link,
                )
        else:
            text_payload = await self._filter_text_groups(text_metadata, group_id, type="commentary")
            if text_payload is None:
                return
            pecha_id = text_payload.pecha_text_id
            if pecha_id and has_been_uploaded(pecha_id, text_payload.type):
                print(f"Skipping already uploaded commentary text: {pecha_id} >>> ({text_payload.title})")
                return
            text_response = await post_text(text_payload)
            if pecha_id:
                log_uploaded_text(
                    pecha_text_id=pecha_id,
                    text_id=text_response["id"],
                    text_type=text_payload.type,
                    title=text_payload.title,
                    language=text_payload.language,
                    source_link=text_payload.source_link,
                )






    def group_instances_by_type(self, instances: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        versions: list[dict[str, Any]] = []
        commentaries: list[dict[str, Any]] = []
        for instance in instances:
            if instance["relationship"] == "translation" or instance["relationship"] == "translation_source":
                versions.append(instance)
            elif instance["relationship"] == "commentary":
                commentaries.append(instance)
        return {"text": versions, "commentary": commentaries}

    async def upload_text_groups(self) -> dict[str, list[dict[str, Any]]]:
        texts = await self.get_text_groups_service()
        for text in texts:
            data = await get_text_instances(text["id"], type="critical")
            instance_id = data[0]["id"]
            get_related_texts_response = await get_related_texts(instance_id)

            grouped_text_by_type = self.group_instances_by_type(get_related_texts_response)
            # Fetch all groups for the selected text.
            # text_groups = await get_text_groups(text["id"])
            # print("text_groups >>>>>>>>>>>>>>>>>",text_groups)

            # Group them by type for downstream use.
            # Remove any group with type 'translation_source' from text_groups
            # filtered_text_groups = [
            #     group
            #     for group in text_groups["texts"]
            #     if group.get("type") != TextType.TRANSLATION_SOURCE.value
            # ]

            # Upload groups to webuddhist backend
            for key in grouped_text_by_type.keys():
                group_response = await post_group(key)
                if key == "text":
                    self.version_group_id = group_response["id"]
                elif key == "commentary":
                    self.commentary_group_id = group_response["id"]

            # Upload texts to webuddhist backend
            for text in grouped_text_by_type["text"]:
                text_payload = await self._filter_text_groups(
                    text, self.version_group_id, type="version"
                )
                

            for text in grouped_text_by_type["commentary"]:
                text_payload = await self._filter_text_groups(
                    text,
                    self.commentary_group_id,
                    type="commentary"
                )
                pecha_id = text_payload.pecha_text_id

                if pecha_id and has_been_uploaded(pecha_id, text_payload.type):
                    print(f"Skipping already uploaded commentary text: {pecha_id} ({text_payload.title})")
                    continue

                text_response = await post_text(text_payload)
        
                if pecha_id:
                    log_uploaded_text(
                        pecha_text_id=pecha_id,
                        text_id=text_response["id"],
                        text_type=text_payload.type,
                        title=text_payload.title,
                        language=text_payload.language,
                        source_link=text_payload.source_link,
                    )

        return grouped_text_by_type

    async def get_texts_service(self, type: str | None = None):
        return await get_texts(type)

    async def _filter_text_groups(
        self, text: dict[str, Any], group_id: str | None, type: str
    ) -> TextGroupPayload:
        # Fetch critical instances for this text so we can map ID and source.
        critical_instances_list = await get_critical_instances(text["id"])

        if len(critical_instances_list) > 0:
            critical_instance = critical_instances_list[0]
        else:
            return None

        raw_title = ''

        for title in text["title"].values():
            raw_title = title
            break

        # Look up the collection ID from collection_upload_log by category_id (pecha_collection_id)
        collection_id = None
        if text["category_id"]:
            id = get_parent_id_by_pecha_collection_id(text["category_id"])
        
        categories = [id] if id else []
        
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
            item_type = item["type"]

            # Only keep root and translation in versions.
            if item_type in {TextType.TRANSLATION.value, TextType.ROOT.value, TextType.TRANSLATION_SOURCE.value}:
                versions.append(item)
            elif item_type == TextType.COMMENTARY.value:
                commentaries.append(item)

        return {
            "text": versions,
            "commentary": commentaries,
        }


    async def get_text_related_by_work_service(text_id: str):
        pass