import requests
import csv
import os
from uploader_app.mappings.mapping_models import (
    MappingPayload,
    TextMapping,
    Mapping
)
from uploader_app.segments.segment_respository import get_manifestation_by_text_id

class MappingService:
    def __init__(self):
        # Import here to avoid circular import
        from uploader_app.segments.segment_service import SegmentService
        self.segment_service = SegmentService()
        self.status_log_file = "manifestation_status_log.csv"

    def _load_processed_instance_ids(self):
        """Load already processed instance IDs from the CSV file"""
        if not os.path.exists(self.status_log_file):
            return set()
        
        processed_ids = set()
        with open(self.status_log_file, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:  # Skip empty rows
                    processed_ids.add(row[0])
        return processed_ids

    def _save_instance_id(self, instance_id):
        """Append instance_id to the CSV file"""
        with open(self.status_log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([instance_id])

    async def trigger_mapping_service(self):
        # Load already processed instance IDs
        processed_ids = self._load_processed_instance_ids()
        
        text_pairs = await self.segment_service.get_pecha_text_ids_from_csv()
        for instance_id, text_id in text_pairs:
            # Skip if already processed
            if instance_id in processed_ids:
                print(f"Skipping instance_id {instance_id} - already processed")
                continue
            
            response = await get_manifestation_by_text_id(instance_id)
            print("response >>>>>>>>>>>>>>>>>",response)
            
            # Save instance_id to CSV after processing
            self._save_instance_id(instance_id)
            processed_ids.add(instance_id)  # Add to set to avoid reprocessing in same run
    













