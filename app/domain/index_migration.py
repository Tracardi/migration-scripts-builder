from pydantic import BaseModel
from typing import Optional, List
from app.domain.field_change import FieldChange
from uuid import uuid4


class IndexMigration(BaseModel):
    """
    That's an object that gets written to the migration file:
        id: just generic UUID4
        index: name of the index to be migrated
        multi: indicates if the index to be migrated is multi or not
        script: painless script to be used to reindex docs
        worker: name of the worker to be triggered
        custom_worker_required: informational field for the dev to know if generic reindex worker can handle this
            migration. If not, then new custom worker is required
        asynchronous: indicates if the migration can be performed asynchronously, if not, then it means it depends on
            other migrations, or other migrations depend on it
    """
    id: Optional[str] = str(uuid4())
    index: str
    multi: bool
    script: Optional[str] = None
    worker: str
    custom_worker_required: Optional[List[FieldChange]] = None
    asynchronous: Optional[bool] = True
