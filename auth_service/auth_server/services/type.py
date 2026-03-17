import logging
from fastapi import Request
from sqlalchemy.orm import Session

from auth_service.auth_server.models.models import Type
from auth_service.auth_server.services.base import BaseService

LOG = logging.getLogger(__name__)


class TypeService(BaseService):

    def __init__(self, db: Session, request: Request = None, **kwargs):
        super().__init__(db, request, **kwargs)

    def _get_model_type(self):
        return Type

    def list_types(self):
        return self._session.query(Type).filter(
            Type.deleted_at == 0).all()