#!/usr/bin/env python3
import atexit
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi.responses import ORJSONResponse
from fastapi import FastAPI

import app.exception_handling
import app.logging
import app.clients
import settings
from app.api import oauth

@asynccontextmanager
async def lifespan(asgi_app: FastAPI) -> AsyncIterator[None]:
    try:
        await app.clients.database.connect()
        await app.clients.redis.ping()
        yield
    finally:
        await app.clients.database.disconnect()
        await app.clients.redis.aclose()

asgi_app = FastAPI(lifespan=lifespan, default_response_class=ORJSONResponse)

@asgi_app.get("/_health")
async def health():
    return {"status": "ok"}

asgi_app.include_router(oauth.router)

def main() -> int:
    app.logging.configure_logging()

    app.exception_handling.hook_exception_handlers()
    atexit.register(app.exception_handling.unhook_exception_handlers)

    uvicorn.run(
        "main:asgi_app",
        reload=settings.CODE_HOTRELOAD,
        server_header=False,
        date_header=False,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        access_log=False,
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())