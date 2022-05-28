from pydantic import BaseModel
from app.domain.mappings_difference import MappingsDifference
from app.domain.operation import Operation
from typing import List


class RulesEngine(BaseModel):
    difference: MappingsDifference

    def get_operations(self) -> List[Operation]:
        ops = []

        return ops
