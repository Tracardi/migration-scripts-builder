from pydantic import BaseModel


class FieldChange(BaseModel):
    name: str
    old_type: str
    new_type: str
