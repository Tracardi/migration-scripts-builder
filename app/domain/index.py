from pydantic import BaseModel
from typing import Dict


class Index(BaseModel):
    name: str
    multi: bool
    mapping: Dict[str, str] = {}
