import logging
from typing import Generic, TypeVar
from fastapi import Request
from sqlalchemy.orm import Session

from auth_service.auth_server.utils import get_current_timestamp
from auth_service.auth_server.exceptions import NotFoundException, Err

LOG = logging.getLogger(__name__)

ModelT = TypeVar("ModelT")


class BaseService(Generic[ModelT]):

    def __init__(self, db: Session, request: Request = None, **kwargs):
        self._session    = db
        self._request    = request
        self._token      = None
        self._config     = None
        self._model_type = None

    # ── Token ─────────────────────────────────────────────────────────────────

    @property
    def token(self) -> str:
        if self._token is None:
            token = getattr(self._request.state, "token", None)
            if not token:
                auth_header = self._request.headers.get("Authorization", "")
                if auth_header.startswith("Bearer "):
                    token = auth_header.split(" ")[1]
                    self._request.state.token = token
            self._token = token
        return self._token

    # ── User ──────────────────────────────────────────────────────────────────

    @property
    def user(self):
        return getattr(self._request.state, "user", None)

    @property
    def user_id(self) -> str | None:
        user = self.user
        if user:
            return user.id
        return None

    # ── Config ────────────────────────────────────────────────────────────────

    @property
    def config(self):
        if self._config is None:
            from auth_service.auth_server.settings import settings
            self._config = settings
        return self._config

    # ── Model type ────────────────────────────────────────────────────────────

    @property
    def model_type(self):
        if self._model_type is None:
            self._model_type = self._get_model_type()
        return self._model_type

    def _get_model_type(self):
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement _get_model_type()"
        )

    # ── Session ───────────────────────────────────────────────────────────────

    @property
    def session(self) -> Session:
        return self._session

    # ── CRUD operations ───────────────────────────────────────────────────────

    def get_by_id(self, record_id) -> ModelT:
        record = self._session.query(self.model_type).filter(
            self.model_type.id         == record_id,
            self.model_type.deleted_at == 0,
        ).first()
        if not record:
            raise NotFoundException(
                Err.OA0028, [self.model_type.__name__, record_id])
        return record

    def list_active(self, skip: int = 0, limit: int = 20):
        query = self._session.query(self.model_type).filter(
            self.model_type.deleted_at == 0)
        total   = query.count()
        records = query.offset(skip).limit(limit).all()
        return records, total

    def soft_delete(self, record_id) -> None:
        record = self.get_by_id(record_id)
        record.deleted_at = get_current_timestamp()
        self._session.commit()
        LOG.info("Soft-deleted %s with id %s",
                 self.model_type.__name__, record_id)

    def save(self, record: ModelT) -> ModelT:
        record.created_at = get_current_timestamp()
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)
        LOG.info("Created %s with id %s",
                 self.model_type.__name__, record.id)
        return record

    def update(self, record: ModelT) -> ModelT:
        self._session.commit()
        self._session.refresh(record)
        LOG.info("Updated %s with id %s",
                 self.model_type.__name__, record.id)
        return record