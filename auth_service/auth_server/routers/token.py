from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth_server.services.base import get_db
from auth_server.services import token as token_service

router = APIRouter(prefix="/token", tags=["Authentication"])


@router.post("")
def login(email: str, password: str, db: Session = Depends(get_db)):
    return token_service.login(db, email, password)