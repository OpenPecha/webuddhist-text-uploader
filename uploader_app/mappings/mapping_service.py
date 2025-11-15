
from mapping_models import (
    MappingPayload,
    TextMapping,
    Mapping
)

def upload_mappings(relations):
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