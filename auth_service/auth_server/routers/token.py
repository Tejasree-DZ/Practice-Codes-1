import logging
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from auth_service.auth_server.routers.base import make_router, BaseRouter
from auth_service.auth_server.schemas.token import (
    TokenRequest, RefreshTokenRequest, TokenResponse
)
from auth_service.auth_server.services.token import TokenService
from auth_service.auth_server.dependencies import get_db
from auth_service.auth_server.exceptions import (
    UnauthorizedException, InvalidTokenException
)

LOG = logging.getLogger(__name__)
router = make_router(tags=["token"])


class TokenRouter(BaseRouter):
    service_class = TokenService


@router.post("/token", response_model=TokenResponse)
def login(
    request: Request,
    data: TokenRequest,
    db: Session = Depends(get_db),
):
    try:
        return TokenRouter(request, db).service.login(data)
    except UnauthorizedException as e:
        raise HTTPException(status_code=401, detail=e.message)


@router.post("/refresh_token", response_model=TokenResponse)
def refresh_token(
    request: Request,
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    try:
        return TokenRouter(request, db).service.refresh(data)
    except (UnauthorizedException, InvalidTokenException) as e:
        raise HTTPException(status_code=401, detail=e.message)