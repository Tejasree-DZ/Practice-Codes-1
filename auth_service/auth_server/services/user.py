import logging
from sqlalchemy.orm import Session
from auth_service.auth_server.models.models import User
from auth_service.auth_server.utils import hash_password, verify_password, get_current_timestamp
from auth_service.auth_server.exceptions import Err, NotFoundException, ConflictException, UnauthorizedException
from auth_service.auth_server.schemas.user import UserCreate, UserUpdate

LOG = logging.getLogger(__name__)

class UserService:
    def __init__(self, db: Session): self.db = db

    def get_by_id(self, user_id: str) -> User:
        user = self.db.query(User).filter(User.id == user_id, User.deleted_at == 0).first()
        if not user: raise NotFoundException(Err.OA0043, [user_id])
        return user

    def get_by_mail(self, mail: str) -> User | None:
        return self.db.query(User).filter(User.mail == mail, User.deleted_at == 0).first()

    def list_users(self, skip: int = 0, limit: int = 20):
        query = self.db.query(User).filter(User.deleted_at == 0)
        total = query.count()
        return query.offset(skip).limit(limit).all(), total

    def create_user(self, data: UserCreate) -> User:
        if self.get_by_mail(data.mail): raise ConflictException(Err.OA0042, [data.mail])
        user = User(mail=data.mail, name=data.name)
        user.password = hash_password(data.password, user.salt)
        user.created_at = get_current_timestamp()
        self.db.add(user); self.db.commit(); self.db.refresh(user)
        LOG.info("Created user %s", user.id)
        return user

    def update_user(self, user_id: str, data: UserUpdate) -> User:
        user = self.get_by_id(user_id)
        if data.name is not None: user.name = data.name
        if data.password is not None: user.password = hash_password(data.password, user.salt)
        if data.is_active is not None: user.is_active = data.is_active
        self.db.commit(); self.db.refresh(user)
        return user

    def delete_user(self, user_id: str):
        user = self.get_by_id(user_id)
        user.deleted_at = get_current_timestamp()
        self.db.commit()

    def authenticate(self, mail: str, password: str) -> User:
        user = self.get_by_mail(mail)
        if not user: raise UnauthorizedException(Err.OA0037)
        if not user.is_active: raise UnauthorizedException(Err.OA0038)
        if not verify_password(password, user.salt, user.password): raise UnauthorizedException(Err.OA0037)
        user.last_login = get_current_timestamp()
        self.db.commit()
        return user