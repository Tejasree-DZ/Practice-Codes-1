import logging
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth_service.auth_server.routers.base import make_router
from auth_service.auth_server.schemas.assignment import AssignmentCreate, AssignmentResponse, AssignmentListResponse
from auth_service.auth_server.services.assignment import AssignmentService
from auth_service.auth_server.dependencies import get_db, get_current_user
from auth_service.auth_server.exceptions import NotFoundException, ConflictException

LOG = logging.getLogger(__name__)
router = make_router(tags=["assignments"])

@router.post("/assignments", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_assignment(data: AssignmentCreate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    try: return AssignmentService(db).create_assignment(data).to_schema()
    except ConflictException as e: raise HTTPException(status_code=409, detail=e.message)

@router.get("/assignments", response_model=AssignmentListResponse)
def list_assignments(user_id: str = None, resource_id: str = None, skip: int = 0, limit: int = 20,
                     db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    assignments, total = AssignmentService(db).list_assignments(
        user_id=user_id, resource_id=resource_id, skip=skip, limit=limit)
    return AssignmentListResponse(assignments=[a.to_schema() for a in assignments], total=total)

@router.delete("/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assignment(assignment_id: str, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    try: AssignmentService(db).delete_assignment(assignment_id)
    except NotFoundException as e: raise HTTPException(status_code=404, detail=e.message)