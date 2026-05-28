from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate


def get_products(db:Session, limit:int=100, offset:int=0):
    return db.query(Product).offset(offset).limit(limit).all()


def get_product(db:Session, product_id:int):
    return db.query(Product).filter(Product.id == product_id).first()


def  create_product(db:Session, product:ProductCreate):
    print("Создание новой записи")
    db_product = Product(
        **product.model_dump()
    )
    print("Модель создана")
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product