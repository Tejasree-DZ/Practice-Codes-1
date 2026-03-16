import logging
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth_service.auth_server.routers.base import make_router
from auth_service.auth_server.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from auth_service.auth_server.services.user import UserService
from auth_service.auth_server.dependencies import get_db, get_current_user
from auth_service.auth_server.exceptions import NotFoundException, ConflictException, WrongArgumentsException

LOG = logging.getLogger(__name__)
router = make_router(tags=["users"])

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    try:
        return UserService(db).create_user(data).to_schema()
    except ConflictException as e: raise HTTPException(status_code=409, detail=e.message)
    except WrongArgumentsException as e: raise HTTPException(status_code=400, detail=e.message)

@router.get("/users", response_model=UserListResponse)
def list_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    users, total = UserService(db).list_users(skip=skip, limit=limit)
    return UserListResponse(users=[u.to_schema() for u in users], total=total)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    try: return UserService(db).get_by_id(user_id).to_schema()
    except NotFoundException as e: raise HTTPException(status_code=404, detail=e.message)

@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, data: UserUpdate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    try: return UserService(db).update_user(user_id, data).to_schema()
    except NotFoundException as e: raise HTTPException(status_code=404, detail=e.message)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    try: UserService(db).delete_user(user_id)
    except NotFoundException as e: raise HTTPException(status_code=404, detail=e.message)