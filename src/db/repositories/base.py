from typing import Sequence, Iterable, Mapping, Any

from sqlalchemy import Table
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import Session


class BaseRepository:
    table: Table
    pk: Sequence[str]
    updatable: Sequence[str]

    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert_many(self, rows: Iterable[Mapping[str, Any]]) -> int:
        rows = list(rows)

        if not rows:
            return 0

        stmt = insert(self.table).values(rows)
        update_map = {col: stmt.inserted[col] for col in self.updatable}
        stmt = stmt.on_duplicate_key_update(**update_map)
        result = self.session.execute(stmt)

        return result.rowcount or 0