import logging
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth_service.auth_server.routers.base import make_router
from auth_service.auth_server.services.role import RoleService
from auth_service.auth_server.schemas.role import RoleResponse, RoleListResponse
from auth_service.auth_server.dependencies import get_db, get_current_user
from auth_service.auth_server.exceptions import NotFoundException

LOG = logging.getLogger(__name__)
router = make_router(tags=["roles"])


@router.get("/roles", response_model=RoleListResponse)
def list_roles(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    roles = RoleService(db).list_roles()
    return RoleListResponse(roles=[r.to_schema() for r in roles], total=len(roles))


@router.get("/roles/{role_id}", response_model=RoleResponse)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    try:
        role = RoleService(db).get_by_id(role_id)
        return role.to_schema()
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)