from fastapi import APIRouter

from .organization import router as organization_router
from .team import router as team_router
from .member import router as member_router

routers = APIRouter(prefix="/core/v1")

routers.include_router(organization_router)
routers.include_router(team_router)
routers.include_router(member_router)