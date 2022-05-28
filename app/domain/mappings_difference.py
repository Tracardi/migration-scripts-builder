from pydantic import BaseModel
from typing import List
from app.domain.field import Field
from app.domain.field_change import FieldChange


class MappingsDifference(BaseModel):
    added: List[Field]
    removed: List[Field]
    changed: List[FieldChange]

    def sort(self):
        self.added = sorted(self.added, key=lambda field: field.name.count("."))
        self.removed = sorted(self.removed, key=lambda field: field.name.count("."))
        self.changed = sorted(self.changed, key=lambda key_change: key_change.name.count("."))
