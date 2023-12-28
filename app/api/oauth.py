import secrets
from datetime import datetime
from datetime import timedelta

from fastapi import APIRouter
from fastapi import Form
from fastapi.responses import ORJSONResponse

import settings
from app.adapters import cryptography as cryptography_adapter
from app.adapters import password as password_adapter
from app.api import responses
from app.api.dtos.oauth import OAuthFailureResponse
from app.api.dtos.oauth import OAuthSuccessResponse
from app.api.dtos.oauth import OAuthUnauthorizedResponse
from app.models.api_hint import ApiHint
from app.models.api_scope import ApiScope
from app.repositories import api_sessions as api_sessions_repository
from app.repositories import users as users_repository

router = APIRouter(default_response_class=ORJSONResponse)


@router.post(
    "/oauth/token",
    response_model=OAuthSuccessResponse
    | OAuthFailureResponse
    | OAuthUnauthorizedResponse,
)
async def oauth_token(
    username: str | None = Form(None),
    password: str | None = Form(None),
    grant_type: str = Form(...),
    client_id: int = Form(...),
    client_secret: str = Form(...),
    scope: str = Form(...),
):
    requested_scopes = [
        ApiScope(requested_scope) for requested_scope in scope.split(",")
    ]

    # if it's a lazer client then it must have ApiScope.ALL
    # we will maybe support oauth for non lazer clients at some point
    if ApiScope.ALL not in requested_scopes:
        return responses.create_unauthorized_response()

    # lazer has static client ids & secrets per environment
    # ref: https://github.com/ppy/osu/blob/master/osu.Game/Online/DevelopmentEndpointConfiguration.cs
    # ref: https://github.com/ppy/osu/blob/master/osu.Game/Online/ExperimentalEndpointConfiguration.cs
    # ref: https://github.com/ppy/osu/blob/master/osu.Game/Online/ProductionEndpointConfiguration.cs
    if (
        client_id not in settings.ALLOWED_LAZER_CLIENT_IDS
        or client_secret not in settings.ALLOWED_LAZER_CLIENT_SECRETS
    ):
        return responses.create_unauthorized_response()

    # lazer can only use the password grant type
    # TODO: grant type enum
    if grant_type != "password":
        return responses.create_unauthorized_response()

    if username is None or password is None:
        return responses.create_oauth_failure_response(
            hint=ApiHint.USERNAME_OR_PASSWORD_INCORRECT,
        )

    password_md5 = cryptography_adapter.calculate_md5(password)

    user = await users_repository.get_by_username(username)
    if user is None:
        return responses.create_oauth_failure_response(
            hint=ApiHint.USERNAME_OR_PASSWORD_INCORRECT,
        )

    correct_password = await password_adapter.verify_password(
        password_md5,
        user.hashed_password,
    )
    if not correct_password:
        return responses.create_oauth_failure_response(
            hint=ApiHint.USERNAME_OR_PASSWORD_INCORRECT,
        )

    access_token = secrets.token_urlsafe(16)
    refresh_token = secrets.token_urlsafe(16)
    expires_at = datetime.utcnow() + timedelta(
        seconds=settings.OAUTH_ACCESS_TOKEN_VALIDITY_SECONDS,
    )

    api_session = await api_sessions_repository.add(
        token_type="Bearer",
        access_token=access_token,
        refresh_token=refresh_token,
        expires_at=expires_at,
        user_id=user.id,
    )

    expires_in = api_session.expires_at - datetime.utcnow()
    expires_in_seconds = int(expires_in.total_seconds())

    return OAuthSuccessResponse(
        token_type=api_session.token_type,
        expires_in=expires_in_seconds,
        access_token=api_session.access_token,
        refresh_token=api_session.refresh_token,
    )
