
#database connection string methods and sessions
import logging
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, scoped_session
import time


def get_current_timestamp() -> int:
    return int(time.time())

from auth_service.auth_server.models.models import Base

logger = logging.getLogger(__name__)


def _should_retry(exception: Exception) -> bool:
    logger.warning("DB connection attempt failed: %s — retrying…", exception)
    return True


class BaseDB:
    def __init__(self, config=None) -> None:
        self._engine: Engine | None = None
        self._config = config

    @staticmethod
    def session(engine: Engine) -> scoped_session:
        return scoped_session(sessionmaker(bind=engine))

    @retry(
        stop_max_attempt_number=20,
        wait_fixed=1000,
        retry_on_exception=_should_retry,
    )
    def create_all(self) -> None:
        Base.metadata.create_all(self.engine)

    @property
    def engine(self) -> Engine:
        if not self._engine:
            self._engine = self._get_engine()
        return self._engine

    def _get_engine(self) -> Engine:
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement _get_engine()"
        )