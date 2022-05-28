from pydantic import BaseModel
from typing import List
from app.domain.field import Field
from app.domain.field_change import FieldChange


class MappingsDifference(BaseModel):
    added: List[Field]
    removed: List[Field]
    changed: List[FieldChange]
