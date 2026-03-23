from sqlalchemy import create_engine

from core_service.core_apis_server.models.db_base import BaseDB
from core_service.core_apis_server.models.migrator import Migrator
from core_service.core_apis_server.settings import settings


class PostgresDB(BaseDB):

    def _get_engine(self):
        user, password, host, db, port = settings.core_db_params()
        return create_engine(
            f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
            f"?sslmode=require&channel_binding=require",
            pool_recycle=300,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )

    def create_schema(self):
        migrator = Migrator(self.engine)
        migrator.migrate_all()


postgres_db = PostgresDB()