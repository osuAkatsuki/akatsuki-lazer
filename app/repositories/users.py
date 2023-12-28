import app.clients
from app.models.user import User


async def get_by_username(username: str) -> User | None:
    safe_username = username.lower().replace(" ", "_")

    rec = await app.clients.database.fetch_one(
        "SELECT id, username, password_md5 AS hashed_password FROM users WHERE username_safe = :safe_username",
        {"safe_username": safe_username},
    )
    if rec is None:
        return None

    user = User.model_validate(dict(rec._mapping))
    return user
