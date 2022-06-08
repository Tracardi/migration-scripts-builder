from pydantic import BaseModel
from app.domain.reindex_endpoint import ReindexEndpoint
from typing import Optional, List
from app.domain.field_change import FieldChange


class IndexMigration(BaseModel):
    name: str
    multi: bool
    endpoint: ReindexEndpoint
    worker: str
    custom_worker_required: Optional[List[FieldChange]] = None
