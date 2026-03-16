import logging
from typing import Generic, TypeVar
from sqlalchemy.orm import Session

from auth_service.auth_server.utils import get_current_timestamp
from auth_service.auth_server.exceptions import NotFoundException, Err

LOG = logging.getLogger(__name__)

ModelT = TypeVar("ModelT")


class BaseService(Generic[ModelT]):
    """
    Generic base service providing common CRUD operations.
    All service classes inherit from this and pass their model type.

    Example:
        class UserService(BaseService[User]):
            def __init__(self, db: Session):
                super().__init__(db, User)
    """

    def __init__(self, db: Session, model: type[ModelT]):
        self.db    = db
        self.model = model

    def get_by_id(self, record_id) -> ModelT:
        """
        Fetch a single active record by primary key.
        Raises NotFoundException if not found or soft-deleted.
        """
        record = self.db.query(self.model).filter(
            self.model.id         == record_id,
            self.model.deleted_at == 0,
        ).first()
        if not record:
            raise NotFoundException(Err.OA0028, [self.model.__name__, record_id])
        return record

    def list_active(self, skip: int = 0, limit: int = 20):
        """
        Return a paginated list of all active (non-deleted) records.
        Returns a tuple of (records, total_count).
        """
        query = self.db.query(self.model).filter(self.model.deleted_at == 0)
        total = query.count()
        records = query.offset(skip).limit(limit).all()
        return records, total

    def soft_delete(self, record_id) -> None:
        """
        Soft-delete a record by setting deleted_at to current timestamp.
        Raises NotFoundException if the record does not exist.
        """
        record = self.get_by_id(record_id)
        record.deleted_at = get_current_timestamp()
        self.db.commit()
        LOG.info("Soft-deleted %s with id %s", self.model.__name__, record_id)

    def save(self, record: ModelT) -> ModelT:
        """
        Persist a new record to the database.
        Sets created_at automatically and returns the refreshed record.
        """
        record.created_at = get_current_timestamp()
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        LOG.info("Created %s with id %s", self.model.__name__, record.id)
        return record

    def update(self, record: ModelT) -> ModelT:
        
        self.db.commit()
        self.db.refresh(record)
        LOG.info("Updated %s with id %s", self.model.__name__, record.id)
        return record