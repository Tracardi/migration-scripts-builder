from pydantic import BaseModel
from app.domain.reindex_endpoint import ReindexEndpoint
from typing import Optional, List
from app.domain.field_change import FieldChange
from uuid import uuid4


class IndexMigration(BaseModel):
    id: Optional[str] = str(uuid4())
    name: str
    multi: bool
    endpoint: ReindexEndpoint
    worker: str
    custom_worker_required: Optional[List[FieldChange]] = None
