import strawberry
from strawberry.types import Info
from fastapi import  Depends
from strawberry.fastapi import BaseContext
from databases import Database

from src.db import get_db
from src.repositories import BookRepository, AuthorRepository


class Context(BaseContext):
    db: Database

    def __init__(
        self,
        db: Database = Depends(get_db),
    ) -> None:
        self.db = db


@strawberry.type
class Author:
    name: str


@strawberry.type
class Book:
    id: int
    title: str
    author: Author
    author_id: int


@strawberry.type
class Query:

    @strawberry.field
    async def books(
        self,
        info: Info[Context, None],
        author_ids: list[int] | None = None,
        search: str | None = None,
        limit: int | None = None,
    ) -> list[Book]:
        # TODO:
        # Do NOT use dataloaders
        await info.context.db.connect()  # это стоит вынести в lifespan(), но у меня не получилось завести его там

        book_repository = BookRepository(info.context.db)  # предполагал инжектить репозитории в объявлении метода,
        author_repository = AuthorRepository(info.context.db)  # но strawberry ругается на такое и я не понял как это правильно сделать

        res = await book_repository.get_books(author_ids=author_ids, search=search, limit=limit)
        book_fields = ['id', 'title', 'author_id']
        books = []
        for record in res:
            data = {field_name: record.get(field_name) for field_name in book_fields}
            author = await author_repository.get_authors(author_id=data['author_id'])
            data['author'] = Author(**author)
            book = Book(**data)
            books.append(book)

        return books

