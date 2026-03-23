import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import uvicorn
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from auth_service.auth_server.settings import settings
from auth_service.auth_server.globals import configure_logging
from auth_service.auth_server.middleware import log_requests
from auth_service.auth_server.routers import routers

LOG = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging(settings.DEBUG)
    LOG.info("Starting Auth Service...")
    from auth_service.auth_server.models.db_postgres import postgres_db
    postgres_db.create_schema()
    LOG.info("Database schema ready.")
    yield
    LOG.info("Shutting down Auth Service.")


app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

app.include_router(routers)


@app.get("/health")
def health():
    from auth_service.auth_server.models.db_postgres import postgres_db
    return {"status": "ok", "db": postgres_db.ping()}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host = "127.0.0.1",
        port = 8000,
        reload=True
    )