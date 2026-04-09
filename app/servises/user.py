
from sqlalchemy.orm import Session
from app.models.user import User


def get_user_by_username(username: str, db: Session) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(id: int, db: Session) -> User | None:
    return db.query(User).filter(User.id == id).first()

