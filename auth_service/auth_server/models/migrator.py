import os
import logging

from alembic.config import Config
from alembic import command

import auth_service.auth_server.models.models as models

LOG = logging.getLogger(__name__)

target_metadata = models.Base.metadata


class Migrator(object):
    def __init__(self, engine):
        self._engine    = engine
        self.engine_url = str(self._engine.url)

        self.alembic_cfg = Config()
        self.alembic_cfg.set_main_option(
            "script_location",
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                '..', 'alembic'
            ),
        )
        self.alembic_cfg.set_main_option(
            "sqlalchemy.url", self.engine_url
        )

    def migrate(self):
        LOG.info("Running Alembic migrations for %s", self.engine_url)
        command.upgrade(self.alembic_cfg, "head")
        LOG.info("Migrations complete.")

    def _seed_reference_data(self):
        from auth_service.auth_server.models.enums import RoleName, TypeName
        from sqlalchemy.orm import sessionmaker

        session = sessionmaker(bind=self._engine)()
        try:
            for type_name in TypeName:
                existing = session.query(models.Type).filter_by(
                    name=type_name.value).first()
                if not existing:
                    session.add(models.Type(name=type_name.value))

            for role_name in RoleName:
                existing = session.query(models.Role).filter_by(
                    name=role_name.value).first()
                if not existing:
                    session.add(models.Role(name=role_name.value))

            session.commit()
            LOG.info("Reference data seeded successfully.")
        except Exception as e:
            session.rollback()
            LOG.error("Failed to seed reference data: %s", e)
            raise
        finally:
            session.close()

    def migrate_all(self):
        try:
            self.migrate()
            self._seed_reference_data()
        except Exception as ex:
            LOG.error("Failed to apply migrations: %s", str(ex))
            raise