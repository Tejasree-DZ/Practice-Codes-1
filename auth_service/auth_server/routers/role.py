from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth_server.services.base import get_db
from auth_server.services import role as role_service

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("")
def get_roles(db: Session = Depends(get_db)):
    return role_service.get_roles(db)