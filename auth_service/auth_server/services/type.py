from sqlalchemy.orm import Session
from auth_server.models.models import Type


def get_types(db: Session):
    return db.query(Type).all()