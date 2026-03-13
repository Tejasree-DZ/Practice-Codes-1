from sqlalchemy.orm import Session
from auth_server.models.models import Role


def get_roles(db: Session):
    return db.query(Role).all()