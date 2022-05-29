from pydantic import BaseModel
from app.domain.mappings_difference import MappingsDifference
from app.domain.operation import Operation
from typing import List, Optional
from app.misc.cast_table import cast_table
from app.domain.field_change import FieldChange


class RulesEngine(BaseModel):
    difference: MappingsDifference

    def get_operations(self) -> List[Operation]:
        self.difference.sort()

        changed_ops = self.handle_changed()

        print(self.difference)

        return [*changed_ops]

    def handle_changed(self) -> List[Operation]:
        ops = []

        while self.difference.changed:
            changed_field = self.difference.changed.pop(0)

            op = self.handle_type_change(changed_field)
            if op is not None:
                ops.append(op)

        return ops

    def handle_type_change(self, changed_field: FieldChange) -> Optional[Operation]:

        if changed_field.new_type in cast_table.get(changed_field.old_type, {}):
            if cast_table[changed_field.old_type][changed_field.new_type] == "explicit":
                return Operation(
                    for_worker=False,
                    type="cast",
                    source=changed_field.name,
                    destination=changed_field.name,
                    cast=changed_field.new_type
                )

        elif changed_field.new_type in ("text", "string", "match_only_text", "keyword", "constant_keyword", "wildcard")\
                and changed_field.old_type in ("object", "_complex"):

            self.delete_children(changed_field.name)

            return Operation(
                for_worker=True,
                type="base64",
                source=changed_field.name,
                destination=changed_field.name,
                cast=None
            )

    def delete_children(self, field_name: str):
        self.difference.removed = [field for field in self.difference.removed if field.name.startswith(field_name)]


