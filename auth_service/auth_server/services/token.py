from datetime import timedelta
from sqlalchemy.orm import Session
from auth_server.models.models import User
from auth_server.utils import verify_password, create_access_token
from auth_server.settings import settings


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


def login(db: Session, email: str, password: str):

    user = authenticate_user(db, email, password)

    if not user:
        return None

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }