from __future__ import with_statement
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from alembic import context
from sqlalchemy import create_engine, pool
import core_service.core_apis_server.models.models
from core_service.core_apis_server.settings import settings

config = context.config

if config.config_file_name is not None:
    from logging.config import fileConfig
    fileConfig(config.config_file_name)

target_metadata = core_service.core_apis_server.models.models.Base.metadata

user, password, host, db, port = settings.core_db_params()
DB_URL = (
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    f"?sslmode=require&channel_binding=require"
)


def run_migrations_offline():
    context.configure(
        url=DB_URL,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = create_engine(DB_URL)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()