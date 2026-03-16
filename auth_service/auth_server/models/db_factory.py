import logging
from enum import Enum
from auth_service.auth_server.exceptions import Err, WrongArgumentsException

LOG = logging.getLogger(__name__)

class DBType(Enum):
    POSTGRES = "postgres"

class DBFactory(object):
    _instances = {}

    @staticmethod
    def _get_db(db_type, config):
        from auth_service.auth_server.models.db_postgres import PostgresDB
        DBS = {DBType.POSTGRES: PostgresDB}
        db_class = DBS.get(db_type)
        if not db_class:
            LOG.error('Nonexistent model type specified: %s', db_type)
            raise WrongArgumentsException(Err.OA0045, [db_type])
        return db_class(config)

    def __new__(cls, db_type, config, *args, **kwargs):
        cls._db = None
        if db_type not in cls._instances:
            instance = super().__new__(cls, *args, **kwargs)
            instance._db = DBFactory._get_db(db_type, config)
            cls._instances[db_type] = instance
        return cls._instances[db_type]

    @classmethod
    def clean_type(cls, db_type):
        if cls._instances.get(db_type): del cls._instances[db_type]

    @property
    def db(self): return self._db