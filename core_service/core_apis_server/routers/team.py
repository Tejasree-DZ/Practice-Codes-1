import logging
from fastapi import Depends, Request, status, HTTPException
from sqlalchemy.orm import Session

from core_service.core_apis_server.routers.base import make_router, BaseRouter
from core_service.core_apis_server.services.team import TeamService
from core_service.core_apis_server.schemas.team import (
    TeamCreate, TeamUpdate, TeamResponse, TeamListResponse
)
from core_service.core_apis_server.dependencies import get_db, get_current_user
from core_service.core_apis_server.exceptions import (
    NotFoundException, ConflictException, WrongArgumentsException
)

LOG    = logging.getLogger(__name__)
router = make_router(prefix="/core/v1", tags=["teams"])


class TeamRouter(BaseRouter):
    service_class = TeamService


def get_team_router(
    request: Request,
    session: Session = Depends(get_db),
) -> TeamRouter:
    return TeamRouter(request, session)


@router.post("/organization/{organization_id}/teams",
             response_model=TeamResponse,
             status_code=status.HTTP_201_CREATED)
async def create_team(
    organization_id: str,
    payload: TeamCreate,
    service_router: TeamRouter = Depends(get_team_router),
    _: str = Depends(get_current_user),
):
    try:
        return (await service_router.service.create_team(
            organization_id, payload)).to_schema()
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ConflictException as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.get("/organization/{organization_id}/teams",
            response_model=TeamListResponse)
async def list_teams(
    organization_id: str,
    skip: int = 0,
    limit: int = 20,
    service_router: TeamRouter = Depends(get_team_router),
    _: str = Depends(get_current_user),
):
    teams, total = await service_router.service.list_teams_by_organization(
        organization_id, skip=skip, limit=limit)
    return TeamListResponse(
        teams=[t.to_schema() for t in teams],
        total=total,
    )


@router.get("/teams/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: str,
    service_router: TeamRouter = Depends(get_team_router),
    _: str = Depends(get_current_user),
):
    try:
        return (await service_router.service.get_team(team_id)).to_schema()
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.patch("/teams/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: str,
    payload: TeamUpdate,
    service_router: TeamRouter = Depends(get_team_router),
    _: str = Depends(get_current_user),
):
    try:
        return (await service_router.service.update_team(
            team_id, payload)).to_schema()
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.delete("/teams/{team_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
    team_id: str,
    service_router: TeamRouter = Depends(get_team_router),
    _: str = Depends(get_current_user),
):
    try:
        await service_router.service.delete_team(team_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)