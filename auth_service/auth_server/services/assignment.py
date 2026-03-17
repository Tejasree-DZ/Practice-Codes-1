import logging
from fastapi import Request
from sqlalchemy.orm import Session

from auth_service.auth_server.models.models import Assignment
from auth_service.auth_server.services.base import BaseService
from auth_service.auth_server.exceptions import Err, ConflictException
from auth_service.auth_server.schemas.assignment import AssignmentCreate

LOG = logging.getLogger(__name__)


class AssignmentService(BaseService):

    def __init__(self, db: Session, request: Request = None, **kwargs):
        super().__init__(db, request, **kwargs)

    def _get_model_type(self):
        return Assignment

    def list_assignments(self, user_id=None, resource_id=None,
                         skip=0, limit=20):
        query = self._session.query(Assignment).filter(
            Assignment.deleted_at == 0)
        if user_id:
            query = query.filter(Assignment.user_id == user_id)
        if resource_id:
            query = query.filter(Assignment.resource_id == resource_id)
        total = query.count()
        return query.offset(skip).limit(limit).all(), total

    def create_assignment(self, data: AssignmentCreate) -> Assignment:
        existing = self._session.query(Assignment).filter(
            Assignment.user_id     == data.user_id,
            Assignment.role_id     == data.role_id,
            Assignment.type_id     == data.type_id,
            Assignment.resource_id == data.resource_id,
            Assignment.deleted_at  == 0,
        ).first()
        if existing:
            raise ConflictException(Err.OA0035, ["Assignment"])
        assignment = Assignment(
            user_id=data.user_id,
            role_id=data.role_id,
            type_id=data.type_id,
            resource_id=data.resource_id,
        )
        return self.save(assignment)

    def delete_assignment(self, assignment_id: str):
        self.soft_delete(assignment_id)