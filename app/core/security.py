from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import datetime
from typing import Dict, List, Optional
from app.core.config import config
from sqlalchemy.orm import Session
import string
from jose import jwt



pwd_context = CryptContext(schemes=[config.ALGORITHM,"bcrypt"], default = "argon2", deprecated = "auto")


def get_password_hash(password:str):
    return pwd_context.hash(password)


def verify_password(password:str, hash_password:str):
    return pwd_context.verify(password, hash_password)


def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, config.ALGORITHM)
    return encoded_jwt