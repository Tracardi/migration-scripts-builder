from pydantic import BaseModel
from app.domain.reindex_endpoint import ReindexEndpoint
from app.domain.operation import Operation
from typing import List


class IndexMigration(BaseModel):
    name: str
    multi: bool
    endpoint: ReindexEndpoint
    worker_operations: List[Operation]
