import logging
from fastapi import Request
from sqlalchemy.orm import Session

from core_service.core_apis_server.models.models import Team, Organization
from core_service.core_apis_server.services.base import BaseService
from core_service.core_apis_server.exceptions import Err, ConflictException, NotFoundException
from core_service.core_apis_server.schemas.team import TeamCreate, TeamUpdate

LOG = logging.getLogger(__name__)


class TeamService(BaseService):

    def __init__(self, db_session: Session, token: str = None,
                 request: Request = None, **kwargs):
        super().__init__(db_session, token, request, **kwargs)

    def _get_model_type(self):
        return Team

    async def create_team(self, organization_id: str,
                           payload: TeamCreate) -> Team:
        org = self._session.query(Organization).filter(
            Organization.id         == organization_id,
            Organization.deleted_at == 0,
        ).first()
        if not org:
            raise NotFoundException(Err.OC0011, [organization_id])
        existing = self._session.query(Team).filter(
            Team.name            == payload.name,
            Team.organization_id == organization_id,
            Team.deleted_at      == 0,
        ).first()
        if existing:
            raise ConflictException(Err.OC0016, [payload.name])
        team = Team(
            name=payload.name,
            description=payload.description,
            organization_id=organization_id,
            parent_id=payload.parent_id,
        )
        result = self.save(team)
        org.teams_count = self._session.query(Team).filter(
            Team.organization_id == organization_id,
            Team.deleted_at      == 0,
        ).count()
        self._session.commit()
        return result

    async def get_team(self, team_id: str) -> Team:
        return self.get_by_id(team_id)

    async def list_teams_by_organization(self, organization_id: str,
                                          skip: int = 0, limit: int = 20):
        query = self._session.query(Team).filter(
            Team.organization_id == organization_id,
            Team.deleted_at      == 0,
        )
        total = query.count()
        teams = query.offset(skip).limit(limit).all()
        return teams, total

    async def update_team(self, team_id: str, payload: TeamUpdate) -> Team:
        team = self.get_by_id(team_id)
        if payload.name is not None:
            team.name = payload.name
        if payload.description is not None:
            team.description = payload.description
        return self.update(team)

    async def delete_team(self, team_id: str):
        self.soft_delete(team_id)