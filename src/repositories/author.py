from typing import Any

from databases import Database


class AuthorRepository:
    def __init__(self, db: Database):
        self.db = db

    async def get_authors(self, author_id: int) -> dict[str, Any]:
        result = await self.db.fetch_one("SELECT name FROM authors WHERE id = :author_id", {'author_id': author_id})
        return dict(result)
