import logging
from fastapi import Depends, Request, status, HTTPException
from sqlalchemy.orm import Session

from core_service.core_apis_server.routers.base import make_router, BaseRouter
from core_service.core_apis_server.services.organization import OrganizationService
from core_service.core_apis_server.schemas.organization import (
    OrganizationCreate, OrganizationUpdate,
    OrganizationResponse, OrganizationListResponse
)
from core_service.core_apis_server.dependencies import get_db, get_current_user
from core_service.core_apis_server.exceptions import (
    NotFoundException, ConflictException, WrongArgumentsException
)

LOG    = logging.getLogger(__name__)
router = make_router(prefix="/core/v1", tags=["organizations"])


class OrganizationRouter(BaseRouter):
    service_class = OrganizationService


def get_organization_router(
    request: Request,
    session: Session = Depends(get_db),
) -> OrganizationRouter:
    return OrganizationRouter(request, session)


@router.post("/organizations",
             response_model=OrganizationResponse,
             status_code=status.HTTP_201_CREATED)
async def create_organization(
    payload: OrganizationCreate,
    service_router: OrganizationRouter = Depends(get_organization_router),
    _: str = Depends(get_current_user),
):
    try:
        return await service_router.service.create_organization(
            service_router.user_id, payload)
    except ConflictException as e:
        raise HTTPException(status_code=409, detail=e.message)
    except WrongArgumentsException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get("/organizations",
            response_model=OrganizationListResponse)
async def list_organizations(
    skip: int = 0,
    limit: int = 20,
    service_router: OrganizationRouter = Depends(get_organization_router),
    _: str = Depends(get_current_user),
):
    organizations, total = await service_router.service.list_organizations(
        skip=skip, limit=limit)
    return OrganizationListResponse(
        organizations=[o.to_schema() for o in organizations],
        total=total,
    )


@router.get("/organizations/{organization_id}",
            response_model=OrganizationResponse)
async def get_organization(
    organization_id: str,
    service_router: OrganizationRouter = Depends(get_organization_router),
    _: str = Depends(get_current_user),
):
    try:
        return (await service_router.service.get_organization(
            organization_id)).to_schema()
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.patch("/organizations/{organization_id}",
              response_model=OrganizationResponse)
async def update_organization(
    organization_id: str,
    payload: OrganizationUpdate,
    service_router: OrganizationRouter = Depends(get_organization_router),
    _: str = Depends(get_current_user),
):
    try:
        return (await service_router.service.update_organization(
            organization_id, payload)).to_schema()
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.delete("/organizations/{organization_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    organization_id: str,
    service_router: OrganizationRouter = Depends(get_organization_router),
    _: str = Depends(get_current_user),
):
    try:
        await service_router.service.delete_organization(organization_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)