import csv
from typing import Any, List
from pathlib import Path
from datetime import datetime

from uploader_app.segments.segment_respository import (
    get_segments_annotation,
    get_segments_by_id,
    get_segment_content,
    get_manifestation_by_text_id
)
from uploader_app.config import TEXT_UPLOAD_LOG_FILE
from uploader_app.segments.segment_model import ManifestationModel

LOG_PATH = Path(TEXT_UPLOAD_LOG_FILE)
MANIFESTATION_LOG_PATH = Path("manifestation_status_log.csv")

class SegmentService:

    async def upload_segments(self):
        pecha_text_ids = await self.get_pecha_text_ids_from_csv()
        manifestation_data = []  # Store manifestation status and text id for each text
        
        for pecha_text_id in pecha_text_ids:
            manifestation_response = await get_manifestation_by_text_id(pecha_text_id)
            manifestation_model = ManifestationModel(**manifestation_response)
            # Store manifestation status and text id
            manifestation_data.append({
                "text_id": pecha_text_id,
                "status": manifestation_model.status,
                "job_id": manifestation_model.job_id,
                "message": manifestation_model.message
            })
        

            # instance = await self.get_segments_annotationby_pecha_text_id(pecha_text_id)
            # annotation_ids = self.get_annotation_ids(instance)
            # segments = await self.get_segments_by_id_list(annotation_ids[0])
            # segments_content = await self._get_segments_content(segments["data"], pecha_text_id)
            # segment_model = SegmentModel(text_id=pecha_text_id, segments=segments_content)
        
            


            
            

    async def _get_segments_content(self, segments: List[dict[str, Any]], pecha_text_id: str) -> List[dict[str, Any]]:
        segments_content_with_mapping = []
        segments_content = []
        segment_ids = [segment["id"] for segment in segments]
        get_segment_content_response = await get_segment_content(segment_ids, pecha_text_id)
        return get_segment_content_response
        

        # segments_content = await get_segment_content(segment_ids, pecha_text_id)
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
        
        segments = await get_segments_by_id(annotation_ids)
        return segments
    
    def save_manifestation_data_to_csv(self, manifestation_data: List[dict[str, Any]], file_path: Path = MANIFESTATION_LOG_PATH) -> None:
      
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Define CSV headers
        headers = ["text_id", "status", "job_id", "message", "timestamp"]
        
        # Check if file exists to determine if we need to write headers
        file_exists = file_path.exists()
        
        # Write to CSV
        with file_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            
            # Write header if file is new
            if not file_exists:
                writer.writeheader()
            
            # Write each manifestation data entry
            timestamp = datetime.now().isoformat()
            for data in manifestation_data:
                writer.writerow({
                    "text_id": data.get("text_id", ""),
                    "status": data.get("status", ""),
                    "job_id": data.get("job_id", ""),
                    "message": data.get("message", ""),
                    "timestamp": timestamp
                })
            
  