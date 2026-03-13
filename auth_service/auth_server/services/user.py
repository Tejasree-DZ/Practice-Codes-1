from sqlalchemy.orm import Session
from auth_server.models.models import User
from auth_server.utils import hash_password


def create_user(db: Session, user):
    db_user = User(
        email=user.email,
        password=hash_password(user.password),
        name=user.name,
        type_id=user.type_id
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)

    if user:
        db.delete(user)
        db.commit()

    return user

def update_user(db, user_id, user):
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        return {"error": "User not found"}

    if user.email:
        db_user.email = user.email

    if user.password:
        db_user.password = user.password

    if user.name:
        db_user.name = user.name

    db.commit()
    db.refresh(db_user)

    return db_user