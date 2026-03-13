from sqlalchemy.orm import Session
from auth_server.models.models import Assignment


def create_assignment(db: Session, assignment):
    db_assignment = Assignment(
        user_id=assignment.user_id,
        role_id=assignment.role_id
    )

    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)

    return db_assignment


def get_assignments(db: Session):
    return db.query(Assignment).all()


def delete_assignment(db: Session, assignment_id: int):
    assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id
    ).first()

    if assignment:
        db.delete(assignment)
        db.commit()

    return assignment