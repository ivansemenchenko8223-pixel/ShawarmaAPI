from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.schemas.order import Order, OrderCreate
from app.models.product import Product


def get_order(db:Session, order_id:int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_user_orders(db:Session, user_id:int):
    return db.query(Order).filter(user_id == Order.user_id).all()


def  create_order(db:Session, order:OrderCreate, user_id:int):
    db_order = Order(user_id = user_id)
    db.add(db_order)
    db.flush()
    
    total_price = 0

    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise ValueError(f"Продукт с данным {item.product_id} не найден")
        
        price = product.price*item.quantity
        total_price+=price
        db_item = OrderItem(order_id = db_order.id, 
                            product_id = item.product_id,
                            quantity = item.quantity,
                            price = price)
        db.add(db_item)

    db_order.total_price == total_price
    db.commit()
    db.refresh()
    return db_orders

