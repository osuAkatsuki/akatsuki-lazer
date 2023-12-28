from typing import TYPE_CHECKING

from databases import Database
from redis.asyncio import Redis

import settings
from app.adapters import database as database_adapter

if TYPE_CHECKING:
    ...

database = Database(
    url=database_adapter.create_database_url(
        dialect=settings.DB_DIALECT,
        driver=settings.DB_DRIVER,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASS,
    ),
)
redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    username=settings.REDIS_USER,
    password=settings.REDIS_PASS,
    ssl=settings.REDIS_USE_SSL,
)