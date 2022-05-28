from pydantic import BaseModel
from app.domain.mappings_difference import MappingsDifference


class IndexDifference(BaseModel):
    name: str
    multi: bool
    difference: MappingsDifference
