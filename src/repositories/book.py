from typing import Any

from databases import Database


class BookRepository:
    db: Database

    def __init__(self, db: Database):  # изначально хотел инжектить db через Depends(), но что-то у меня не завелось
        self.db = db

    async def get_books(self,         author_ids: list[int] | None = None,
        search: str | None = None,
        limit: int | None = None,) -> list[dict[str, Any]]:

        if author_ids is None:
            author_ids = []

        query = "SELECT * FROM books"
        conditions = []
        params = {}
        if author_ids:
            conditions.append("  author_id IN (%s)" % ','.join(map(str,author_ids)))

        if search:
            conditions.append('title ilike :search')
            params['search'] = '%'+search+'%'

        if any([author_ids, search]):
            condition_statement = ' AND '.join(conditions)
            query += ' WHERE ' + condition_statement

        if limit:
            query += " LIMIT :limit"
            params['limit'] = limit

        response = await self.db.fetch_all(query, values=params)
        return [dict(record) for record in response]

