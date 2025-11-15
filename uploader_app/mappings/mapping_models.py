from pydantic import BaseModel

class Mapping(BaseModel):
    parent_text_id: str
    segments: list[str]

class TextMapping(BaseModel):
    text_id: str
    segment_id: str
    mappings: list[Mapping]

class MappingPayload(BaseModel):
    text_mapping: list[TextMapping]