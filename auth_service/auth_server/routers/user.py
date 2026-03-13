from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth_server.services.base import get_db
from auth_server.services import user as user_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("")
def create_user(user, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)


@router.get("")
def get_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(db, user_id)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db, user_id)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db, user_id)