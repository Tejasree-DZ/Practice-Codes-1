import logging
from typing import Generator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from auth_service.auth_server.models.db_postgres import postgres_db
from auth_service.auth_server.models.enums import TokenType
from auth_service.auth_server.utils import decode_token
from auth_service.auth_server.exceptions import InvalidTokenException

LOG = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/v1/token")


def get_db() -> Generator[Session, None, None]:
    session_factory = postgres_db.session(postgres_db.engine)
    db = session_factory()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        session_factory.remove()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> str:
    try:
        user_id = decode_token(token, TokenType.ACCESS)
        from auth_service.auth_server.models.models import User
        user = db.query(User).filter(
            User.id == user_id,
            User.deleted_at == 0,
        ).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        if not user.is_active:
            raise HTTPException(status_code=401, detail="User is inactive")
        return user_id
    except InvalidTokenException as e:
        raise HTTPException(status_code=401, detail=e.message)