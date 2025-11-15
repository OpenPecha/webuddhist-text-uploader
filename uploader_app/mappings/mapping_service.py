import requests
from uploader_app.mappings.mapping_models import (
    MappingPayload,
    TextMapping,
    Mapping
)

def generate_mapping_payload(relations):
    response = MappingPayload(
        text_mapping = []
    )
    
    # relations is a dict with "manifestation_id" and "segments" keys
    manifestation_id = relations.get("manifestation_id", "")
    segments_list = relations.get("segments", [])

    for relation in segments_list:
        mapping = TextMapping(
            text_id = manifestation_id,
            segment_id = relation["segment_id"],
            mappings = []
        )
        for segment_mapping in relation.get("mappings", []):
            segments = [
                segment["segment_id"] for segment in segment_mapping.get("segments", [])
            ]
            mapping.mappings.append(Mapping(
                parent_text_id = segment_mapping["manifestation_id"],
                segments = segments
            ))
        response.text_mapping.append(mapping)
    return response

def upload_mappings(relations):
    print("relations >>>>>>>>>>>>>>>>>",relations)
    mapping_payload = generate_mapping_payload(relations)
    
    url = "https://webuddhist-dev-backend.onrender.com/api/v1/mappings"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Convert the payload to dict for JSON serialization
    response = requests.post(
        url,
        json=mapping_payload.dict() if hasattr(mapping_payload, 'dict') else mapping_payload,
        headers=headers
    )
    
    return response