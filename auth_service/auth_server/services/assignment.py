import logging
from sqlalchemy.orm import Session
from auth_service.auth_server.models.models import Assignment
from auth_service.auth_server.utils import get_current_timestamp
from auth_service.auth_server.exceptions import Err, NotFoundException, ConflictException
from auth_service.auth_server.schemas.assignment import AssignmentCreate

LOG = logging.getLogger(__name__)

class AssignmentService:
    def __init__(self, db: Session): self.db = db

    def get_by_id(self, assignment_id: str) -> Assignment:
        a = self.db.query(Assignment).filter(
            Assignment.id == assignment_id, Assignment.deleted_at == 0).first()
        if not a: raise NotFoundException(Err.OA0019, [assignment_id])
        return a

    def list_assignments(self, user_id=None, resource_id=None, skip=0, limit=20):
        query = self.db.query(Assignment).filter(Assignment.deleted_at == 0)
        if user_id: query = query.filter(Assignment.user_id == user_id)
        if resource_id: query = query.filter(Assignment.resource_id == resource_id)
        total = query.count()
        return query.offset(skip).limit(limit).all(), total

    def create_assignment(self, data: AssignmentCreate) -> Assignment:
        existing = self.db.query(Assignment).filter(
            Assignment.user_id == data.user_id, Assignment.role_id == data.role_id,
            Assignment.type_id == data.type_id, Assignment.resource_id == data.resource_id,
            Assignment.deleted_at == 0).first()
        if existing: raise ConflictException(Err.OA0035, ["Assignment"])
        a = Assignment(user_id=data.user_id, role_id=data.role_id,
                       type_id=data.type_id, resource_id=data.resource_id)
        a.created_at = get_current_timestamp()
        self.db.add(a); self.db.commit(); self.db.refresh(a)
        return a

    def delete_assignment(self, assignment_id: str):
        a = self.get_by_id(assignment_id)
        a.deleted_at = get_current_timestamp()
        self.db.commit()