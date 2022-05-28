from app.domain.field import Field
from app.domain.field_change import FieldChange
from app.domain.mappings_difference import MappingsDifference


def compare_mappings(old_mapping: dict, new_mapping: dict) -> MappingsDifference:

    removed = [
        Field(name=field_name, type=old_mapping[field_name]) for field_name in set(old_mapping) - set(new_mapping)
    ]
    added = [
        Field(name=field_name, type=new_mapping[field_name]) for field_name in set(new_mapping) - set(old_mapping)
    ]

    type_changes = [
        FieldChange(name=key, old_type=old_mapping[key], new_type=new_mapping[key]) for key in
        set(old_mapping).intersection(set(new_mapping))
        if old_mapping[key] != new_mapping[key]
    ]

    return MappingsDifference(added=added, removed=removed, changed=type_changes)
