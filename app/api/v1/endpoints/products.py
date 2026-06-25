from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import config
from app.schemas.product import ProductCreate, Product
from app.db.session import get_db
from app.servises.user import get_user_by_username, get_user_by_email
from datetime import timedelta
from app.servises import product
from app.core.depences import get_current_user, get_current_admin_user
from app.servises.product import create_product as create_new_product



router = APIRouter(prefix="/products")


@router.get("/")
def get_products(offset:int=0, limit:int=100, db:Session=Depends(get_db)):
    return product.get_products(db, limit, offset) 


@router.post("/")
def create_product(product:ProductCreate, db:Session=Depends(get_db),current_admin=Depends(get_current_admin_user)):
    print("Дошло до эндпоинта")
    return create_new_product(db,product)