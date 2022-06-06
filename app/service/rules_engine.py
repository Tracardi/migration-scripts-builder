from pydantic import BaseModel
from app.domain.mappings_difference import MappingsDifference
from app.domain.operation import Operation
from typing import List, Optional
from app.misc.cast_table import cast_table
from app.domain.field_change import FieldChange
from app.domain.field import Field


class RulesEngine(BaseModel):
    difference: MappingsDifference

    def get_operations(self) -> List[Operation]:
        """
        Returns list of operations required to migrate data from given index.
        """
        self.difference.sort()

        ops = []
        ops.extend(self.handle_changed())
        ops.extend(self.handle_added())
        ops.extend(self.handle_removed())

        return ops

    def handle_added(self) -> List[Operation]:
        ops = []

        while self.difference.added:
            added_field = self.difference.added.pop(0)

            ops.extend(self.handle_added_field(added_field))

        return ops

    def handle_changed(self) -> List[Operation]:
        ops = []

        while self.difference.changed:
            changed_field = self.difference.changed.pop(0)

            op = self.handle_type_change(changed_field)
            if op is not None:
                ops.append(op)

        return ops

    def handle_removed(self):
        ops = []

        while self.difference.removed:
            removed_field = self.difference.removed.pop(0)

            ops.append(self.handle_removed_field(removed_field))

        return ops

    def handle_type_change(self, changed_field: FieldChange) -> Optional[Operation]:

        if changed_field.old_type == "_complex" and changed_field.new_type == "object":
            self.delete_children(changed_field.name)

        if changed_field.new_type in cast_table.get(changed_field.old_type, {}):
            if cast_table[changed_field.old_type][changed_field.new_type] == "explicit":
                return Operation(
                    type="cast",
                    source=changed_field.name,
                    destination=changed_field.name,
                    cast=changed_field.new_type
                )

            elif cast_table[changed_field.old_type][changed_field.new_type] != "implicit":
                return Operation(
                    type=cast_table[changed_field.old_type][changed_field.new_type],
                    source=changed_field.name,
                    destination=changed_field.name,
                    cast=None
                )

        elif changed_field.new_type in ("text", "string", "match_only_text", "keyword", "constant_keyword", "wildcard")\
                and changed_field.old_type in ("object", "_complex"):

            self.delete_children(changed_field.name)

    def handle_removed_field(self, removed_field: Field) -> Optional[Operation]:

        self.delete_children(removed_field.name)

        return Operation(
            type="remove",
            source=removed_field.name,
            destination=removed_field.name,
            cast=None
        )

    def handle_added_field(self, added_field: Field) -> List[Operation]:
        ops = []

        for removed_field in self.difference.removed:
            cast_type = cast_table.get(removed_field.type, {}).get(added_field.type, None)
            op_type = {
                "implicit": "rewrite",
                "explicit": "cast"
            }.get(cast_type, cast_type)

            ops.append(
                Operation(
                    type=op_type,
                    source=removed_field.name,
                    destination=added_field.name,
                    cast=added_field.type
                )
            )

        ops.append(
            Operation(
                type="add",
                source=added_field.name,
                destination=added_field.name,
                cast=added_field.type
            )
        )

        return ops

    def delete_children(self, field_name: str):
        self.difference.removed = [field for field in self.difference.removed if not field.name.startswith(field_name)]

