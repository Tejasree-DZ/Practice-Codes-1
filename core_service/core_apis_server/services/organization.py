import logging
from fastapi import Request
from sqlalchemy.orm import Session

from core_service.core_apis_server.models.models import Organization, Team, Member
from core_service.core_apis_server.services.base import BaseService
from core_service.core_apis_server.exceptions import Err, ConflictException, NotFoundException
from core_service.core_apis_server.schemas.organization import OrganizationCreate, OrganizationUpdate

LOG = logging.getLogger(__name__)


class OrganizationService(BaseService):

    def __init__(self, db_session: Session, token: str = None,
                 request: Request = None, **kwargs):
        super().__init__(db_session, token, request, **kwargs)

    def _get_model_type(self):
        return Organization

    async def create_organization(self, user_id: str,
                                   payload: OrganizationCreate) -> Organization:
        existing = self._session.query(Organization).filter(
            Organization.name       == payload.name,
            Organization.deleted_at == 0,
        ).first()
        if existing:
            raise ConflictException(Err.OC0015, [payload.name])
        org = Organization(
            name=payload.name,
            description=payload.description,
        )
        return self.save(org)

    async def get_organization(self, organization_id: str) -> Organization:
        return self.get_by_id(organization_id)

    async def list_organizations(self, skip: int = 0, limit: int = 20):
        return self.list_active(skip=skip, limit=limit)

    async def update_organization(self, organization_id: str,
                                   payload: OrganizationUpdate) -> Organization:
        org = self.get_by_id(organization_id)
        if payload.name is not None:
            org.name = payload.name
        if payload.description is not None:
            org.description = payload.description
        return self.update(org)

    async def delete_organization(self, organization_id: str):
        self.soft_delete(organization_id)

    def update_counts(self, organization_id: str):
        org = self.get_by_id(organization_id)
        org.teams_count = self._session.query(Team).filter(
            Team.organization_id == organization_id,
            Team.deleted_at      == 0,
        ).count()
        org.members_count = self._session.query(Member).join(Team).filter(
            Team.organization_id == organization_id,
            Team.deleted_at      == 0,
            Member.deleted_at    == 0,
        ).count()
        self._session.commit()