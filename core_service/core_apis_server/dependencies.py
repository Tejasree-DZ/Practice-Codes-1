import logging
from typing import Generator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core_service.core_apis_server.models.db_postgres import postgres_db
from core_service.core_apis_server.utils import decode_token
from core_service.core_apis_server.exceptions import InvalidTokenException

LOG = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/auth/v1/token")


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


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        user_id = decode_token(token)
        return user_id
    except InvalidTokenException as e:
        raise HTTPException(status_code=401, detail=e.message)