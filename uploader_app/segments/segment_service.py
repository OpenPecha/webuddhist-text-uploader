import csv
from typing import Any, List
from pathlib import Path

from uploader_app.segments.segment_respository import (
    get_segments_annotation,
    get_annotation_by_id
)
from uploader_app.config import TEXT_UPLOAD_LOG_FILE

LOG_PATH = Path(TEXT_UPLOAD_LOG_FILE)

class SegmentService:

    async def upload_segments(self):
        pecha_text_ids = await self.get_pecha_text_ids_from_csv()
        
        for pecha_text_id in pecha_text_ids:
            instance = await self.get_segments_annotationby_pecha_text_id(pecha_text_id)
            annotation_ids = self.get_annotation_ids(instance)
            segments = await self.get_segments_by_id_list(annotation_ids)

            segments_content = self.upload_segments_content(segments, pecha_text_id)

            
            

    def get_segments_content(self, segments: List[dict[str, Any]], pecha_text_id: str) -> List[dict[str, Any]]:
        segments_content = []
        for segment in segments:
            segments_content.append(segment["content"])
        return segments_content

    async def get_segments_annotationby_pecha_text_id(
        self, pecha_text_id: str
    ) -> dict[str, Any]:
        return await get_segments_annotation(pecha_text_id)

    def get_annotation_ids(self, instance: dict[str, Any]) -> list[str]:
        """
        The `instance` object is expected to look like:
            {
                "metadata": { ... },
                "annotations": [
                    {"annotation_id": "...", "type": "segmentation"},
                    {"annotation_id": "...", "type": "something_else"},
                    ...
                ]
            }
        """
        annotations = instance["annotations"] or []
        segmentation_ids: list[str] = []

        for annotation in annotations:
            if annotation["type"] == "segmentation":
                segmentation_ids.append(annotation["annotation_id"])

        return segmentation_ids

    async def get_pecha_text_ids_from_csv(self) -> List[str]:

        if not LOG_PATH.exists():
            return []

        pecha_ids: list[str] = []
        with LOG_PATH.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pecha_id = row["pecha_text_id"]
                if pecha_id:
                    pecha_ids.append(pecha_id)

        return pecha_ids


    async def get_segments_by_id_list(self, annotation_ids: str) -> List[dict[str, Any]]:
        annotations: List[dict[str, Any]] = []
        for annotation_id in annotation_ids:
            annotation = await get_annotation_by_id(annotation_id)
            print(">>>>>>>>>>>>>>>>>>>>>>",annotation)
            annotations.append(annotation["data"])
        return annotations