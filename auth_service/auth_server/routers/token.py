import logging
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from auth_service.auth_server.routers.base import make_router
from auth_service.auth_server.schemas.token import TokenRequest, RefreshTokenRequest, TokenResponse
from auth_service.auth_server.services.token import TokenService
from auth_service.auth_server.dependencies import get_db
from auth_service.auth_server.exceptions import UnauthorizedException, InvalidTokenException

LOG = logging.getLogger(__name__)
router = make_router(tags=["token"])

@router.post("/token", response_model=TokenResponse)
def login(data: TokenRequest, db: Session = Depends(get_db)):
    try: return TokenService(db).login(data)
    except UnauthorizedException as e: raise HTTPException(status_code=401, detail=e.message)

@router.post("/refresh_token", response_model=TokenResponse)
def refresh_token(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    try: return TokenService(db).refresh(data)
    except (UnauthorizedException, InvalidTokenException) as e:
        raise HTTPException(status_code=401, detail=e.message)