from pydantic import BaseModel
from app.domain.operation import Operation
from typing import List


class PainlessTranslator(BaseModel):
    operations: List[Operation]

    def generate_script(self) -> dict:
        script = ""

        for operation in self.operations:
            if operation.type == "cast":
                script += f"// ctx._source.{operation.destination} = ({operation.cast})ctx._source.{operation.source}\n"

            elif operation.type == "potential_type_conflict":
                script += f"// POTENTIAL TYPE CONFLICT IN THE LINE BELOW\n" \
                          f"// ctx._source.{operation.destination} = ({operation.cast})ctx._source.{operation.source}\n"

            elif operation.type == "user_input":
                script += f"// ctx._source.{operation.destination} = {operation.source}\n"

        return {"script": {"source": script, "lang": "painless"}}
