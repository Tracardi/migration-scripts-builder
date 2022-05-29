from pydantic import BaseModel


class Field(BaseModel):
    """
    Represents mapping field:
        field="field.name.here",
        type="elastic-field-type"
    """
    name: str
    type: str
