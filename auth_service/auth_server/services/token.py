import logging
from fastapi import Request
from sqlalchemy.orm import Session

from auth_service.auth_server.services.user import UserService
from auth_service.auth_server.utils import (
    create_access_token, create_refresh_token, decode_token
)
from auth_service.auth_server.models.enums import TokenType
from auth_service.auth_server.schemas.token import (
    TokenResponse, TokenRequest, RefreshTokenRequest
)
from auth_service.auth_server.exceptions import Err, UnauthorizedException

LOG = logging.getLogger(__name__)


class TokenService:

    def __init__(self, db: Session, request: Request = None, **kwargs):
        self._session     = db
        self._request     = request
        self.user_service = UserService(db, request)

    def login(self, data: TokenRequest) -> TokenResponse:
        user = self.user_service.authenticate(data.mail, data.password)
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    def refresh(self, data: RefreshTokenRequest) -> TokenResponse:
        user_id = decode_token(data.refresh_token, TokenType.REFRESH)
        user    = self.user_service.get_by_id(user_id)
        if not user.is_active:
            raise UnauthorizedException(Err.OA0038)
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )