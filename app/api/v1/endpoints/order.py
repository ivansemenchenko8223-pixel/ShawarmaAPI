from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import config
from app.schemas.order import Order, OrderCreate
from app.db.session import get_db
from app.servises.user import get_user_by_username, get_user_by_email
from datetime import timedelta
from app.servises.order import get_order, get_user_orders, create_order as create_new_order
from app.core.depences import get_current_user
from app.servises.product import create_product as create_new_product


router = APIRouter(prefix="/orders")

@router.post("/order")
def create_order(order:OrderCreate, db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    try:
        return create_new_order(db,order, current_user.id)
    except ValueError as error:
        raise HTTPException(status_code=400,
                            detail=str(error))