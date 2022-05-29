from pydantic import BaseModel
from typing import Optional


class Operation(BaseModel):
    """
    Represents one operation, which can be translated into painless script, or operation for Tracardi worker:
        for_worker = whether the operation should be performed by script or the worker,
        type = operation type, for example generic "cast" or "rewrite",
        source = value to perform the operation on, for example "some.field",
        destination = field to assign the operation result to, for example "some.other.field",
        cast = data type that the source should be casted to before assignment to destination field.
    """
    for_worker: bool
    type: str
    source: str
    destination: str
    cast: Optional[str] = None
