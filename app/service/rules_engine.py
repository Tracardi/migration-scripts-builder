from pydantic import BaseModel
from app.domain.mappings_difference import MappingsDifference
from app.domain.operation import Operation
from typing import List
from app.misc.cast_table import cast_table


class RulesEngine(BaseModel):
    difference: MappingsDifference

    def get_operations(self) -> List[Operation]:
        self.difference.sort()

        changed_ops = self.handle_changed()

        print(self.difference)

        return [*changed_ops]

    def handle_changed(self) -> List[Operation]:
        res = []

        while self.difference.changed:
            change = self.difference.changed.pop()
            try:
                operation = self.__getattribute__(f"_cast_{change.old_type}_to_{change.new_type}")(change.name)
                if operation is not None:
                    res.append(operation)

            except AttributeError as _:
                res.append(
                    Operation(
                        source=change.name,
                        destination=change.name,
                        cast=change.new_type,
                        type="cast" if self.able_to_auto_cast(change.old_type, change.new_type) else
                        "potential_conflict"
                    )
                )

        while self.difference.added:
            added = self.difference.added.pop()
            for removed in self.difference.removed:
                res.append(
                    Operation(
                        source=removed.name,
                        destination=added.name,
                        type="cast" if self.able_to_auto_cast(removed.type, added.type) else "potential_type_conflict",
                        cast=added.type
                    )
                )
            res.append(Operation(source=f"<type {added.type}>", destination=added.name, type="user_input", cast=None))

        while self.difference.removed:
            removed = self.difference.removed.pop()
            res.append(Operation(source=removed.name, destination=removed.name, cast=None, type="remove"))

        return res

    def _cast__complex_to_object(self, change_name: str) -> None:
        self.difference.removed = [field for field in self.difference.removed if not field.name.startswith(change_name)]
        return None

    def _cast_object_to__complex(self, change_name: str) -> None:
        self.difference.added = [field for field in self.difference.added if not field.name.startswith(change_name)]
        return None

    def _cast__complex_to_string(self, change_name: str) -> Operation:
        self.difference.removed = [field for field in self.difference.removed if not field.name.startswith(change_name)]
        return Operation(
            type="base64",
            cast=None,
            source=change_name,
            destination=change_name
        )

    @property
    def _cast__complex_to_text(self):
        return self._cast__complex_to_string

    @property
    def _cast__complex_to_keyword(self):
        return self._cast__complex_to_string

    @property
    def _cast_object_to_string(self):
        return self._cast__complex_to_string

    @property
    def _cast_object_to_keyword(self):
        return self._cast__complex_to_string

    def _cast_object_to_text(self):
        return self._cast__complex_to_string

    @staticmethod
    def able_to_auto_cast(from_type: str, to_type: str) -> bool:
        return to_type in cast_table.get(from_type, [])
