from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth_server.services.base import get_db
from auth_server.services import type as type_service

router = APIRouter(prefix="/types", tags=["Types"])


@router.get("")
def get_types(db: Session = Depends(get_db)):
    return type_service.get_types(db)