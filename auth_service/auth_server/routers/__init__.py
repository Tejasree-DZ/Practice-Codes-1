from fastapi import APIRouter

from .user import router as user_router
from .role import router as role_router
from .type import router as type_router
from .assignment import router as assignment_router
from .token import router as token_router


routers = APIRouter(prefix="/auth/v1")

routers.include_router(user_router)
routers.include_router(role_router)
routers.include_router(type_router)
routers.include_router(assignment_router)
routers.include_router(token_router)