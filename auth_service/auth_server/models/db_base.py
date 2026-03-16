
import logging

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine import Engine
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

import auth_service.auth_server.models.models as model_base

LOG = logging.getLogger(__name__)


def should_retry(retry_state) -> bool:
    LOG.warning(
        "DB connection attempt %s failed: %s — retrying...",
        retry_state.attempt_number,
        retry_state.outcome.exception(),
    )
    return True


class BaseDB(object):

    def __init__(self, config=None, _scopefunc=None):
        self._engine    = None
        self._config    = config
        self._scopefunc = _scopefunc

    @staticmethod
    def session(engine: Engine, scopefunc=None) -> scoped_session:
        return scoped_session(
            sessionmaker(bind=engine),
            scopefunc=scopefunc,
        )

    @retry(
        stop=stop_after_attempt(20),
        wait=wait_fixed(1),
        retry=retry_if_exception_type(Exception),
        before_sleep=should_retry,
    )
    def create_all(self):
        model_base.Base.metadata.create_all(self.engine)

    def drop_all(self):
        model_base.Base.metadata.drop_all(self.engine)

    def ping(self) -> bool:
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except Exception as e:
            LOG.error("Database ping failed: %s", e)
            return False

    @property
    def engine(self) -> Engine:
        if not self._engine:
            self._engine = self._get_engine()
        return self._engine

    def _get_engine(self) -> Engine:
        raise NotImplementedError