from app.api.v1.endpoints import auth, products, order
from fastapi import APIRouter


router = APIRouter(prefix="/api/v1")

router.include_router(auth.router)
router.include_router(products.router)
router.include_router(order.router)
