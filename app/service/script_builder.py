from pydantic import BaseModel
from app.domain.operation import Operation
from typing import List


class ScriptBuilder(BaseModel):
    operations: List[Operation]

    def build(self):
        script = ""

        for operation in self.operations:
            try:
                script += "//" + ';\n//'.join(self.__getattribute__(operation.type)(operation)) + ";\n"

            except AttributeError as _:
                print(f"ScriptBuilder: No operation function defined for operation type {operation.type}.")

        return 'Map temp = new HashMap();\n' \
               'temp.putAll(ctx._source);\n' \
               f'{script}' \
               'ctx._source = [:];\n' \
               'ctx._source.putAll(temp);' if self.operations else None

    @classmethod
    def rewrite(cls, op: Operation) -> List[str]:
        return [
            f"temp.{op.destination} = ctx._source.{op.source}"
        ]

    @classmethod
    def cast(cls, op: Operation) -> List[str]:
        return [
            f"temp.{op.destination} = ({op.cast})ctx._source.{op.source}"
        ]

    @classmethod
    def long_to_date(cls, op: Operation) -> List[str]:
        return [
            f"temp.{op.destination} = Instant.ofEpochMilli(ctx._source.{op.source}).toString().replace(\"Z\", \"\")",
        ]

    @classmethod
    def date_to_long(cls, op: Operation) -> List[str]:
        return [
            f"temp.{op.destination} = Instant.parse(ctx._source.{op.source} + \"Z\").toEpochMilli()"
        ]

    @classmethod
    def remove(cls, op: Operation) -> List[str]:
        path = op.source.split(".")
        return [
            f"temp.{'.'.join(path[:-1]) + '.' if path[:-1] else '' }remove(\"{path[-1]}\")"
        ]

    @classmethod
    def add(cls, op: Operation) -> List[str]:
        return [
            f"temp.{op.source} = <type {op.cast}>"
        ]
