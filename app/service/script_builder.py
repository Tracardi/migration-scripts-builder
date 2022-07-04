from pydantic import BaseModel
from app.domain.operation import Operation
from typing import List
import logging

logger = logging.getLogger(__name__)


class ScriptBuilder(BaseModel):
    operations: List[Operation]

    def build(self):
        script = ""

        for operation in self.operations:
            try:
                script += "//" + ';\n//'.join(self.__getattribute__(operation.type)(operation)) + ";\n"

            except AttributeError as _:
                logger.log(msg=f"ScriptBuilder: No operation function defined for operation type {operation.type}.",
                           level=logging.WARN)

        return 'Map row = new HashMap();\n' \
               'row.putAll(ctx._source);\n' \
               f'{script}' \
               'ctx._source = [:];\n' \
               'ctx._source.putAll(row);' if self.operations else None

    @staticmethod
    def rewrite(op: Operation) -> List[str]:
        return [
            f"row.{op.destination} = ctx._source.{op.source}"
        ]

    @staticmethod
    def cast(op: Operation) -> List[str]:
        return [
            f"row.{op.destination} = ({op.cast})ctx._source.{op.source}"
        ]

    @staticmethod
    def long_to_date(op: Operation) -> List[str]:
        return [
            f"row.{op.destination} = Instant.ofEpochMilli(ctx._source.{op.source}).toString().replace(\"Z\", \"\")",
        ]

    @staticmethod
    def date_to_long(op: Operation) -> List[str]:
        return [
            f"row.{op.destination} = Instant.parse(ctx._source.{op.source} + \"Z\").toEpochMilli()"
        ]

    @staticmethod
    def remove(op: Operation) -> List[str]:
        path = op.source.split(".")
        return [
            f"row.{'.'.join(path[:-1]) + '.' if path[:-1] else '' }remove(\"{path[-1]}\")"
        ]

    @staticmethod
    def add(op: Operation) -> List[str]:
        return [
            f"row.{op.source} = <type {op.cast}>"
        ]
