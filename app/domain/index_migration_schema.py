from pydantic import BaseModel
from app.domain.index_migration import IndexMigration, CopyIndex
from app.service.script_builder import ScriptBuilder
from typing import List
from app.domain.operation import Operation
from app.domain.field_change import FieldChange
from hashlib import sha1


class IndexMigrationSchema(BaseModel):
    """
    That's an object representing index migration in terms of Operation class objects. ScriptBuilder is used to
    translate this object into IndexMigration, which is a final result:
        from_index: name of the index to be migrated
        to_index: name of the target index
        multi: indicates if the index is multi index or not
        operations: list of operations that need to be performed in order to migrate data
        custom_worker_required: informational field for the dev to know if generic reindex worker can handle this
            migration. If not, then new custom worker is required
    """
    to_index: str
    from_index: str
    multi: bool
    operations: List[Operation]
    custom_worker_required: List[FieldChange]

    def build_migration(self) -> IndexMigration:

        return IndexMigration(
            id=sha1(f"{self.to_index}{self.from_index}".encode('utf-8')).hexdigest(),
            copy_index=CopyIndex(
                from_index=self.from_index,
                to_index=self.to_index,
                multi=self.multi,
                script=ScriptBuilder(operations=self.operations).build(),
            ),
            worker="reindex",
            conflicts=self.custom_worker_required if self.custom_worker_required else None
        )
