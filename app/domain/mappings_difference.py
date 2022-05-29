from pydantic import BaseModel
from typing import List
from app.domain.field import Field
from app.domain.field_change import FieldChange


class MappingsDifference(BaseModel):
    """
    Represents difference between two mappings:
        added = list of fields present in new mapping, but not in old one,
        removed = list of fields present in old mapping, but not in new one,
        changed = list of fields that are in both mappings, but with different type
    """
    added: List[Field]
    removed: List[Field]
    changed: List[FieldChange]

    def sort(self):
        """
        Sorts itself such that most nested fields are the last in every property
        """
        self.added = sorted(self.added, key=lambda field: field.name.count("."))
        self.removed = sorted(self.removed, key=lambda field: field.name.count("."))
        self.changed = sorted(self.changed, key=lambda key_change: key_change.name.count("."))
