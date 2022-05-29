from pydantic import BaseModel
from app.domain.mappings_difference import MappingsDifference


class IndexDifference(BaseModel):
    """
    Represents difference between old and new index mappings:
        name="index-name",
        multi="<multi-index-or-not>",
        difference=MappingsDifference(added=[...], removed=[...], changed=[...])
    """
    name: str
    multi: bool
    difference: MappingsDifference
