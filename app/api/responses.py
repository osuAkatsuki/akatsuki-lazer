from fastapi import status
from fastapi.responses import ORJSONResponse

from app.api.dtos.oauth import OAuthFailureResponse
from app.api.dtos.oauth import OAuthUnauthorizedResponse
from app.models.api_hint import ApiHint


def create_unauthorized_response() -> ORJSONResponse:
    return ORJSONResponse(
        content=OAuthUnauthorizedResponse(authentication="basic"),
        status_code=status.HTTP_401_UNAUTHORIZED,
    )


def create_oauth_failure_response(
    authentication: str | None = None,
    hint: ApiHint | None = None,
) -> ORJSONResponse:
    return ORJSONResponse(
        content=OAuthFailureResponse(authentication=authentication, hint=hint),
        status_code=status.HTTP_400_BAD_REQUEST,
    )
