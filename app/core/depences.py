from sqlalchemy.orm import Session
from app.servises.user import get_user_by_username
from app.db.session import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from app.core.config import config
from app.schemas.token import Token, TokenData


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token:str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credentails_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неправильные входные данные",
        headers={"WWW-Authenticate":"Bearer"}
    )

    print("Декодирован токен")

    print(config.SECRET_KEY, config.ALGORITHM)

    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms = ["HS256"])
        print("Токен декодирован")
        username = payload.get("sub")
        if not username:
            raise credentails_exception
        
        token_data = TokenData(username=username)

    except Exception as error:
        print(error)
        raise credentails_exception
    

    user = get_user_by_username(token_data.username, db)



    if not user:

        print("Не удалось получить пользователя")

        raise credentails_exception
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь не активен")
    
    return user


            