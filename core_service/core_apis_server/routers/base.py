import logging
from fastapi import APIRouter, Request
from sqlalchemy.orm import Session

from core_service.core_apis_server.exceptions import (
    Err, UnauthorizedException, FailedDependency
)

LOG = logging.getLogger(__name__)


def make_router(**kwargs) -> APIRouter:
    return APIRouter(**kwargs)


class BaseRouter:
    service_class = None

    def __init__(self, request: Request, session: Session, **kwargs):
        self._request      = request
        self._session      = session
        self._service      = None
        self._token        = None
        self._current_user = None

    @property
    def config(self):
        from core_service.core_apis_server.settings import settings
        return settings

    @property
    def token(self) -> str:
        token = getattr(self._request.state, "token", None)
        if not token:
            auth_header = self._request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                self._request.state.token = token
        if not token:
            raise UnauthorizedException(Err.OC0009)
        return token

    @property
    def current_user(self):
        cached_user = getattr(self._request.state, "user", None)
        if cached_user:
            return cached_user
        try:
            from core_service.core_apis_server.utils import decode_token
            user_id = decode_token(self.token)
            self._request.state.user_id = user_id
            return user_id
        except UnauthorizedException:
            raise
        except Exception:
            raise UnauthorizedException(Err.OC0008)

    @property
    def user_id(self) -> str:
        user_id = getattr(self._request.state, "user_id", None)
        if not user_id:
            return self.current_user
        return user_id

    @property
    def session(self) -> Session:
        return self._session

    @property
    def service(self):
        if self.service_class is None:
            raise NotImplementedError(
                f"{self.__class__.__name__} must define service_class"
            )
        if self._service is None:
            self._service = self.service_class(
                db_session=self._session,
                token=self.token,
                request=self._request,
            )
        return self._service

    @property
    def request(self) -> Request:
        return self._request

    @property
    def client_ip(self) -> str:
        return self._request.client.host if self._request.client else "unknown"