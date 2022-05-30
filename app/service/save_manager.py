from app.domain.index_migration import IndexMigration
from typing import List
import json


class SaveManager:

    @staticmethod
    def save_migrations(migrations: List[IndexMigration], name: str) -> None:

        with open(f'tmp/{name}.json', mode="w+") as migration_file:

            json.dump([mig.dict() for mig in migrations], migration_file, indent=2)
