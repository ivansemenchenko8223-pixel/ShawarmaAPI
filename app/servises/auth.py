from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token
from app.servises.user import get_user_by_username


def authenticate_user(username:str, password:str, db:Session)->User:
    user = get_user_by_username(username, db)
    if not user or not verify_password(password, hash_password=user.hashed_password):
        return None
    return user


def register_user(user:UserCreate, db:Session)->User:
    hash_password = get_password_hash(user.password)
    db_user = User(
        email = user.email,
        username = user.username,
        hashed_password = hash_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
