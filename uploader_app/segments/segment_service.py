import csv
from typing import Any, List
from pathlib import Path

from uploader_app.segments.segment_respository import (
    get_instances_by_pecha_text_id,
)
from uploader_app.config import TEXT_UPLOAD_LOG_FILE

LOG_PATH = Path(TEXT_UPLOAD_LOG_FILE)

class SegmentService:

    async def upload_segments(self):
        pecha_text_ids = await self.get_pecha_text_ids_from_csv()
        
        for pecha_text_id in pecha_text_ids:
            instance = await self.get_segments_by_pecha_text_id(pecha_text_id)
            segmentation_ids = self.get_segmentation_annotation_ids(instance)
            print(
                f"pecha_text_id={pecha_text_id}"
                f"segmentation_annotation_ids={segmentation_ids}"
            )

    async def get_segments_by_pecha_text_id(
        self, pecha_text_id: str
    ) -> dict[str, Any]:
        return await get_instances_by_pecha_text_id(pecha_text_id)

    def get_segmentation_annotation_ids(self, instance: dict[str, Any]) -> list[str]:
        """
        Extract all `annotation_id` values where annotation `type` is "segmentation".

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