from src.graphql.schema import Query, Context
from functools import partial
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter



schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(  # type: ignore
    schema,
    context_getter=partial(Context, ),
)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")