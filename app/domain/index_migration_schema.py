from pydantic import BaseModel
from app.domain.index_migration import IndexMigration
from app.domain.reindex_endpoint import ReindexEndpoint, EndpointBody, IndexName, PainlessScript
from app.service.script_builder import ScriptBuilder
from typing import List
from app.domain.operation import Operation


class IndexMigrationSchema(BaseModel):
    name: str
    multi: bool
    operations: List[Operation]

    def build_migration(self, old_prefix: str, new_prefix: str) -> IndexMigration:
        return IndexMigration(
            name=self.name,
            multi=self.multi,
            endpoint=ReindexEndpoint(
                body=EndpointBody(
                    source=IndexName(
                        index=f"{old_prefix}.{self.name}" if old_prefix else self.name,
                    ),
                    dest=IndexName(index=f"{new_prefix}.{self.name}"),
                    script=PainlessScript(
                        source=ScriptBuilder(operations=self.operations).build()
                    )
                )
            ),
            worker="reindex"
        )
