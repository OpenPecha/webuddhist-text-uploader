from ast import Str
import csv
from re import S
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
    post_segments,
    get_segments_id_by_annotation_id
)

from uploader_app.config import TEXT_UPLOAD_LOG_FILE
from uploader_app.segments.segment_model import ManifestationModel

LOG_PATH = Path(TEXT_UPLOAD_LOG_FILE)
MANIFESTATION_LOG_PATH = Path("manifestation_status_log.csv")
SEGMENTS_UPLOAD_LOG_PATH = Path("segments_upload_log.csv")

class SegmentService:

    async def upload_segments(self):
        text_pairs = await self.get_pecha_text_ids_from_csv()

        try:
            for pecha_text_id, text_id in text_pairs:
                # Check if segments for this text_id have already been uploaded
                if self.is_segments_already_uploaded(text_id):
                    print(f"Segments for text_id {text_id} already uploaded. Skipping...")
                    continue
                
                instance = await self.get_segments_annotation_by_pecha_text_id(pecha_text_id)
                annotation_ids = self.get_annotation_ids(instance)
                annotation_sengments = await get_segments_id_by_annotation_id(annotation_ids[0])
                segments_ids = [segment["id"] for segment in annotation_sengments["data"]]
                print(f"{pecha_text_id} annotation_ids length >>>>>>>>>>>>>>>>>",len(segments_ids))
                # Process segment_ids in batches to manage batch size
                
                # segments_contents = await self.make_batch_segments_content(segments_ids, pecha_text_id)
                segments_contents = self.parse_segments_content(annotation_sengments["data"], instance['content'])
                if self.is_segments_already_uploaded(text_id):
                    print(f"Segments for text_id {text_id} already uploaded. Skipping...")
                    continue
                await self.create_segments_payload(text_id, segments_contents)
                self.log_completed_segments_upload(text_id, len(segments_contents))
        except Exception as e:
            print("Error in upload_segments >>>>>>>>>>>>>>>>>",e)


    # async def make_batch_segments_content(self, segment_ids: List(str), pecha_text_id: str) -> List[dict[str, Any]]:
    #     batch_size = 2000  # you can adjust the batch size as needed
    #     all_segments_content = []
    #     for i in range(0, len(segment_ids), batch_size):
    #         batch_segment_ids = segment_ids[i:i+batch_size]
    #         print(f"{pecha_text_id} batch_segment_ids length >>>>>>>>>>>>>>>>>",len(batch_segment_ids))
    #         # For each batch, get segment content and accumulate
    #         batch_content = await self._get_segments_content(batch_segment_ids, pecha_text_id)
    #         all_segments_content.extend(batch_content)
    #     return all_segments_content

    def parse_segments_content(self, segments_annotation: List[dict[str, Any]], base_text: str) -> List[dict[str, Any]]:
        segments_content = []
        for segment in segments_annotation:
            segment_content = base_text[segment["span"]["start"]:segment["span"]["end"]]
            segments_content.append({
                "segment_id": segment["id"],
                "content": segment_content
            })
        return segments_content


    async def create_segments_payload(self, text_id: str, segments_content: List[dict[str, Any]]) -> List[dict[str, Any]]:
        """
        Create and post segments in batches to avoid payload size limits.
        """
        batch_size = 200  # Adjust batch size as needed
        total_segments = len(segments_content)
        
        print(f"Posting {total_segments} segments in batches of {batch_size}...")
        
        for i in range(0, total_segments, batch_size):
            batch = segments_content[i:i + batch_size]
            batch_number = (i // batch_size) + 1
            total_batches = (total_segments + batch_size - 1) // batch_size
            
            payload = {
                "text_id": text_id,
                "segments": [
                    {
                        "pecha_segment_id": segment["segment_id"],
                        "content": segment["content"],
                        "type": "source",
                    } for segment in batch
                ]
            }
            
            print(f"Posting batch {batch_number}/{total_batches} ({len(batch)} segments)...")
            await post_segments(payload)


    async def _get_segments_content(self, segment_ids: List[str], pecha_text_id: str) -> List[dict[str, Any]]:
        get_segment_content_response = await get_segment_content(segment_ids, pecha_text_id)
        return get_segment_content_response


    async def get_segments_annotation_by_pecha_text_id(
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

    async def get_pecha_text_ids_from_csv(self) -> List[tuple[str, str]]:

        if not LOG_PATH.exists():
            return []

        pecha_ids: list[tuple[str, str]] = []
        with LOG_PATH.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pecha_text_id = row["pecha_text_id"]
                text_id = row["text_id"]
                if pecha_text_id and text_id:
                    pecha_ids.append((pecha_text_id, text_id))

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
    
    def is_segments_already_uploaded(self, text_id: str) -> bool:
        """
        Check if segments for a given text_id have already been uploaded.
        Returns True if text_id exists in segments_upload_log.csv, False otherwise.
        """
        if not SEGMENTS_UPLOAD_LOG_PATH.exists():
            return False
        
        with SEGMENTS_UPLOAD_LOG_PATH.open("r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                # Skip empty rows
                if not row or len(row) == 0:
                    continue
                # Skip header row if it exists
                if row[0] == "text_id":
                    continue
                # Check if the first column (text_id) matches
                if row[0] == text_id:
                    return True
        
        return False
    
    def log_completed_segments_upload(self, text_id: str, segment_count: int) -> None:
        """
        Log text_id to CSV after all segments have been successfully uploaded.
        CSV format: text_id, segment_count, timestamp
        """
        # Ensure parent directory exists
        SEGMENTS_UPLOAD_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file exists to determine if we need to write header
        file_exists = SEGMENTS_UPLOAD_LOG_PATH.exists()
        
        # Append the text_id to the CSV
        with SEGMENTS_UPLOAD_LOG_PATH.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            # Write header if file is new
            if not file_exists:
                writer.writerow(["text_id", "segment_count", "timestamp"])
            
            # Write the text_id entry
            timestamp = datetime.now().isoformat()
            writer.writerow([text_id, segment_count, timestamp])
