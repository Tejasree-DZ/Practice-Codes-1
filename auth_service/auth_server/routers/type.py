import logging
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth_service.auth_server.routers.base import make_router
from auth_service.auth_server.services.type import TypeService
from auth_service.auth_server.schemas.type import TypeResponse, TypeListResponse
from auth_service.auth_server.dependencies import get_db, get_current_user
from auth_service.auth_server.exceptions import NotFoundException

LOG = logging.getLogger(__name__)
router = make_router(tags=["types"])


@router.get("/types", response_model=TypeListResponse)
def list_types(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    types = TypeService(db).list_types()
    return TypeListResponse(types=[t.to_schema() for t in types], total=len(types))


@router.get("/types/{type_id}", response_model=TypeResponse)
def get_type(
    type_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    try:
        type_ = TypeService(db).get_by_id(type_id)
        return type_.to_schema()
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)