from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth_server.services.base import get_db
from auth_server.services import assignment as assignment_service

router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.post("")
def create_assignment(assignment, db: Session = Depends(get_db)):
    return assignment_service.create_assignment(db, assignment)


@router.get("")
def get_assignments(db: Session = Depends(get_db)):
    return assignment_service.get_assignments(db)


@router.delete("/{assignment_id}")
def delete_assignment(assignment_id: int, db: Session = Depends(get_db)):
    return assignment_service.delete_assignment(db, assignment_id)