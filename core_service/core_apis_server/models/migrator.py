import os
import logging

from alembic.config import Config
from alembic import command

import core_service.core_apis_server.models.models as models

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
        self.alembic_cfg.set_main_option("sqlalchemy.url", self.engine_url)

    def migrate(self):
        LOG.info("Running Alembic migrations for %s", self.engine_url)
        command.upgrade(self.alembic_cfg, "head")
        LOG.info("Migrations complete.")

    def migrate_all(self):
        try:
            self.migrate()
        except Exception as ex:
            LOG.error("Failed to apply migrations: %s", str(ex))
            raise