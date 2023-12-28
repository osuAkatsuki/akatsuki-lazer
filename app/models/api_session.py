from datetime import datetime

from pydantic import BaseModel


class ApiSession(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
    expires_at: datetime
    user_id: int
