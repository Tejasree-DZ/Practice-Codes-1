import logging
from fastapi import APIRouter, Request
from sqlalchemy.orm import Session

from auth_service.auth_server.exceptions import (
    Err, UnauthorizedException, ForbiddenException
)

LOG = logging.getLogger(__name__)


def make_router(**kwargs) -> APIRouter:
    return APIRouter(**kwargs)


class BaseRouter:
    service_class = None

    def __init__(self, request: Request, session: Session, **kwargs):
        self._request        = request
        self._session        = session
        self._service        = None
        self._token          = None
        self._current_user   = None

    @property
    def config(self):
        """
        Returns app-level config stored in request.app.state.
        Raises FailedDependency if config is not set.
        """
        from auth_service.auth_server.settings import settings
        return settings

    @property
    def token(self) -> str:
        """
        Returns the JWT token from request state.
        Raises UnauthorizedException if token is missing.
        """
        token = getattr(self._request.state, "token", None)
        if not token:
            # fallback — read from Authorization header
            auth_header = self._request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                self._request.state.token = token
        if not token:
            raise UnauthorizedException(Err.OA0062)
        return token

    @property
    def current_user(self):
        """
        Returns the current authenticated user from request state.
        Decodes JWT token and fetches user from DB if not cached.
        """
        cached_user = getattr(self._request.state, "user", None)
        if cached_user:
            return cached_user
        try:
            from auth_service.auth_server.utils import decode_token
            from auth_service.auth_server.models.enums import TokenType
            from auth_service.auth_server.models.models import User
            user_id = decode_token(self.token, TokenType.ACCESS)
            user = self._session.query(User).filter(
                User.id == user_id,
                User.deleted_at == 0,
            ).first()
            if not user:
                raise UnauthorizedException(Err.OA0024, [user_id])
            if not user.is_active:
                raise UnauthorizedException(Err.OA0038)
            self._request.state.user = user
            return user
        except UnauthorizedException:
            raise
        except Exception:
            raise UnauthorizedException(Err.OA0011)

    @property
    def user_id(self) -> str:
        """Returns current user id."""
        return self.current_user.id

    @property
    def user_mail(self) -> str:
        """Returns current user email."""
        return self.current_user.mail

    @property
    def is_active(self) -> bool:
        """Returns whether current user is active."""
        return self.current_user.is_active

    @property
    def session(self) -> Session:
        """Returns the database session."""
        return self._session

    @property
    def service(self):
        """
        Lazily initialises and returns the service instance.
        service_class must be set in the subclass.

        Example:
            class UserRouter(BaseRouter):
                service_class = UserService
        """
        if self.service_class is None:
            raise NotImplementedError(
                f"{self.__class__.__name__} must define service_class"
            )
        if self._service is None:
            self._service = self.service_class(
                db=self._session,
                request=self._request,
            )
        return self._service

    @property
    def request(self) -> Request:
        """Returns the raw FastAPI request object."""
        return self._request

    @property
    def client_ip(self) -> str:
        """Returns the client IP address from the request."""
        return self._request.client.host if self._request.client else "unknown"

    @property
    def method(self) -> str:
        """Returns the HTTP method of the request."""
        return self._request.method

    @property
    def path(self) -> str:
        """Returns the URL path of the request."""
        return self._request.url.path