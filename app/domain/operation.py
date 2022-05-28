from pydantic import BaseModel
from typing import Optional


class Operation(BaseModel):
    type: str
    source: str
    destination: str
    cast: Optional[str] = None
