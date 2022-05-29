from pydantic import BaseModel
from typing import Optional


class Operation(BaseModel):
    for_worker: bool
    type: str
    source: str
    destination: str
    cast: Optional[str] = None
