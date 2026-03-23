import logging
from fastapi import Request
from sqlalchemy.orm import Session

from core_service.core_apis_server.models.models import Member, Team
from core_service.core_apis_server.services.base import BaseService
from core_service.core_apis_server.exceptions import Err, ConflictException, NotFoundException
from core_service.core_apis_server.schemas.member import MemberCreate

LOG = logging.getLogger(__name__)


class MemberService(BaseService):

    def __init__(self, db_session: Session, token: str = None,
                 request: Request = None, **kwargs):
        super().__init__(db_session, token, request, **kwargs)

    def _get_model_type(self):
        return Member

    async def add_member(self, team_id: str, payload: MemberCreate) -> Member:
        team = self._session.query(Team).filter(
            Team.id         == team_id,
            Team.deleted_at == 0,
        ).first()
        if not team:
            raise NotFoundException(Err.OC0012, [team_id])
        existing = self._session.query(Member).filter(
            Member.team_id      == team_id,
            Member.auth_user_id == payload.auth_user_id,
            Member.deleted_at   == 0,
        ).first()
        if existing:
            raise ConflictException(Err.OC0017)
        member = Member(
            team_id=team_id,
            auth_user_id=payload.auth_user_id,
        )
        return self.save(member)

    async def list_members_by_team(self, team_id: str,
                                    skip: int = 0, limit: int = 20):
        query   = self._session.query(Member).filter(
            Member.team_id    == team_id,
            Member.deleted_at == 0,
        )
        total   = query.count()
        members = query.offset(skip).limit(limit).all()
        return members, total

    async def remove_member(self, member_id: str):
        self.soft_delete(member_id)