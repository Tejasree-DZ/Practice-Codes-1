"""
models/migrator.py
------------------
Provides the ``Migrator`` class responsible for:

1.  Running all pending Alembic migrations against the given engine.
2.  Seeding the reference data (Role rows, Type rows) that must exist
    before any API calls are made.

Called from db_postgres.py exactly as in the OptScale MySQLDB reference:

    def create_schema(self):
        migrator = Migrator(self.engine)
        migrator.migrate_all()
"""

import logging

from alembic import command
from alembic.config import Config
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Role, Type
from .enums import RoleName, TypeName

logger = logging.getLogger(__name__)


class Migrator:
    """
    Runs Alembic migrations and seeds static reference data.

    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
        The live engine to run migrations and seeding against.
        Passed in by PostgresDB.create_schema so that Migrator never
        needs to know about connection strings or settings directly.

    Usage
    -----
    ::

        migrator = Migrator(engine)
        migrator.migrate_all()
    """

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    # ── Public entry point ────────────────────────────────────────────────────

    def migrate_all(self) -> None:
        """
        Run all pending Alembic migrations then seed reference data.
        Called once on application startup from PostgresDB.create_schema().
        """
        self._run_migrations()
        self._seed_reference_data()

    # ── Migrations ────────────────────────────────────────────────────────────

    def _run_migrations(self) -> None:
        """Upgrade the database schema to the latest Alembic revision."""
        logger.info("Running Alembic migrations…")
        cfg = Config("alembic.ini")
        # Override the URL so Alembic uses the same engine the app uses
        cfg.set_main_option(
            "sqlalchemy.url",
            str(self._engine.url),
        )
        command.upgrade(cfg, "head")
        logger.info("Alembic migrations complete.")

    # ── Seeding ───────────────────────────────────────────────────────────────

    def _seed_reference_data(self) -> None:
        """Insert Role and Type rows if they do not already exist."""
        session: Session = sessionmaker(bind=self._engine)()
        try:
            self._seed_roles(session)
            self._seed_types(session)
            session.commit()
            logger.info("Reference data seeding complete.")
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def _seed_roles(session: Session) -> None:
        existing = {
            r.name
            for r in session.query(Role).filter(Role.deleted_at.is_(None)).all()
        }
        for role in RoleName:
            if role.value not in existing:
                session.add(
                    Role(
                        name=role.value,
                        description=f"Built-in {role.value} role",
                    )
                )
                logger.info("Seeded role: %s", role.value)

    @staticmethod
    def _seed_types(session: Session) -> None:
        existing = {
            t.name
            for t in session.query(Type).filter(Type.deleted_at.is_(None)).all()
        }
        for typ in TypeName:
            if typ.value not in existing:
                session.add(
                    Type(
                        name=typ.value,
                        description=f"Resource type: {typ.value}",
                    )
                )
                logger.info("Seeded type: %s", typ.value)