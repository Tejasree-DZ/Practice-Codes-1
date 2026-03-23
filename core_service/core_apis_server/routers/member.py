import logging
from fastapi import Depends, Request, status, HTTPException
from sqlalchemy.orm import Session

from core_service.core_apis_server.routers.base import make_router, BaseRouter
from core_service.core_apis_server.services.member import MemberService
from core_service.core_apis_server.schemas.member import (
    MemberCreate, MemberResponse, MemberListResponse
)
from core_service.core_apis_server.dependencies import get_db, get_current_user
from core_service.core_apis_server.exceptions import (
    NotFoundException, ConflictException
)

LOG    = logging.getLogger(__name__)
router = make_router(prefix="/core/v1", tags=["members"])


class MemberRouter(BaseRouter):
    service_class = MemberService


def get_member_router(
    request: Request,
    session: Session = Depends(get_db),
) -> MemberRouter:
    return MemberRouter(request, session)


@router.post("/teams/{team_id}/members",
             response_model=MemberResponse,
             status_code=status.HTTP_201_CREATED)
async def add_member(
    team_id: str,
    payload: MemberCreate,
    service_router: MemberRouter = Depends(get_member_router),
    _: str = Depends(get_current_user),
):
    try:
        return (await service_router.service.add_member(
            team_id, payload)).to_schema()
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except ConflictException as e:
        raise HTTPException(status_code=409, detail=e.message)


@router.get("/teams/{team_id}/members",
            response_model=MemberListResponse)
async def list_members(
    team_id: str,
    skip: int = 0,
    limit: int = 20,
    service_router: MemberRouter = Depends(get_member_router),
    _: str = Depends(get_current_user),
):
    members, total = await service_router.service.list_members_by_team(
        team_id, skip=skip, limit=limit)
    return MemberListResponse(
        members=[m.to_schema() for m in members],
        total=total,
    )


@router.delete("/members/{member_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    member_id: str,
    service_router: MemberRouter = Depends(get_member_router),
    _: str = Depends(get_current_user),
):
    try:
        await service_router.service.remove_member(member_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)