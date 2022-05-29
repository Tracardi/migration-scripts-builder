from pydantic import BaseModel


class FieldChange(BaseModel):
    """
    Represents field type change between mappings:
        name="some.field.here",
        old_type="elasticsearch-field-type1",
        new_type="elasticsearch-field-type2"
    """
    name: str
    old_type: str
    new_type: str
