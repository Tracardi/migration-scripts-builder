from pydantic import BaseModel
from app.domain.operation import Operation
from typing import List


class ScriptBuilder(BaseModel):
    operations: List[Operation]

    def build(self):
        script = ""

        for operation in self.operations:
            pass

        return 'Map temp = new HashMap();\n' \
               'temp.putAll(ctx._source);\n' \
               f'{script}' \
               'ctx._source = [:];\n' \
               'ctx._source.putAll(temp);'
