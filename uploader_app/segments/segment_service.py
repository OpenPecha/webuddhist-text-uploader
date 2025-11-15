import csv
import time
from typing import Any, List
from pathlib import Path
from datetime import datetime
import requests
from uploader_app.config import SQSURL


from uploader_app.segments.segment_respository import (
    get_segments_annotation,
    get_segments_by_id,
    get_segment_content,
    get_manifestation_by_text_id,
    get_relation_text_id,
    post_segments
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
            try:    
                # Check if the text_id is already in the CSV
                manifestation_response = await get_manifestation_by_text_id(pecha_text_id)
                manifestation_model = ManifestationModel(**manifestation_response)
                # Store manifestation status and text id
                manifestation_data.append({
                    "text_id": pecha_text_id,
                    "status": manifestation_model.status,
                    "job_id": manifestation_model.job_id,
                    "message": manifestation_model.message
                })
            except requests.exceptions.HTTPError as e:
                print(f"HTTP error for text_id={pecha_text_id}: {e}")
                continue
            except Exception as e:
                print(f"Unexpected error for text_id={pecha_text_id}: {e}")
                continue
        self.save_manifestation_data_to_csv(manifestation_data)
        for pecha_text_id in pecha_text_ids:
            relation_text = await self.get_relation_text_id_service(pecha_text_id)
            segments_ids = [segment["segment_id"] for segment in relation_text["segments"]]
            print(">>>>>>>>>>>>>>>>>>>>>>",segments_ids, pecha_text_id)
            segments_content = await self._get_segments_content(segments_ids, pecha_text_id)
            create_segments_payload = self.create_segments_payload(segments_content)
            break


    async def create_segments_payload(self, text_id: str, segments_content: List[dict[str, Any]]) -> List[dict[str, Any]]:
        payload = {
            "text_id": text_id,
            "segments": []
        }
        for segment in segments_content:
            payload["segments"].append({
                "content": segment["content"],
                "type": "source",
            })
        post_segments_response = await post_segments(payload)
        return payload
    
    def generate_weBuddhist_mapping_payload(self, mapping):
        pass

    def completed_job(self, job_id: str) -> bool:
        url = f"{SQSURL.DEVELOPMENT.value}/relation/{job_id}"
        response = requests.get(url)
        return response.json()
    async def get_relation_text_id_service(self, text_id : str) -> str:
        return await get_relation_text_id(text_id)

    def read_manifestation_log(self) -> List[dict[str, Any]]:
        """
        Read manifestation data from CSV file WITHOUT headers.
        CSV format: text_id, status, job_id, message, timestamp
        """
        if not MANIFESTATION_LOG_PATH.exists():
            return []
        
        manifestation_records = []
        with MANIFESTATION_LOG_PATH.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                # Skip empty rows
                if not row or len(row) == 0 or not row[0].strip():
                    continue
                
                # CSV columns: text_id, status, job_id, message, timestamp
                manifestation_records.append({
                    "text_id": row[0] if len(row) > 0 else "",
                    "status": row[1] if len(row) > 1 else "",
                    "job_id": row[2] if len(row) > 2 else "",
                    "message": row[3] if len(row) > 3 else "",
                    "timestamp": row[4] if len(row) > 4 else ""
                })
        
        return manifestation_records
    
    async def _get_segments_content(self, segment_ids: List[str], pecha_text_id: str) -> List[dict[str, Any]]:
        segments_content = []
        get_segment_content_response = await get_segment_content(segment_ids, pecha_text_id)
        return get_segment_content_response
        

        # segments_content = await get_segment_content(segment_ids, pecha_text_id)
        return segments_content


    async def get_segments_annotationby_pecha_text_id(
        self, pecha_text_id: str
    ) -> dict[str, Any]:
        return await get_segments_annotation(pecha_text_id)

    def get_annotation_ids(self, instance: dict[str, Any]) -> list[str]:
       
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
        """
        Save manifestation data to CSV file WITHOUT headers.
        CSV format: text_id, status, job_id, message, timestamp
        """
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to CSV without headers
        with file_path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            # Write each manifestation data entry as a row
            timestamp = datetime.now().isoformat()
            for data in manifestation_data:
                writer.writerow([
                    data.get("text_id", ""),
                    data.get("status", ""),
                    data.get("job_id", ""),
                    data.get("message", ""),
                    timestamp
                ])
            
  