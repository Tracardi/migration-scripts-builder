from pydantic import BaseModel
from app.domain.operation import Operation
from typing import List


class IndexOperations(BaseModel):
    for_worker: List[Operation]
    for_script: List[Operation]
