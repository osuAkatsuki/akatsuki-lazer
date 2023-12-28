from datetime import datetime

import app.clients
from app.models.api_session import ApiSession


def format_redis_key(access_token: str) -> str:
    return f"akatsuki:lazer:sessions:{access_token}"


async def add(
    token_type: str,
    access_token: str,
    refresh_token: str,
    expires_at: datetime,
    user_id: int,
) -> ApiSession:
    api_session = ApiSession(
        token_type=token_type,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
        user_id=user_id,
    )
    await app.clients.redis.set(
        name=format_redis_key(access_token),
        value=api_session.model_dump_json(),
        ex=expires_at - datetime.utcnow(),
    )

    return api_session


async def get_by_access_token(access_token: str) -> ApiSession | None:
    redis_session = await app.clients.redis.get(name=format_redis_key(access_token))
    if redis_session is None:
        return None

    api_session = ApiSession.model_validate_json(redis_session)
    return api_session
