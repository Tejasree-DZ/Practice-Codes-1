from sqlalchemy.orm import Session
from auth_server.models.db_base import SessionLocal 


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()