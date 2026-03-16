import logging
from sqlalchemy.orm import Session
from auth_service.auth_server.models.models import Role
from auth_service.auth_server.exceptions import Err, NotFoundException

LOG = logging.getLogger(__name__)

class RoleService:
    def __init__(self, db: Session): self.db = db

    def get_by_id(self, role_id: int) -> Role:
        role = self.db.query(Role).filter(Role.id == role_id, Role.deleted_at == 0).first()
        if not role: raise NotFoundException(Err.OA0025, [role_id])
        return role

    def list_roles(self):
        return self.db.query(Role).filter(Role.deleted_at == 0).all()