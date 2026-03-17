import logging
from fastapi import Request
from sqlalchemy.orm import Session

from auth_service.auth_server.models.models import User
from auth_service.auth_server.services.base import BaseService
from auth_service.auth_server.utils import (
    hash_password, verify_password, get_current_timestamp
)
from auth_service.auth_server.exceptions import (
    Err, ConflictException, UnauthorizedException
)
from auth_service.auth_server.schemas.user import UserCreate, UserUpdate

LOG = logging.getLogger(__name__)


class UserService(BaseService):

    def __init__(self, db: Session, request: Request = None, **kwargs):
        super().__init__(db, request, **kwargs)

    def _get_model_type(self):
        return User

    def get_by_mail(self, mail: str) -> User | None:
        return self._session.query(User).filter(
            User.mail      == mail,
            User.deleted_at == 0,
        ).first()

    def create_user(self, data: UserCreate) -> User:
        if self.get_by_mail(data.mail):
            raise ConflictException(Err.OA0042, [data.mail])
        user          = User(mail=data.mail, name=data.name)
        user.password = hash_password(data.password, user.salt)
        return self.save(user)

    def update_user(self, user_id: str, data: UserUpdate) -> User:
        user = self.get_by_id(user_id)
        if data.name is not None:
            user.name = data.name
        if data.password is not None:
            user.password = hash_password(data.password, user.salt)
        if data.is_active is not None:
            user.is_active = data.is_active
        return self.update(user)

    def delete_user(self, user_id: str):
        self.soft_delete(user_id)

    def authenticate(self, mail: str, password: str) -> User:
        user = self.get_by_mail(mail)
        if not user:
            raise UnauthorizedException(Err.OA0037)
        if not user.is_active:
            raise UnauthorizedException(Err.OA0038)
        if not verify_password(password, user.salt, user.password):
            raise UnauthorizedException(Err.OA0037)
        user.last_login = get_current_timestamp()
        self._session.commit()
        return user