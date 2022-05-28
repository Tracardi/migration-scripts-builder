from pydantic import BaseModel
from typing import Dict
from app.domain.mappings_difference import MappingsDifference
from app.domain.field_change import FieldChange
from app.domain.field import Field


class DifferenceFinder(BaseModel):
    old_mapping: Dict[str, str]
    new_mapping: Dict[str, str]

    def get_difference(self) -> MappingsDifference:
        removed = [
            Field(
                name=field_name,
                type=self.old_mapping[field_name]
            ) for field_name in set(self.old_mapping) - set(self.new_mapping)
        ]
        added = [
            Field(
                name=field_name,
                type=self.new_mapping[field_name]
            ) for field_name in set(self.new_mapping) - set(self.old_mapping)
        ]

        type_changes = [
            FieldChange(name=key, old_type=self.old_mapping[key], new_type=self.new_mapping[key]) for key in
            set(self.old_mapping).intersection(set(self.new_mapping))
            if self.old_mapping[key] != self.new_mapping[key]
        ]

        return MappingsDifference(added=added, removed=removed, changed=type_changes)
