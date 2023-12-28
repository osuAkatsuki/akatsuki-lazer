from typing import Literal

from pydantic import BaseModel

from app.models.api_hint import ApiHint


class OAuthSuccessResponse(BaseModel):
    token_type: str
    expires_in: int
    access_token: str
    refresh_token: str | None


class OAuthFailureResponse(BaseModel):
    authentication: str | None
    hint: ApiHint | None


class OAuthUnauthorizedResponse(BaseModel):
    authentication: Literal["basic"]
