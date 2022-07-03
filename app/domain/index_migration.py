from pydantic import BaseModel
from typing import Optional, List
from app.domain.field_change import FieldChange


class CopyIndex(BaseModel):
    """
    from_index: name of the index to be migrated
    to_index: name of the target index
    multi: indicates if the index to be migrated is multi or not
    script: painless script to be used to reindex docs
    """
    from_index: str
    to_index: str
    multi: bool
    script: Optional[str] = None


class IndexMigration(BaseModel):
    """
    That's an object that gets written to the migration file:
        id: just some hash
        worker: name of the worker to be triggered
        copy: CopyIndex object holding info about migration
        conflicts: informational field for the dev to know if generic reindex worker can handle this
            migration. If not, then new custom worker is required
        asynchronous: indicates if the migration can be performed asynchronously, if not, then it means it depends on
            other migrations, or other migrations depend on it
    """
    id: str
    copy_index: CopyIndex
    worker: str
    conflicts: Optional[List[FieldChange]] = None
    asynchronous: Optional[bool] = True
