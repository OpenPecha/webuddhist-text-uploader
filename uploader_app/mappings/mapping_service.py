import requests
from mapping_models import (
    MappingPayload,
    TextMapping,
    Mapping
)

def generate_mapping_payload(relations):
    response = MappingPayload(
        text_mapping = []
    )

    for relation in relations:
        mapping = TextMapping(
            text_id = relations["manifestation_id"],
            segment_id = relation["segment_id"],
            mappings = []
        )
        for segment_mapping in relation["mappings"]:
            segments = [
                segment["segment_id"] for segment in segment_mapping["segments"]
            ]
            mapping.mappings.append(Mapping(
                parent_text_id = segment_mapping["manifestation_id"],
                segments = segments
            ))
        response.text_mapping.append(mapping)
    return response

def upload_mappings(relations):
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