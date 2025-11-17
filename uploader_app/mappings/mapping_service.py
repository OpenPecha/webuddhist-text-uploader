import requests
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

    async def trigger_mapping_service(self):
        text_pairs = await self.segment_service.get_pecha_text_ids_from_csv()
        for pecha_text_id, text_id in text_pairs:
            response = await get_manifestation_by_text_id(pecha_text_id)
            print("response >>>>>>>>>>>>>>>>>",response)
    













