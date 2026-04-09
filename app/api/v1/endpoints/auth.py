from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import config
from app.schemas.user import UserCreate, User
from app.db.session import get_db
from app.servises.user import get_user_by_username, get_user_by_email
from app.servises.auth import register_user, authenticate_user
from datetime import timedelta
from app.core.security import create_access_token


router = APIRouter(prefix="/auth")


@router.post("/register", status_code=status.HTTP_200_OK)
def register(user:UserCreate, db:Session=Depends(get_db)):
    db_user = get_user_by_username(user.username, db)
    if db_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Такой username уже есть")
    
    db_user = get_user_by_email(user.email, db)
    if db_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Такой email уже есть")
    return register_user(user, db)


@router.post("/login")
def login(form_data:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Неправильный username или password",
            headers= {"WWW-Authenticate":"Bearer"}
        )
    
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub":user.username})
    return {"access_token":access_token, "token_type":"Bearer"}