import logging
from sqlalchemy.orm import Session
from auth_service.auth_server.models.models import Type
from auth_service.auth_server.exceptions import Err, NotFoundException

LOG = logging.getLogger(__name__)

class TypeService:
    def __init__(self, db: Session): self.db = db

    def get_by_id(self, type_id: int) -> Type:
        t = self.db.query(Type).filter(Type.id == type_id, Type.deleted_at == 0).first()
        if not t: raise NotFoundException(Err.OA0056, [type_id])
        return t

    def list_types(self):
        return self.db.query(Type).filter(Type.deleted_at == 0).all()