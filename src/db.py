from databases import Database

from src.settings import db_settings

db = Database(db_settings.DSN)

async def get_db() -> Database:
    try:
        await db.connect()
        yield db
    finally:
        await db.disconnect()

